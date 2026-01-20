
from ...service.processor import bind_command_global as bind_command
from ..core.zone import ZoneGet, ZoneSet, ZoneUnset, ZoneCommit

from ...service.knot_write_port import global_knot_write_port

@bind_command(ZoneGet)
def get_zone(command: ZoneGet):
    global global_knot_write_port

    global_knot_write_port.send_block(
        cmd="zone-read",
        zone=command.zone, # type: ignore
        owner=command.owner, # type: ignore
        rtype=command.type # type: ignore
    )
    result = global_knot_write_port.receive_block()
    return result

@bind_command(ZoneSet)
def set_zone(command: ZoneSet):
    global global_knot_write_port

    global_knot_write_port.send_block(
        cmd="zone-set",
        zone=command.zone, # type: ignore
        owner=command.owner, # type: ignore
        rtype=command.type, # type: ignore
        ttl=command.ttl, # type: ignore
        data=command.data # type: ignore
    )
    global_knot_write_port.receive_block()

@bind_command(ZoneUnset)
def unset_zone(command: ZoneUnset):
    global global_knot_write_port

    global_knot_write_port.send_block(
        cmd="zone-unset",
        zone=command.zone, # type: ignore
        owner=command.owner, # type: ignore
        rtype=command.type, # type: ignore
        data=command.data # type: ignore
    )
    global_knot_write_port.receive_block()

@bind_command(ZoneCommit)
def commit_config(command: ZoneCommit):
    global global_knot_write_port
    global_knot_write_port.send_block(cmd="conf-commit")
    global_knot_write_port.receive_block()