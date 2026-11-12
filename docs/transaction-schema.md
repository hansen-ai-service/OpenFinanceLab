transaction-schema.md

# Transaction Schema (OFL-009)

## 1. Purpose

- This document defines what one transaction entry looks like so data generation, ingestion, storage, calculations, and the API all use the same structure.

## 2. Fields

| Field | Type | Required | Meaning | Validation |
|---|---|---|---|---|
| transaction_id | string | Yes | Unique label for the transaction | 1-64 characters, unique across the dataset |
| transaction_date | date | Yes | When the transaction happened | Format YYYY-MM-DD, not in the future |
| type | enum | Yes | Direction of money | `revenue` or `expense` |
| amount | decimal | Yes | Value of the transaction | Greater than 0, at most 2 decimal places |
| currency | string | Yes | Currency code | `USD` only for v1 |
| category | enum | Yes | What kind of transaction it is | Must be in the category list and match `type` |
| description | string | No | Short note | Up to 255 characters |
| counterparty | string | No | Customer (revenue) or vendor (expense) | Up to 100 characters |
| payment_method | enum | No | How it was paid | `card`, `bank_transfer`, `cash`, `check`, `other` |

## 3. Categories

- **Revenue:** product_sales, services, subscriptions, other_revenue
- **Expense:** payroll, rent, software, marketing, supplies, utilities, other_expense


## 4. Validation Rules

1. Amount is always positive. The `type` field says whether it is money in or out.
2. Category must belong to the transaction's type (a revenue cannot have category `rent`).
3. Leading and trailing whitespace is trimmed from all text fields.
4. Empty optional fields are treated as null.
5. Files with missing required columns are rejected.
6. Files with unknown columns are rejected.

## 5. Duplicate Definition

- Two transactions are duplicates if these fields all match, even if `transaction_id` differs:
`transaction_date`, `type`, `category`, `amount`, `currency`, `counterparty`

- An empty counterparty is treated as empty string, so two rows with no counterparty can still match.

## 6. CSV Format

Column order is fixed:

```
transaction_id, transaction_date, type, amount, currency, category, description, counterparty, payment_method
```

Example data:

```
REV-000001, 2026-03-14, revenue, 1250.00, USD, services, Consulting invoice, Acme Corp, bank_transfer
EXP-000001, 2026-03-15, expense, 89.99, USD, software, Monthly SaaS license, Notion, card
```