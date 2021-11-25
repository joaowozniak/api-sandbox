import base64, datetime
from fastapi.testclient import TestClient
from src.main import *
from src.auth.basic_auth import *

client = TestClient(sandbox)

## Authentication tests
def test_login_one_account():
    '''
    Test login user with one account.
    '''
    username = "user_12345"
    password = ""
    
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")

    response = client.get("/login", headers = {"Authorization": f"Basic {param}"})
    assert response.status_code == 200
    assert response.json() == {"Log in": "OK"}


def test_login_more_accounts():
    '''
    Test login user with multiple accounts.
    '''
    username = "user_multiple_12345"
    password = ""
    
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")

    response = client.get("/login", headers = {"Authorization": f"Basic {param}"})
    assert response.status_code == 200
    assert response.json() == {"Log in": "OK"}


def test_fail_login():
    '''
    Test login fail.
    '''
    username = "12345"
    password = ""
    
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")

    response = client.get("/login", headers = {"Authorization": f"Basic {param}"})
    assert response.status_code == 401
    assert response.json() == {"detail":"Credentials not valid"}

def test_check_username():
    '''
    Test auth.basic_auth.check_username() function.
    '''
    username1 = "user_12345"
    out1 = check_username(username1)

    username2 = "user_multiple_12345"
    out2 = check_username(username2)

    username3 = "usr_multiple_12345"
    out3 = check_username(username3)

    assert out1['has_more_account'] == False
    assert out1['name'] == username1

    assert out2['has_more_account'] == True
    assert out2['name'] == username2

    assert out3['has_more_account'] == None
    assert out3['name'].startswith("_") == True
    

def test_verify_user():
    '''
    Test auth.basic_auth.verify_user() function.
    '''
    username1 = "user_12345"
    password1 = ""
    param1 = base64.b64encode((username1 + ":" + password1).encode()).decode("ascii")
    (_param1, has_more_account1) = verify_user(param1)

    username2 = "user_multiple_12345"
    password2 = ""
    param2 = base64.b64encode((username2 + ":" + password2).encode()).decode("ascii")
    (_param2, has_more_account2) = verify_user(param2)

    assert param1 == _param1
    assert has_more_account1 == False
    assert param2 == _param2
    assert has_more_account2 == True


def test_get_token():
    '''
    Test auth.basic_auth.get_token() function.
    '''
    username = "user_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
    token = get_token(param)
    expected = "test_dXNlcl8xMjM0NTo="
    assert token == expected


## Accounts tests
def test_accounts():
    '''
    Test /accounts endpoint for an user with one account.
    '''
    username = "user_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
  
    response = client.get("/accounts", headers = {"Authorization": f"Basic {param}"})
    expected = [
        {
            "currency":"USD",
            "enrollment_id":"enr_248c1839f51a8f5f8b799c",
            "id":"acc_4feaa04187bca8a4e52ad9",
            "institution": {
                "id":"chase",
                "name":"Chase"
            },
            "last_four":"4492",
            "links": {
                "balances":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/balances",
                "details":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/details",
                "self":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9",
                "transactions":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/transactions"
            },
            "name":"Jimmy Carter",
            "subtype":"checking",
            "type":"depository"
        }
    ]
   
    assert response.status_code == 200
    assert response.json() == expected
    

