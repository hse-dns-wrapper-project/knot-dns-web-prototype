from dataclasses import dataclass

from ...processor.command import PriorityCommand

@dataclass(frozen=True)
class ConfigSet(PriorityCommand):
    section: str | None = None
    identifier: str | None = None
    item: str | None = None
    data: str | None = None

@dataclass(frozen=True)
class ConfigUnset(PriorityCommand):
    section: str | None = None
    identifier: str | None = None
    item: str | None = None