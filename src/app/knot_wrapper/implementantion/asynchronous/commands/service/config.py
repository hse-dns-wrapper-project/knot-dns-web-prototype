
from ...service.processor import bind_command_global as bind_command
from ..core.config import ConfigSet, ConfigUnset

from ...service.knot_write_port import global_knot_write_port

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