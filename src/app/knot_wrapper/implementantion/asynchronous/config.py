
from typing import Any
from libknot.control import KnotCtl
from ...transaction import KnotConfigTransaction

from threading import Lock

from .commands.core.config import ConfigSet, ConfigUnset
from .processor.processor import Processor

global_config_lock = Lock()

global_knot_config_transaction_processor: Processor | None = None
def set_knot_config_transaction_processor(processor: Processor):
    global global_knot_config_transaction_processor
    global_knot_config_transaction_processor = processor

class KnotConfigTransactionMTImpl(KnotConfigTransaction):
    def __init__(self, reader_ctl: KnotCtl):
        super().__init__(reader_ctl, None)

    def open(self, timeout: int = -1):
        global global_config_lock

        global_config_lock.acquire(timeout = timeout)
    
    def commit(self):
        global global_config_lock

        global_config_lock.release()

    def rollback(self):
        global global_config_lock

        global_config_lock.release()

    def get(self, section: str, identifier: str, item: str, flags: str, filters: str) -> Any:
        self.reader_ctl.send_block(
            cmd="conf-read",
            section=section,
            identifier=identifier,
            item=item,
            flags=flags,
            filters=filters
        )
        result = self.reader_ctl.receive_block()
        return result
    
    def set(self, section: str, identifier: str, item: str, data: str):
        global global_knot_config_transaction_processor

        if global_knot_config_transaction_processor is None:
            return
        
        command = ConfigSet(
            section,
            identifier,
            item,
            data
        )

        future = global_knot_config_transaction_processor.add_priority_command(command)
        future.result()

    def unset(self, section: str, identifier: str, item: str):
        global global_knot_config_transaction_processor

        if global_knot_config_transaction_processor is None:
            return
        
        command = ConfigUnset(
            section,
            identifier,
            item
        )

        future = global_knot_config_transaction_processor.add_priority_command(command)
        future.result()