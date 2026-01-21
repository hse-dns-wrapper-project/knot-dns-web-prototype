from typing import Any

from .implementation.asynchronous.service import *
from .transaction import get_knot_config_transaction, get_knot_controller

def get_all_zones():
    with get_knot_controller("/root/knot/knot.sock") as ctl:
        with get_knot_config_transaction(ctl, global_processor) as transaction:
            result = transaction.get(section="zone")
            if len(result) == 0:
                return tuple()
            zones_dict: dict[str, Any] = result['zone']
            zones = tuple((name for name in zones_dict))
            return zones