
from typing import Any
from libknot.control import KnotCtl
from ...transaction import KnotZoneTransaction, KnotConfigTransaction

from ...transaction import set_knot_config_transaction_impl, set_knot_zone_transaction_impl

class KnotZoneTransactionImpl(KnotZoneTransaction):
    def __init__(self, ctl: KnotCtl):
        super().__init__(ctl, None)

    def open(self):
        self.ctl.send_block(cmd="zone-begin")
        self.ctl.receive_block()
    
    def commit(self):
        self.ctl.send_block(cmd="zone-commit")
        self.ctl.receive_block()

    def rollback(self):
        self.ctl.send_block(cmd="zone-abort")
        self.ctl.receive_block()
    
    def get(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None
    ):
        self.ctl.send_block(
            cmd="zone-read",
            zone=zone, # type: ignore
            owner=owner, # type: ignore
            rtype=type # type: ignore
        )
        result = self.ctl.receive_block()
        return result
    
    def set(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        ttl: str | None = None,
        data: str | None = None
    ):
        self.ctl.send_block(
            cmd="zone-set",
            zone=zone, # type: ignore
            owner=owner, # type: ignore
            rtype=type, # type: ignore
            ttl=ttl, # type: ignore
            data=data # type: ignore
        )
        self.ctl.receive_block()

    def unset(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        data: str | None = None):
        self.ctl.send_block(
            cmd="zone-unset",
            zone=zone, # type: ignore
            owner=owner, # type: ignore
            rtype=type, # type: ignore
            data=data # type: ignore
        )
        self.ctl.receive_block()

class KnotConfigTransactionImpl(KnotConfigTransaction):
    def __init__(self, ctl: KnotCtl):
        super().__init__(ctl, None)

    def open(self):
        self.ctl.send_block(cmd="conf-begin")
        self.ctl.receive_block()
    
    def commit(self):
        self.ctl.send_block(cmd="conf-commit")
        self.ctl.receive_block()

    def rollback(self):
        self.ctl.send_block(cmd="conf-abort")
        self.ctl.receive_block()

    def get(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        flags: str | None = None,
        filters: str | None = None
    ) -> Any:
        self.ctl.send_block(
            cmd="conf-read",
            section=section, # type: ignore
            identifier=identifier, # type: ignore
            item=item, # type: ignore
            flags=flags, # type: ignore
            filters=filters # type: ignore
        )
        result = self.ctl.receive_block()
        return result
    
    def set(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        data: str | None = None
    ):
        self.ctl.send_block(
            cmd="conf-set",
            section=section, # type: ignore
            identifier=identifier, # type: ignore
            item=item, # type: ignore
            data=data # type: ignore
        )
        self.ctl.receive_block()

    def unset(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None
    ):
        self.ctl.send_block(
            cmd="conf-unset",
            section=section, # type: ignore
            identifier=identifier, # type: ignore
            item=item # type: ignore
        )
        self.ctl.receive_block()

set_knot_config_transaction_impl(KnotConfigTransactionImpl)
set_knot_zone_transaction_impl(KnotZoneTransactionImpl)