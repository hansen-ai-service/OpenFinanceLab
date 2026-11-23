import argparse
import csv
import random
from datetime import date, timedelta
from decimal import Decimal

#Fixed range so same seed gives same output
START, END = date(2024, 1, 1), date(2026, 10, 31)

# column names; consistent with schema design
COLS = ["transaction_id", "transaction_date", "type", "amount", "currency",
        "category", "description", "counterparty", "payment_method"]

# Category values: (weight, min amount, max amount, description)
CATEGORIES = {
    "product_sales": (35, 25, 2500, ["Starter kit order", "Bulk order", "Accessory order"]),
    "services": (25, 300, 5000, ["Consulting invoice", "Website build", "Training session"]),
    "subscriptions": (30, 19, 199, ["Monthly plan", "Annual plan", "Premium plan"]),
    "other_revenue": (10, 20, 500, ["Referral bonus", "Interest income", "Refund received"])
}
COUNTERPARTIES = ["Acme Corp", "Brightside LLC", "Maple Retail", "Northwind Co",
                  "Cedar Supply", "Lakeview Dental", "Redwood Studio", ""]

PAYMENT_METHODS = ["card", "bank_transfer", "check", "cash", "other", ""]

# Code to generate synthetic revenue data
def generate_revenue(n, seed):
    rng = random.Random(seed)
    names = list(CATEGORIES)
    weights = [CATEGORIES[c][0] for c in names]
    days = (END -START).days
    rows, seen = [], set()
    while len(rows) < n:
        category = rng.choices(names, weights=weights)[0]
        _, lo, hi, descriptions = CATEGORIES[category]
        row = {
            "transaction_date": (START + timedelta(days=rng.randint(0, days))).isoformat(),
            "type": "revenue",
            "amount": str((Decimal(rng.randint(lo * 100, hi * 100)) / 100).quantize(Decimal("0.01"))),
            "currency": "USD",
            "category": category,
            "description": rng.choice(descriptions),
            "counterparty": rng.choice(COUNTERPARTIES),
            "payment_method": rng.choice(PAYMENT_METHODS)
        }
        # duplicate key from schema
        key = (row["transaction_date"], row["type"], row["category"],
               row["amount"], row["currency"], row["counterparty"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
    rows.sort(key=lambda r: r["transaction_date"])
    for i, r in enumerate(rows, start=1):
        r["transaction_id"] = f"REV-{i:06d}"
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic revenue transactions.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--out", default="revenue_records.csv")
    args = parser.parse_args()

    rows = generate_revenue(args.count, args.seed)
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} revenue records to {args.out} (seed={args.seed})")