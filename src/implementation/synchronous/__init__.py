
from typing import Any
from libknot.control import KnotCtl
from ...transaction import KnotZoneTransaction, KnotConfigTransaction

from ...transaction import set_knot_config_transaction_impl, set_knot_zone_transaction_impl

from ..base_operations.config import get_config, set_config, unset_config
from ..base_operations.zone import get_zone, set_zone, unset_zone

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
        return get_zone(
            self.ctl,
            zone,
            owner,
            type
        )
    
    def set(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        ttl: str | None = None,
        data: str | None = None
    ):
        return set_zone(
            self.ctl,
            zone,
            owner,
            type,
            ttl,
            data
        )

    def unset(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        data: str | None = None
    ):
        return unset_zone(
            self.ctl,
            zone,
            owner,
            type,
            data
        )

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
        return get_config(
            self.ctl,
            section,
            identifier,
            item,
            flags,
            filters
        )
    
    def set(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        data: str | None = None
    ):
        return set_config(
            self.ctl,
            section,
            identifier,
            item,
            data
        )

    def unset(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None
    ):
        return unset_config(
            self.ctl,
            section,
            identifier,
            item
        )

set_knot_config_transaction_impl(KnotConfigTransactionImpl)
set_knot_zone_transaction_impl(KnotZoneTransactionImpl)