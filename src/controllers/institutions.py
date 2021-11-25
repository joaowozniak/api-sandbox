from typing import List
from ..models.institution import Institution


def get_all_institutions() -> List[Institution]:
    institutions = [
        "Chase",
        "Bank of America",
        "Wells Fargo",
        "Citibank",
        "Capital One",
    ]
    out_institutions = []
    for inst in institutions:
        inst_aux = Institution(id=snake_casting(inst), name=inst)
        out_institutions.append(inst_aux)
    return out_institutions


def snake_casting(inst_name: str) -> str:
    inst_name = inst_name.lower()
    return inst_name.replace(" ", "_")
