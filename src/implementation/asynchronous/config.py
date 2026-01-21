
from typing import Any
from libknot.control import KnotCtl
from ...transaction import KnotConfigTransaction

from .processor.command import Command, CommandBatch
from .commands.core.config import ConfigGet, ConfigSet, ConfigUnset, ConfigCommit
from .processor.processor import Processor

global_knot_config_transaction_processor: Processor | None = None
def set_knot_config_transaction_processor(processor: Processor):
    global global_knot_config_transaction_processor
    global_knot_config_transaction_processor = processor

class KnotConfigTransactionMTImpl(KnotConfigTransaction):
    def __init__(self, ctl: KnotCtl):
        super().__init__(ctl, None)

        self.transaction_write_buffer: list[Command] = list()

    def open(self, timeout: int = -1):
        self.transaction_write_buffer.clear()
    
    def commit(self):
        global global_knot_config_transaction_processor

        if global_knot_config_transaction_processor is None:
            return

        self.transaction_write_buffer.append(
            ConfigCommit()
        )
        command_batch = CommandBatch(
            tuple(
                self.transaction_write_buffer
            )
        )
        self.transaction_write_buffer.clear()
        
        future = global_knot_config_transaction_processor.add_command_batch(command_batch)
        future.result()

    def rollback(self):
        self.transaction_write_buffer.clear()

    def get(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        flags: str | None = None,
        filters: str | None = None
    ) -> Any:
        global global_knot_config_transaction_processor

        if global_knot_config_transaction_processor is None:
            return

        command = ConfigGet(section, identifier, item, flags, filters)
        future = global_knot_config_transaction_processor.add_priority_command(command)
        result = future.result()
        return result
    
    def set(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        data: str | None = None
    ):
        global global_knot_config_transaction_processor

        command = ConfigSet(section, identifier, item, data)
        self.transaction_write_buffer.append(command)

    def unset(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None
    ):
        command = ConfigUnset(section, identifier, item)
        self.transaction_write_buffer.append(command)