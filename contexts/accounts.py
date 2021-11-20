from models.account import Account, get_all_account_names
from models.institution import Institution, get_all_institutions
import hashlib

base_link = "http://localhost/accounts/"

def from_token(token):

    enrollment_id = "enr_" + str(hashlib.sha256(token.encode()).hexdigest())[-22:]
    id = "acc_" + str(hashlib.md5(token.encode()).hexdigest())[-22:]
    institutions = get_all_institutions()
    institution = institutions[(abs(hash(str(hashlib.md5(token.encode()).hexdigest())))) % len(institutions)]
    acc_num = str(abs(hash(token)) % (98 ** 13))[-10:]
    last_four = acc_num[-4:]
    names = get_all_account_names()
    name = names[(abs(hash(str(hashlib.md5(token.encode()).hexdigest())))) % len(names)]
    
    return Account(
        currency = "USD",
        enrollment_id = enrollment_id,
        account_id = id,
        institution = institution,
        last_four = last_four,
        name = name,
        subtype = "checking",
        type = "depository"
    )
