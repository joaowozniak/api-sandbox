import hashlib, datetime
from typing import List, Optional
from models.account import Account
from models.transaction import Transaction
from models.description import Description
from models.counterparty import Counterparty
from models.transaction_link import Transaction_Link



def fill_links(acc: str):

    base_link = "http://localhost:8000/transactions/"

    return Transaction_Link(
        account=(base_link + acc + "/account"), self=(base_link + acc)
    )

def generate_data_from_acc(acc: Account):

    day_delta = datetime.timedelta(days=1)

    start_date = datetime.date.today()
    end_date = start_date - 5 * day_delta

    transactions = []

    acc_amount = acc.available

    for i in range((start_date - end_date).days + 1):
        date = start_date - i * day_delta

        trans_id = str(
            hashlib.sha256(
                (acc.account_id + date.strftime("%Y/%m/%d")).encode()
            ).hexdigest()
        )[-22:]

        merchs = get_all_merchants()
        merch = merchs[abs(hash(trans_id)) % len(merchs)]

        categories = get_all_categories()
        category = categories[abs(hash(trans_id)) % len(categories)]

        descr_counterparty = Counterparty(name=merch, type="organization")
        trans_description = Description(
            category=category,
            counterparty=descr_counterparty,
            processing_status="complete",
        )

        trans_links = fill_links(trans_id)

        trans_amount = -generate_amount(trans_id)
        trans_running_balance = acc_amount
        acc_amount -= trans_amount

        trans = Transaction(
            account_id=acc.account_id,
            amount=trans_amount,
            date=date.strftime("%Y/%m/%d"),
            description=trans_description,
            id=trans_id,
            links=trans_links,
            running_balance=trans_running_balance,
            status="posted",
            type="card_payment",
            processing_status="ok",
        )

        transactions.append(trans)
    return transactions


def generate_amount(transaction_id: str) -> int:
    amounts = [i for i in range(0, 100)]
    amount = amounts[abs(hash(transaction_id)) % len(amounts)]
    amount = -amount
    return amount


def get_all_merchants():
    merchants = [
        "Uber",
        "Uber Eats",
        "Lyft",
        "Five Guys",
        "In-N-Out Burger",
        "Chick-Fil-A",
        "AMC",
        "Apple",
        "Amazon",
        "Walmart",
        "Target",
        "Hotel Tonight",
        "Misson Ceviche",
        "The",
        "Caltrain",
        "Wingstop",
        "Slim Chickens",
        "CVS",
        "Duane Reade",
        "Walgreens",
        "Roo",
        "McDonald's",
        "Burger King",
        "KFC",
        "Popeye's",
        "Shake Shack",
        "Lowe's",
        "The Ho",
        "Costco",
        "Kroger",
        "iTunes",
        "Spotify",
        "Best Buy",
        "TJ Maxx",
        "Aldi",
        "Dollar",
        "Macy's",
        "H.E. Butt",
        "Dollar Tree",
        "Verizon Wireless",
        "Sprint PCS",
        "T-Mobil",
        "Starbucks",
        "7-Eleven",
        "AT&T Wireless",
        "Rite Aid",
        "Nordstrom",
        "Ross",
        "Gap",
        "Bed, Bath & Beyond",
        "J.C. Penney",
        "Subway",
        "O'Reilly",
        "Wendy's",
        "Dunkin' D",
        "Petsmart",
        "Dick's Sporting Goods",
        "Sears",
        "Staples",
        "Domino's Pizza",
        "Pizz",
        "Papa John's",
        "IKEA",
        "Office Depot",
        "Foot Locker",
        "Lids",
        "GameStop",
        "Sepho",
        "Panera",
        "Williams-Sonoma",
        "Saks Fifth Avenue",
        "Chipotle Mexican Grill",
        "Exx",
        "Neiman Marcus",
        "Jack In The Box",
        "Sonic",
        "Shell",
    ]
    return merchants


def get_all_categories():
    categories = [
        "accommodation",
        "advertising",
        "bar",
        "charity",
        "clothing",
        "dining",
        "education",
        "entertainment",
        "fuel",
        "groceries",
        "health",
        "home",
        "income",
        "insurance",
        "office",
        "phone",
        "service",
        "shopping",
        "software",
        "sport",
        "tax",
        "transportion",
        "utilities",
    ]
    return categories
