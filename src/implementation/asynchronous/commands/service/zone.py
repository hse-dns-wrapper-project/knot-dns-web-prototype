
from ...service.processor import bind_command_global as bind_command
from ..core.zone import ZoneGet, ZoneSet, ZoneUnset, ZoneCommit

from ...service.knot_write_port import global_knot_controller

from ....base_operations.zone import get_zone, set_zone, unset_zone

@bind_command(ZoneGet)
def _get_zone(command: ZoneGet):
    global global_knot_controller

    return get_zone(
        global_knot_controller,
        command.zone,
        command.owner,
        command.type
    )

@bind_command(ZoneSet)
def _set_zone(command: ZoneSet):
    global global_knot_controller

    return set_zone(
        global_knot_controller,
        command.zone,
        command.owner,
        command.type,
        command.ttl,
        command.data
    )

@bind_command(ZoneUnset)
def _unset_zone(command: ZoneUnset):
    global global_knot_controller

    return unset_zone(
        global_knot_controller,
        command.zone,
        command.owner,
        command.type,
        command.data
    )

@bind_command(ZoneCommit)
def commit_config(command: ZoneCommit):
    global global_knot_controller
    global_knot_controller.send_block(cmd="conf-commit")
    global_knot_controller.receive_block()