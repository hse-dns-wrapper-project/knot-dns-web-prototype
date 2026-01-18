from dataclasses import dataclass

from ...processor.command import Command

@dataclass(frozen=True)
class ZoneSet(Command):
    zone: str | None = None
    owner: str | None = None
    type: str | None = None
    ttl: str | None = None
    data: str | None = None

@dataclass(frozen=True)
class ZoneUnset(Command):
    zone: str | None = None
    owner: str | None = None
    type: str | None = None
    data: str | None = None
