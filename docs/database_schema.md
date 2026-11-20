# Database Schema Design

## 1. Overview

The first release will use PostgreSQL with two tables: `transactions` and `categories`.

The design supports storing transactions, validating category assignments, detecting duplicates, and calculating monthly financial summaries.

## 2. Tables

### `categories`

Stores the predefined transaction categories.

| Column | Type | Constraints |
|---|---|---|
| `id` | SMALLINT | Primary key |
| `name` | VARCHAR(50) | Not null, unique |
| `type` | VARCHAR(10) | Not null, `revenue` or `expense` |

Categories will be populated using the list defined in OFL-009.

### `transactions`

Stores imported financial transactions.

| Column | Type | Constraints |
|---|---|---|
| `id` | UUID | Primary key |
| `transaction_id` | VARCHAR(64) | Not null, unique |
| `transaction_date` | DATE | Not null |
| `type` | VARCHAR(10) | Not null, `revenue` or `expense` |
| `amount` | NUMERIC(14,2) | Not null, greater than 0 |
| `currency` | CHAR(3) | Not null, `USD` only |
| `category_id` | SMALLINT | Not null, foreign key |
| `description` | VARCHAR(255) | Nullable |
| `counterparty` | VARCHAR(100) | Nullable |
| `payment_method` | VARCHAR(20) | Nullable, must match OFL-009 options |

`id` is the internal database identifier. `transaction_id` is the identifier provided by the CSV.

## 3. Relationships and Constraints

- Each transaction references one category.
- A category can be used by multiple transactions.
- A transaction's type must match its category's type. This will be enforced with a composite foreign key.
- Transaction IDs must be unique.
- Amounts must be positive and use no more than two decimal places.
- Required fields cannot be null.
- Payment methods and transaction types must use the values defined in OFL-009.

CSV formatting, future transaction dates, whitespace trimming, and duplicate detection will be handled during application validation.

Duplicate transactions are identified using the fields defined in OFL-009, excluding `transaction_id`.

## 4. Financial Calculations

Monthly summaries will be calculated from the `transactions` table:

- **Revenue:** Sum of revenue transactions.
- **Expenses:** Sum of expense transactions.
- **Net cash flow:** Revenue minus expenses.

## 5. Scalability and Deferred Work

The two-table design keeps category definitions separate from transaction records and uses database constraints to maintain data integrity. Additional tables can be introduced as requirements grow.

The following are outside the initial scope:

| Table or feature | Reason for deferral |
|---|---|
| `uploads` | Upload history and import tracking |
| `users` | Multi-user access |
| `datasets` | Supporting multiple businesses |
| `data_quality_issues` | Persisting validation issues |
| `import_rows` | Storing individual imported CSV rows |
| `monthly_summaries` | Monthly totals can be calculated from transactions |
| `accounts` | Supporting multiple financial accounts |

For the first release, the database will use only `transactions` and `categories`.