
from ...service.processor import bind_command_global as bind_command
from ..core.config import ConfigGet, ConfigSet, ConfigUnset, ConfigCommit

from ...service.knot_write_port import global_knot_write_port

@bind_command(ConfigGet)
def get_config(command: ConfigGet):
    global global_knot_write_port

    global_knot_write_port.send_block(
        cmd="conf-read",
        section=command.section, # type: ignore
        identifier=command.identifier, # type: ignore
        item=command.item, # type: ignore
        flags=command.flags, # type: ignore
        filters=command.filters # type: ignore
    )
    result = global_knot_write_port.receive_block()
    return result

@bind_command(ConfigSet)
def set_config(command: ConfigSet):
    global global_knot_write_port

    global_knot_write_port.send_block(
        cmd="conf-set",
        section=command.section, # type: ignore
        identifier=command.identifier, # type: ignore
        item=command.item, # type: ignore
        data=command.data # type: ignore
    )
    global_knot_write_port.receive_block()

@bind_command(ConfigUnset)
def unset_config(command: ConfigUnset):
    global global_knot_write_port

    global_knot_write_port.send_block(
        cmd="conf-unset",
        section=command.section, # type: ignore
        identifier=command.identifier, # type: ignore
        item=command.item # type: ignore
    )
    global_knot_write_port.receive_block()

@bind_command(ConfigCommit)
def commit_config(command: ConfigCommit):
    global global_knot_write_port
    global_knot_write_port.send_block(cmd="conf-commit")
    global_knot_write_port.receive_block()