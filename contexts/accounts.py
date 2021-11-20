from models.account import Account, get_all_account_names
from models.account_link import Account_Link, fill_links
from models.institution import Institution, get_all_institutions
import hashlib

base_link = "http://localhost:8000/accounts/"

def from_token(token) -> Account:

    enrollment_id = "enr_" + str(hashlib.sha256(token.encode()).hexdigest())[-22:]
    id = "acc_" + str(hashlib.md5(token.encode()).hexdigest())[-22:]
    institutions = get_all_institutions()
    institution = institutions[(abs(hash(str(hashlib.md5(token.encode()).hexdigest())))) % len(institutions)]
    acc_num = str(abs(hash(token)) % (10 ** 13))[-10:]    
    last_four = acc_num[-4:]
    names = get_all_account_names()
    name = names[(abs(hash(str(hashlib.md5(token.encode()).hexdigest())))) % len(names)]
    links = fill_links(base_link, id)
    
    return Account(
        currency = "USD",
        enrollment_id = enrollment_id,
        account_id = id,
        institution = institution,
        account_number = acc_num,
        last_four = last_four,
        links = links,
        name = name,
        subtype = "checking",
        type = "depository"
    )
