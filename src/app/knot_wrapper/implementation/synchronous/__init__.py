
from typing import Any
from libknot.control import KnotCtl
from ...transaction import KnotZoneTransaction, KnotConfigTransaction

from ...transaction import set_knot_config_transaction_impl, set_knot_zone_transaction_impl

class KnotZoneTransactionImpl(KnotZoneTransaction):
    def __init__(self, reader_ctl: KnotCtl):
        super().__init__(reader_ctl, None)

    def open(self):
        self.reader_ctl.send_block(cmd="zone-begin")
        self.reader_ctl.receive_block()
    
    def commit(self):
        self.reader_ctl.send_block(cmd="zone-commit")
        self.reader_ctl.receive_block()

    def rollback(self):
        self.reader_ctl.send_block(cmd="zone-abort")
        self.reader_ctl.receive_block()
    
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
        self.reader_ctl.send_block(
            cmd="zone-set",
            zone=zone,
            owner=owner,
            rtype=type,
            ttl=ttl,
            data=data
        )
        self.reader_ctl.receive_block()

    def unset(self, zone: str, owner: str, type: str, data: str | None = None):
        self.reader_ctl.send_block(
            cmd="zone-unset",
            zone=zone,
            owner=owner,
            rtype=type,
            data=data # type: ignore
        )
        self.reader_ctl.receive_block()

class KnotConfigTransactionImpl(KnotConfigTransaction):
    def __init__(self, reader_ctl: KnotCtl):
        super().__init__(reader_ctl, None)

    def open(self):
        self.reader_ctl.send_block(cmd="conf-begin")
        self.reader_ctl.receive_block()
    
    def commit(self):
        self.reader_ctl.send_block(cmd="conf-commit")
        self.reader_ctl.receive_block()

    def rollback(self):
        self.reader_ctl.send_block(cmd="conf-abort")
        self.reader_ctl.receive_block()

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
        self.reader_ctl.send_block(
            cmd="conf-set",
            section=section,
            identifier=identifier,
            item=item,
            data=data
        )
        self.reader_ctl.receive_block()

    def unset(self, section: str, identifier: str, item: str):
        self.reader_ctl.send_block(
            cmd="conf-unset",
            section=section,
            identifier=identifier,
            item=item
        )
        self.reader_ctl.receive_block()

set_knot_config_transaction_impl(KnotConfigTransactionImpl)
set_knot_zone_transaction_impl(KnotZoneTransactionImpl)