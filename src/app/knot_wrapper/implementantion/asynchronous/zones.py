
from libknot.control import KnotCtl
from ...transaction import KnotZoneTransaction

from .processor.processor import Processor

from .processor.command import Command, CommandBatch
from .commands.core.zone import ZoneSet, ZoneUnset

global_knot_zone_transaction_processor: Processor | None = None
def set_knot_zone_transaction_processor(processor: Processor):
    global global_knot_zone_transaction_processor
    global_knot_zone_transaction_processor = processor

class KnotZoneTransactionMTImpl(KnotZoneTransaction):
    def __init__(self, reader_ctl: KnotCtl):
        super().__init__(reader_ctl, None)

        self.transaction_write_buffer: list[Command] = list()

    def open(self):
        self.reader_ctl.send_block(cmd="zone-begin")
        self.reader_ctl.receive_block()

        self.transaction_write_buffer.clear()
    
    def commit(self):
        global global_knot_zone_transaction_processor

        self.reader_ctl.send_block(cmd="zone-abort")
        self.reader_ctl.receive_block()

        self.transaction_write_buffer.clear()
        if global_knot_zone_transaction_processor is None:
            return

        command_batch = CommandBatch(
            tuple(
                self.transaction_write_buffer
            )
        )
        
        future = global_knot_zone_transaction_processor.add_command_batch(command_batch)
        future.result()

    def rollback(self):
        self.reader_ctl.send_block(cmd="zone-abort")
        self.reader_ctl.receive_block()
    
        self.transaction_write_buffer.clear()

    def get(self, zone: str, owner: str, type: str):
        self.reader_ctl.send_block(
            cmd="zone-read",
            zone=zone,
            owner=owner,
            rtype=type
        )
        result = self.reader_ctl.receive_block()
        return result
    
    def set(self, zone: str, owner: str, type: str, ttl: str, data: str):
        global global_knot_zone_transaction_processor

        command = ZoneSet(zone, owner, type, ttl, data)
        self.transaction_write_buffer.append(command)

    def unset(self, zone: str, owner: str, type: str, data: str | None = None):
        command = ZoneUnset(zone, owner, type, data)
        self.transaction_write_buffer.append(command)