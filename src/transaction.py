from typing import Any
from abc import ABC, abstractmethod
from contextlib import contextmanager
from libknot.control import KnotCtl

class KnotConfigTransaction(ABC):
    def __init__(
        self,
        ctl: KnotCtl,
        processor
    ):
        self.ctl = ctl
        self.processor = processor

        self.open()

    @abstractmethod
    def get(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        flags: str | None = None,
        filters: str | None = None
    ) -> Any:
        pass
    
    @abstractmethod
    def set(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None,
        data: str | None = None
    ):
        pass

    @abstractmethod
    def unset(
        self,
        section: str | None = None,
        identifier: str | None = None,
        item: str | None = None
    ):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

class KnotZoneTransaction(ABC):
    def __init__(
        self,
        ctl: KnotCtl,
        processor
    ):
        self.ctl = ctl
        self.processor = processor

        self.open()

    @abstractmethod
    def get(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None
    ) -> Any:
        pass

    @abstractmethod
    def set(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        ttl: str | None = None,
        data: str | None = None
    ):
        pass

    @abstractmethod
    def unset(
        self,
        zone: str | None = None,
        owner: str | None = None,
        type: str | None = None,
        data: str | None = None
    ):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

global_knot_config_transaction_impl: type[KnotConfigTransaction] | None = None
global_knot_zone_transaction_impl: type[KnotZoneTransaction] | None = None

def set_knot_config_transaction_impl(impl: type[KnotConfigTransaction]):
    global global_knot_config_transaction_impl
    global_knot_config_transaction_impl = impl

def set_knot_zone_transaction_impl(impl: type[KnotZoneTransaction]):
    global global_knot_zone_transaction_impl
    global_knot_zone_transaction_impl = impl

@contextmanager
def get_knot_controller(path: str):
    ctl = None
    try:
        ctl = KnotCtl()
        ctl.connect(path)
        yield ctl
    finally:
        if ctl is not None:
            ctl.close()

@contextmanager
def get_knot_config_transaction(
    ctl: KnotCtl,
    processor
):
    global global_knot_config_transaction_impl
    transaction = None
    try:
        if global_knot_config_transaction_impl is None:
            raise ValueError
        transaction = global_knot_config_transaction_impl(ctl, processor)
        yield transaction
        transaction.commit()
    except:
        if transaction is not None:
            transaction.rollback()
        raise

@contextmanager
def get_knot_zone_transaction(
    ctl: KnotCtl,
    processor
):
    global global_knot_zone_transaction_impl
    transaction = None
    try:
        if global_knot_zone_transaction_impl is None:
            raise ValueError
        transaction = global_knot_zone_transaction_impl(ctl, processor)
        yield transaction
        transaction.commit()
    except:
        if transaction is not None:
            transaction.rollback()
        raise

