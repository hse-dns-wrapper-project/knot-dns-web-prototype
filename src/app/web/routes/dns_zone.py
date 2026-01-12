from fastapi import Request, Response, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.knot_wrapper.dns_zone import get_zone_by_name, get_zones_list, add_zone, remove_zone
from app.knot_wrapper.transactions import knot_socket, conf_transaction

router = APIRouter(prefix='')
templates = Jinja2Templates(directory='app/web/templates')

@router.get("/zone")
def get_all_zones():
    with knot_socket() as ctl:
        zones = get_zones_list(ctl)
        return JSONResponse(zones)

@router.get("/zone/{zone_domain}")
def get_zone_info_by_name(zone_domain):
    with knot_socket() as ctl:
        zones = get_zone_by_name(ctl, zone_domain)
        return JSONResponse(zones)

@router.post("/zone")
def add_new_zone(
    zone_domain: str
):
    with knot_socket() as ctl:
        with conf_transaction(ctl):
            add_zone(ctl, zone_domain)

@router.delete("/zone")
def remove_old_zone(
    zone_domain: str
):
    with knot_socket() as ctl:
        with conf_transaction(ctl):
            remove_zone(ctl, zone_domain)
