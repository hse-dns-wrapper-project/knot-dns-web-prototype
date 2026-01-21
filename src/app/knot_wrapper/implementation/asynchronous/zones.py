
from libknot.control import KnotCtl
from ...transaction import KnotZoneTransaction

from .processor.processor import Processor

from .processor.command import Command, CommandBatch
from .commands.core.zone import ZoneGet, ZoneSet, ZoneUnset, ZoneCommit

global_knot_zone_transaction_processor: Processor | None = None
def set_knot_zone_transaction_processor(processor: Processor):
    global global_knot_zone_transaction_processor
    global_knot_zone_transaction_processor = processor

class KnotZoneTransactionMTImpl(KnotZoneTransaction):
    def __init__(self, ctl: KnotCtl):
        super().__init__(ctl, None)

        self.transaction_write_buffer: list[Command] = list()

    def open(self):
        self.transaction_write_buffer.clear()
    
    def commit(self):
        global global_knot_zone_transaction_processor

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

    def rollback(self):
        self.transaction_write_buffer.clear()

    def get(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None
    ):
        global global_knot_zone_transaction_processor

        if global_knot_zone_transaction_processor is None:
            return

        command = ZoneGet(zone, owner, type)
        future = global_knot_zone_transaction_processor.add_priority_command(command)
        result = future.result()
        return result
    
    def set(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        ttl: str | None = None,
        data: str | None = None
    ):
        global global_knot_zone_transaction_processor

        command = ZoneSet(zone, owner, type, ttl, data)
        self.transaction_write_buffer.append(command)

    def unset(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        data: str | None = None
    ):
        command = ZoneUnset(zone, owner, type, data)
        self.transaction_write_buffer.append(command)