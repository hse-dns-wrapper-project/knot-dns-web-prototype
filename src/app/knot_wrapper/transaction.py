from abc import ABC, abstractmethod
from contextlib import contextmanager
from libknot.control import KnotCtl

class KnotConfigTransaction(ABC):
    def __init__(
        self,
        reader_ctl: KnotCtl,
        processor
    ):
        self.reader_ctl = reader_ctl
        self.processor = processor

        self.open()

    @abstractmethod
    def get(
        self,
        section: str,
        identifier: str,
        item: str,
        flags: str,
        filters: str
    ):
        pass
    
    @abstractmethod
    def set(
        self,
        section: str,
        identifier: str,
        item: str,
        data: str
    ):
        pass

    @abstractmethod
    def unset(
        self,
        section: str,
        identifier: str,
        item: str
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
        reader_ctl: KnotCtl,
        processor
    ):
        self.reader_ctl = reader_ctl
        self.processor = processor

        self.open()

    @abstractmethod
    def get(
        self,
        zone: str,
        owner: str,
        type: str
    ):
        pass

    @abstractmethod
    def set(
        self,
        zone: str,
        owner: str,
        type: str,
        ttl: str,
        data: str
    ):
        pass

    @abstractmethod
    def unset(
        self,
        zone: str,
        owner: str,
        type: str,
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
def get_knot_reader(path: str):
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
    reader_ctl: KnotCtl,
    processor
):
    global global_knot_config_transaction_impl
    transaction = None
    try:
        if global_knot_config_transaction_impl is None:
            raise ValueError
        transaction = global_knot_config_transaction_impl(reader_ctl, processor)
        yield transaction
        transaction.commit()
    except:
        if transaction is not None:
            transaction.rollback()
        raise

@contextmanager
def get_knot_zone_transaction(
    reader_ctl: KnotCtl,
    processor
):
    global global_knot_zone_transaction_impl
    transaction = None
    try:
        if global_knot_zone_transaction_impl is None:
            raise ValueError
        transaction = global_knot_zone_transaction_impl(reader_ctl, processor)
        yield transaction
        transaction.commit()
    except:
        if transaction is not None:
            transaction.rollback()
        raise

