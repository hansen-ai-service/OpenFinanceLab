"""Generate synthetic expense transactions (OFL-012).

Follows the transaction schema (OFL-009) and uses the shared helpers in common.py,
so the output matches the revenue generator (OFL-011).

Example:
    python generate_expenses.py --seed 42 --count 100 --out expense_records.csv
"""

import argparse
import random

from common import (CATEGORIES_BY_TYPE, PAYMENT_METHODS, assign_ids,
                    duplicate_key, random_amount, random_date, validate_rows,
                    write_csv)

# Category values: (weight, min amount, max amount, descriptions)
# A higher weight means the category shows up more often.
# Amount ranges are the same as the OFL-010 sample dataset.
CATEGORIES = {
    "payroll": (10, 400, 1500, ["Payroll run"]),
    "rent": (8, 1200, 1800, ["Office rent"]),
    "software": (22, 10, 200, ["Project tool license", "Cloud hosting"]),
    "marketing": (18, 50, 800, ["Online ads", "Newsletter tool"]),
    "supplies": (17, 20, 300, ["Office supplies"]),
    "utilities": (15, 40, 250, ["Internet service", "Electricity"]),
    "other_expense": (10, 10, 200, ["Bank fees", "Misc expense"]),
}

# Vendors for each category. An empty string means no vendor is recorded.
VENDORS = {
    "payroll": ["Granite Payroll"],
    "rent": ["Summit Properties"],
    "software": ["Notion", "CloudNest"],
    "marketing": ["AdReach", "MailBridge"],
    "supplies": ["Paper Depot", ""],
    "utilities": ["Beehive Telecom", "Valley Power"],
    "other_expense": ["First Valley Bank", ""],
}

# Make sure the categories here match the schema
assert set(CATEGORIES) == set(CATEGORIES_BY_TYPE["expense"])
assert set(VENDORS) == set(CATEGORIES_BY_TYPE["expense"])


# Code to generate synthetic expense data
def generate_expenses(n, seed):
    rng = random.Random(seed)
    names = list(CATEGORIES)
    weights = [CATEGORIES[c][0] for c in names]
    rows, seen = [], set()

    while len(rows) < n:
        category = rng.choices(names, weights=weights)[0]
        _, lo, hi, descriptions = CATEGORIES[category]
        row = {
            "transaction_id": "",  # filled in after sorting
            "transaction_date": random_date(rng),
            "type": "expense",
            "amount": random_amount(rng, lo, hi),
            "currency": "USD",
            "category": category,
            "description": rng.choice(descriptions),
            "counterparty": rng.choice(VENDORS[category]),
            "payment_method": rng.choice(PAYMENT_METHODS + [""]),  # empty = not recorded
        }
        # skip duplicates, using the definition from the schema
        key = duplicate_key(row)
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)

    # sort by date and give IDs such as EXP-000001
    return assign_ids(rows, "expense")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic expense transactions.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--out", default="expense_records.csv")
    args = parser.parse_args()

    rows = generate_expenses(args.count, args.seed)
    validate_rows(rows)  # stops with a clear message if any row breaks the schema
    write_csv(rows, args.out)
    print(f"Wrote {len(rows)} expense records to {args.out} (seed={args.seed})")