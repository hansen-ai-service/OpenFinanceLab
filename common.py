"""Shared helpers for the synthetic data generators (OFL-011 revenue, OFL-012 expenses).

Everything here follows the transaction schema in docs/transaction-schema.md (OFL-009),
so every generator produces the same columns, ID format, and duplicate rules.
"""

import csv
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

# Fixed column order from the schema (section 6).
COLUMNS = [
    "transaction_id", "transaction_date", "type", "amount", "currency",
    "category", "description", "counterparty", "payment_method",
]

# Allowed categories for each transaction type (schema section 3).
CATEGORIES_BY_TYPE = {
    "revenue": ["product_sales", "services", "subscriptions", "other_revenue"],
    "expense": ["payroll", "rent", "software", "marketing", "supplies",
                "utilities", "other_expense"],
}

PAYMENT_METHODS = ["card", "bank_transfer", "cash", "check", "other"]
CURRENCY = "USD"  # USD only for the first version

# ID prefix for each type, e.g. EXP-000001.
ID_PREFIXES = {"revenue": "REV", "expense": "EXP"}

# Shared date range, so revenue and expenses cover the same months.
# It is fixed (not based on today's date), so the same seed gives the same output.
START_DATE = date(2024, 1, 1)
END_DATE = date(2026, 10, 31)


def random_date(rng, start=START_DATE, end=END_DATE):
    """Return a random date between start and end (both included) as YYYY-MM-DD."""
    days = (end - start).days
    return (start + timedelta(days=rng.randint(0, days))).isoformat()


def random_amount(rng, low, high):
    """Return a random amount between low and high as a string with 2 decimals."""
    cents = rng.randint(int(low * 100), int(high * 100))
    return str((Decimal(cents) / 100).quantize(Decimal("0.01")))


def make_id(kind, number):
    """Build an ID such as EXP-000001 from the type ('expense') and a number."""
    return f"{ID_PREFIXES[kind]}-{number:06d}"


def duplicate_key(row):
    """Fields that define a duplicate (schema section 5).

    Two rows with the same key are duplicates, even if transaction_id differs.
    A missing counterparty counts as an empty string.
    """
    return (
        row["transaction_date"], row["type"], row["category"],
        row["amount"], row["currency"], row.get("counterparty") or "",
    )


def assign_ids(rows, kind):
    """Sort rows by date and give each one an ID (EXP-000001, EXP-000002, ...)."""
    rows.sort(key=lambda r: r["transaction_date"])
    for number, row in enumerate(rows, start=1):
        row["transaction_id"] = make_id(kind, number)
    return rows


def validate_row(row, today=None):
    """Check one row against the schema rules. Returns a list of problems (empty if valid)."""
    today = today or date.today()
    problems = []

    if set(row) != set(COLUMNS):
        return [f"columns do not match the schema: {sorted(set(row) ^ set(COLUMNS))}"]

    # transaction_id: 1 to 64 characters
    if not 1 <= len(row["transaction_id"]) <= 64:
        problems.append("transaction_id must be 1 to 64 characters")

    # transaction_date: YYYY-MM-DD and not in the future
    try:
        parsed = date.fromisoformat(row["transaction_date"])
        if len(row["transaction_date"]) != 10:
            problems.append("transaction_date must use the YYYY-MM-DD format")
        elif parsed > today:
            problems.append("transaction_date must not be in the future")
    except ValueError:
        problems.append("transaction_date must use the YYYY-MM-DD format")

    # type and category must match
    if row["type"] not in CATEGORIES_BY_TYPE:
        problems.append("type must be revenue or expense")
    elif row["category"] not in CATEGORIES_BY_TYPE[row["type"]]:
        problems.append(f"category '{row['category']}' is not valid for type '{row['type']}'")

    # amount: greater than 0, at most 2 decimal places
    try:
        amount = Decimal(row["amount"])
        if not amount > 0:
            problems.append("amount must be greater than 0")
        elif amount.as_tuple().exponent < -2:
            problems.append("amount must have at most 2 decimal places")
    except (InvalidOperation, TypeError):
        problems.append("amount must be a number")

    if row["currency"] != CURRENCY:
        problems.append("currency must be USD")

    # Optional fields: trimmed text with length limits, valid payment method
    for field, limit in (("description", 255), ("counterparty", 100)):
        value = row[field] or ""
        if value != value.strip():
            problems.append(f"{field} must not have leading or trailing spaces")
        if len(value) > limit:
            problems.append(f"{field} must be at most {limit} characters")
    if row["payment_method"] and row["payment_method"] not in PAYMENT_METHODS:
        problems.append("payment_method is not an allowed value")

    return problems


def validate_rows(rows, today=None):
    """Validate every row, plus unique IDs and no duplicates. Raises ValueError if anything is wrong."""
    problems = []
    seen_ids, seen_keys = set(), set()

    for number, row in enumerate(rows, start=1):
        for problem in validate_row(row, today):
            problems.append(f"row {number}: {problem}")
        if row.get("transaction_id") in seen_ids:
            problems.append(f"row {number}: duplicate transaction_id {row['transaction_id']}")
        seen_ids.add(row.get("transaction_id"))
        if not validate_row(row, today):
            key = duplicate_key(row)
            if key in seen_keys:
                problems.append(f"row {number}: duplicate record (same date, type, category, "
                                f"amount, currency, and counterparty)")
            seen_keys.add(key)

    if problems:
        shown = "\n".join(problems[:20])
        extra = f"\n...and {len(problems) - 20} more" if len(problems) > 20 else ""
        raise ValueError(f"{len(problems)} problem(s) found:\n{shown}{extra}")


def write_csv(rows, path):
    """Write the rows to a CSV file using the schema's fixed column order."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
