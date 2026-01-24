
from ...service.processor import bind_command_global as bind_command
from ..core.config import ConfigGet, ConfigSet, ConfigUnset, ConfigCommit, ConfigAbort, ConfigBegin

from ...service.knot_write_port import global_knot_controller

from ....base_operations.config import get_config, set_config, unset_config

@bind_command(ConfigGet)
def _get_config(command: ConfigGet):
    global global_knot_controller

    return get_config(
        global_knot_controller,
        command.section,
        command.identifier,
        command.item,
        command.flags,
        command.filters
    )

@bind_command(ConfigSet)
def _set_config(command: ConfigSet):
    global global_knot_controller

    return set_config(
        global_knot_controller,
        command.section,
        command.identifier,
        command.item,
        command.data
    )

@bind_command(ConfigUnset)
def _unset_config(command: ConfigUnset):
    global global_knot_controller

    return unset_config(
        global_knot_controller,
        command.section,
        command.identifier,
        command.item
    )

@bind_command(ConfigBegin)
def begin_config(command: ConfigBegin):
    global global_knot_controller
    global_knot_controller.send_block(cmd="conf-begin")
    global_knot_controller.receive_block()

@bind_command(ConfigAbort)
def abort_config(command: ConfigAbort):
    global global_knot_controller
    global_knot_controller.send_block(cmd="conf-abort")
    global_knot_controller.receive_block()

@bind_command(ConfigCommit)
def commit_config(command: ConfigCommit):
    global global_knot_controller
    global_knot_controller.send_block(cmd="conf-commit")
    global_knot_controller.receive_block()