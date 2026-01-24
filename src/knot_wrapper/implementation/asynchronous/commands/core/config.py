from dataclasses import dataclass

from ...processor.command import PriorityCommand, Command

@dataclass(frozen=True)
class ConfigGet(PriorityCommand):
    section: str | None = None
    identifier: str | None = None
    item: str | None = None
    flags: str | None = None
    filters: str | None = None

@dataclass(frozen=True)
class ConfigSet(Command):
    section: str | None = None
    identifier: str | None = None
    item: str | None = None
    data: str | None = None

@dataclass(frozen=True)
class ConfigUnset(Command):
    section: str | None = None
    identifier: str | None = None
    item: str | None = None

@dataclass(frozen=True)
class ConfigBegin(Command):
    pass

@dataclass(frozen=True)
class ConfigAbort(Command):
    pass

@dataclass(frozen=True)
class ConfigCommit(Command):
    pass