def test_accounts_multiple():
    '''
    Test /accounts endpoint for an user with multiple accounts.
    '''
    username = "user_multiple_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
  
    response = client.get("/accounts", headers = {"Authorization": f"Basic {param}"})
    expected = [
        {
            "currency":"USD",
            "enrollment_id":"enr_5dc1d3db6ed1f4a22e5772",
            "id":"acc_d47d8266af0fbae0831a46",
            "institution": {
                "id":"capital_one",
                "name":"Capital One"
            },
            "last_four":"3394",
            "links": {
                "balances":"http://localhost:8000/accounts/acc_d47d8266af0fbae0831a46/balances",
                "details":"http://localhost:8000/accounts/acc_d47d8266af0fbae0831a46/details",
                "self":"http://localhost:8000/accounts/acc_d47d8266af0fbae0831a46",
                "transactions":"http://localhost:8000/accounts/acc_d47d8266af0fbae0831a46/transactions"
            },
            "name":"Barack Obama",
            "subtype":"checking",
            "type":"depository"
            },
            {
                "currency":"USD",
                "enrollment_id":"enr_21ce24cdd2a3a105d4e447",
                "id":"acc_41e98f066fad5185ed73fb",
                "institution": {
                    "id":"citibank",
                    "name":"Citibank"
                },
                "last_four":"0743",
                "links": { 
                    "balances":"http://localhost:8000/accounts/acc_41e98f066fad5185ed73fb/balances",
                    "details":"http://localhost:8000/accounts/acc_41e98f066fad5185ed73fb/details",
                    "self":"http://localhost:8000/accounts/acc_41e98f066fad5185ed73fb",
                    "transactions":"http://localhost:8000/accounts/acc_41e98f066fad5185ed73fb/transactions"
                },
                "name":"George H. W. Bush",
                "subtype":"checking",
                "type":"depository"
            }
        ]
        
    assert response.status_code == 200
    assert response.json() == expected


def test_accounts_idx():
    '''
    Test /accounts/{idx} endpoint for an user with one account.
    '''
    username = "user_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
    account_id = "acc_4feaa04187bca8a4e52ad9"

    response = client.get(f"/accounts/{account_id}", headers = {"Authorization": f"Basic {param}"})
    expected = {
        "currency":"USD",
        "enrollment_id":"enr_248c1839f51a8f5f8b799c",
        "id":"acc_4feaa04187bca8a4e52ad9",
        "institution": {
            "id":"chase",
            "name":"Chase"
            },
        "last_four":"4492",
        "links": {
            "balances":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/balances",
            "details":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/details",
            "self":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9",
            "transactions":"http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/transactions"
            },
        "name":"Jimmy Carter",
        "subtype":"checking",
        "type":"depository"
    }

    assert response.status_code == 200
    assert response.json() == expected


def test_accounts_idx_details():
    '''
    Test /accounts/{idx}/details endpoint for an user with one account.
    '''
    username = "user_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
    account_id = "acc_4feaa04187bca8a4e52ad9"

    response = client.get(f"/accounts/{account_id}/details", headers = {"Authorization": f"Basic {param}"})
    expected = {
        "account_id": "acc_4feaa04187bca8a4e52ad9",
        "account_number": "3485614492",
        "links": {
            "account": "http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9",
            "self": "http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/details"
        },
        "routing_numbers": {
            "ach": "97718966"
        }
    }

    assert response.status_code == 200
    assert response.json() == expected


def test_accounts_idx_balances():
    '''
    Test /accounts/{idx}/balances endpoint for an user with one account.
    '''
    username = "user_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
    account_id = "acc_4feaa04187bca8a4e52ad9"

    response = client.get(f"/accounts/{account_id}/balances", headers = {"Authorization": f"Basic {param}"})
    expected = {
        "account_id": "acc_4feaa04187bca8a4e52ad9",
        "available": 2201,
        "ledger": 2201,
        "links": {
            "account": "http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9",
            "self": "http://localhost:8000/accounts/acc_4feaa04187bca8a4e52ad9/balances"
        }
    }

    assert response.status_code == 200
    assert response.json() == expected


def test_accounts_idx_transactions():
    '''
    Test /accounts/{idx}/transactions endpoint for an user with one account.
    '''
    username = "user_12345"
    password = ""
    param = base64.b64encode((username + ":" + password).encode()).decode("ascii")
    account_id = "acc_4feaa04187bca8a4e52ad9"
    start_date = datetime.date.today()

    response = client.get(f"/accounts/{account_id}/transactions", headers = {"Authorization": f"Basic {param}"})
    expected_today = start_date.strftime("%Y/%m/%d")

    day_delta = datetime.timedelta(days=1)
    expected_before = (start_date - 1 * day_delta).strftime("%Y/%m/%d")
    

    assert response.status_code == 200    
    assert response.json()[0]["date"] == expected_today
    assert response.json()[1]["date"] == expected_before
    assert (response.json()[0]["amount"]*(-1) + response.json()[0]["running_balance"]) == response.json()[1]["running_balance"]

