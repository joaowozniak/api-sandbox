import hashlib
from ..models.routing_number import Routing_Number


def get_routingnum_by_inst(inst_id: str) -> str:
    ach = str(int(hashlib.sha256(inst_id.encode()).hexdigest(), 16))[-8:]
    return Routing_Number(ach=ach)
