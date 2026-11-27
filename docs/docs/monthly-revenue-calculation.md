# Monthly Revenue Calculation (OFL-030)

## Purpose

This document explains how OpenFinanceLab calculates monthly revenue for the first release.

## Calculation rules

Monthly revenue is the total amount of all accepted, valid revenue transactions for the selected calendar month.

A transaction is included when:

- Its `type` is `revenue`.
- Its `transaction_date` falls within the selected month and year.
- Its `category` is one of the allowed revenue categories: `product_sales`, `services`, `subscriptions`, or `other_revenue`.
- Its `amount` is greater than zero and has no more than two decimal places.
- It meets the other validation rules in the transaction schema.

Expense transactions and transactions from other months are not included.

**Formula:**

Monthly revenue = Sum of all valid revenue transaction amounts for the selected month

Amounts should be calculated using exact decimal values and displayed in USD with two decimal places. If there are no qualifying revenue transactions for the selected month, the monthly total is $0.00.

## Refunds, negative amounts, and duplicates

The current transaction schema does not allow negative or zero amounts. It does not define how refunds should be recorded or deducted from revenue. The team needs to agree on a refund or adjustment approach before net revenue after refunds can be calculated.

The schema defines how to identify duplicate transactions, but it does not specify whether flagged duplicates should be excluded from reports. The team needs to agree on how duplicate review affects the accepted transactions used in calculations.

## Worked example

The following transactions are available:

| Transaction ID | Date | Type | Category | Amount |
|---|---|---|---|---:|
| REV-000001 | 2026-03-05 | revenue | product_sales | $1,200.00 |
| REV-000002 | 2026-03-14 | revenue | services | $850.00 |
| REV-000003 | 2026-03-20 | revenue | subscriptions | $125.00 |
| EXP-000001 | 2026-03-25 | expense | rent | $600.00 |
| REV-000004 | 2026-04-02 | revenue | product_sales | $500.00 |

For March 2026, the first three transactions are included. The rent transaction is excluded because it is an expense, and REV-000004 is excluded because it occurred in April.

March 2026 revenue = $1,200.00 + $850.00 + $125.00

**Expected result: $2,175.00**
