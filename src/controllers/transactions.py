import hashlib, datetime
from typing import List, Optional
from ..models.account import Account
from ..models.transaction import Transaction
from ..models.description import Description
from ..models.counterparty import Counterparty
from ..models.transaction_link import Transaction_Link


def fill_links(account_id: str, transaction_id: str) -> Transaction_Link:

    base_link = "http://localhost:8000/accounts/"

    return Transaction_Link(
        account=(base_link + account_id),
        self=(base_link + account_id + "/transactions/" + transaction_id),
    )


def encode_with_alfanumeric(account_id: str, date: datetime.date) -> str:
    encoded = str(
        hashlib.sha256((account_id + date.strftime("%Y/%m/%d")).encode()).hexdigest()
    )[-22:]

    return encoded


def generate_transactions(account: Account) -> List[Transaction]:

    day_delta = datetime.timedelta(days=1)
    start_date = datetime.date.today()
    end_date = start_date - 90 * day_delta

    transactions = []

    account_amount = account.available
    account_id = account.account_id

    for day in range((start_date - end_date).days):
        date = start_date - day * day_delta

        trans_key = encode_with_alfanumeric(account.account_id, date)
        trans_id = "txn_" + trans_key
        trans_id_num = int(hashlib.md5(trans_key.encode()).hexdigest(), 16)

        merchants = get_all_merchants()
        merchant = merchants[trans_id_num % len(merchants)]

        categories = get_all_categories()
        category = categories[trans_id_num % len(categories)]

        description_counterparty = Counterparty(name=merchant, type="organization")
        trans_description = Description(
            category=category,
            counterparty=description_counterparty,
            processing_status="complete",
        )

        trans_links = fill_links(account_id, trans_id)

        trans_amount = generate_amount(trans_id_num)

        trans = Transaction(
            account_id=account.account_id,
            amount=trans_amount,
            date=date.strftime("%Y/%m/%d"),
            description=trans_description,
            id=trans_id,
            links=trans_links,
            running_balance=account_amount,
            status="posted",
            type="card_payment",
            processing_status="complete",
        )

        account_amount = account_amount - trans_amount
        transactions.append(trans)
    return transactions


def generate_amount(transaction_id: str) -> float:
    amounts = [i for i in range(1, 100)]
    amount = amounts[transaction_id % len(amounts)]
    return amount * (-1.0)


def get_transaction_by_id(transactions: List[Transaction], id: str) -> Transaction:
    for trans in transactions:
        if id == trans.id:
            return trans
    return None


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
