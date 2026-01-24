
from libknot.control import KnotCtl
from ...transaction import KnotZoneTransaction

from .processor.processor import Processor

from .processor.command import Command, CommandBatch
from .commands.core.zone import ZoneGet, ZoneSet, ZoneUnset, ZoneCommit

from .versions.storage import VersionsStorage
from .service.versions import global_versions_controller
from .service.commit_lock import global_commit_lock

global_knot_zone_transaction_processor: Processor | None = None
def set_knot_zone_transaction_processor(processor: Processor):
    global global_knot_zone_transaction_processor
    global_knot_zone_transaction_processor = processor

class KnotZoneTransactionMTImpl(KnotZoneTransaction):
    def __init__(self, ctl: KnotCtl):
        super().__init__(ctl)

        self.transaction_write_buffer: list[Command] = list()
        self.versions_storage = VersionsStorage()

    def open(self):
        self.transaction_write_buffer.clear()
    
    def __try_buffer_versions__(self):
        global global_versions_controller

        for command in self.transaction_write_buffer:
            if (
                isinstance(command, ZoneGet) or
                isinstance(command, ZoneSet) or
                isinstance(command, ZoneUnset)
            ):
                key = (command.zone, command.owner, command.type)
            else:
                return
            
            self.versions_storage.try_object(
                global_versions_controller,
                key
            )

    def __update_buffer_versions__(self):
        global global_versions_controller

        for command in self.transaction_write_buffer:
            if (
                isinstance(command, ZoneGet) or
                isinstance(command, ZoneSet) or
                isinstance(command, ZoneUnset)
            ):
                key = (command.zone, command.owner, command.type)
            else:
                return
            
            self.versions_storage.update_object(
                global_versions_controller,
                key
            )

    def commit(self):
        global global_knot_zone_transaction_processor, global_commit_lock

        if global_knot_zone_transaction_processor is None:
            return

        self.transaction_write_buffer.append(
            ZoneCommit()
        )

        command_batch = CommandBatch(
            tuple(
                self.transaction_write_buffer
            )
        )
        self.transaction_write_buffer.clear()
        
        future = global_knot_zone_transaction_processor.add_command_batch(command_batch)
        future.result()

        with global_commit_lock:
            self.__try_buffer_versions__()
            self.__update_buffer_versions__()

    def rollback(self):
        self.transaction_write_buffer.clear()

    def get(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None
    ):
        global global_knot_zone_transaction_processor, global_versions_controller

        if global_knot_zone_transaction_processor is None:
            return

        command = ZoneGet(
            zone,
            owner,
            type
        )
        future = global_knot_zone_transaction_processor.add_priority_command(command)
        result = future.result()

        key = (zone, owner, type)
        self.versions_storage.try_object(
            global_versions_controller,
            key
        )

        return result
    
    def set(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        ttl: str | None = None,
        data: str | None = None
    ):
        global global_knot_zone_transaction_processor, global_versions_controller

        key = (zone, owner, type)
        self.versions_storage.update_object(
            global_versions_controller,
            key
        )

        command = ZoneSet(
            zone,
            owner,
            type,
            ttl,
            data
        )
        self.transaction_write_buffer.append(command)

    def unset(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        data: str | None = None
    ):
        global global_versions_controller

        key = (zone, owner, type)
        self.versions_storage.update_object(
            global_versions_controller,
            key
        )

        command = ZoneUnset(
            zone,
            owner,
            type,
            data
        )
        self.transaction_write_buffer.append(command)