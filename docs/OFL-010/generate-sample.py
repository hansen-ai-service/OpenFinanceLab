import csv
import random
from datetime import date, timedelta
from decimal import Decimal

SEED = 42
TOTAL_ROWS = 24
START, END = date(2022, 1, 1), date(2026, 3,31) # entries taken place in past

# Columns for database structure
COLS = ["transaction_id", "transaction_date", "type", "amount", "currency",
        "category", "description", "counterparty", "payment_method"]

# data follows structure: type -> category -> (min_amount, max_amount, description)
CATEGORIES = {
    "revenue": {
        "product_sales": (25, 2500, ["Starter kit order", "Bulk order", "Accessory order"]),
        "services": (300, 5000, ["Consulting invoice", "Website build", "Training session"]),
        "subscriptions": (19, 199, ["Monthly plan", "Annual plan"]),
        "other_revenue": (20, 500, ["Referral bonus", "Interest income"]),
    },
    "expense": {
        "payroll": (400, 1500, ["Payroll run"]),
        "rent": (1200, 1800, ["Office rent"]),
        "software": (10, 200, ["Project tool license", "Cloud hosting"]),
        "marketing": (50, 800, ["Online ads", "Newsletter tool"]),
        "supplies": (20, 300, ["Office supplies"]),
        "utilities": (40, 250, ["Internet service", "Electricity"]),
        "other_expense": (10, 200, ["Bank fees", "Misc expense"]),
    },
}
COUNTERPARTIES = {
    "revenue": ["Acme Corp", "Brightside LLC", "Maple Retail", "Northwind Co", "Cedar Supply", ""],
    "expense": ["Summit Properties", "Notion", "AdReach", "Paper Depot", "Beehive Telecom", ""]
}
PAYMENT_METHODS = ["card", "bank_transfer", "cash", "check", "other", ""]

# code to generate the data
def generate(kind, n, rng, seen_keys):
    prefix = "REV" if kind == "revenue" else "EXP"
    rows = []
    while len(rows) < n:
        category = rng.choice(list(CATEGORIES[kind]))
        lo, hi, descs = CATEGORIES[kind][category]
        row ={
            "transaction_date": (START + timedelta(days=rng.randint(0, (END - START).days))).isoformat(),
            "type": kind,
            "amount": str((Decimal(rng.randint(lo * 100, hi * 100)) / 100).quantize(Decimal("0.01"))),
            "currency": "USD",
            "category": category,
            "description": rng.choice(descs),
            "counterparty": rng.choice(COUNTERPARTIES[kind]),
            "payment_method": rng.choice(PAYMENT_METHODS),
        }
        # duplicate key from shcema: never create a duplicate record
        key = (row["transaction_date"], row["type"], row["category"],
                row["description"], row["counterparty"], row["payment_method"])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        rows.append(row)
    rows.sort(key=lambda r: r["transaction_date"])
    for i, r in enumerate(rows, start=1):
        r["transaction_id"] = f"{prefix}{i:04d}"
    return rows

if __name__ == "__main__":
    rng = random.Random(SEED)
    seen = set()
    n_rev = TOTAL_ROWS // 2
    rows = generate("revenue", n_rev, rng, seen) + generate("expense", TOTAL_ROWS - n_rev, rng, seen)

    with open("sample_transactions.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to sample_transactions.csv")
