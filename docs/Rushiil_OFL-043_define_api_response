OFL-043: API Response Specification

This document defines the JSON responses returned by the OpenFinanceLab backend API for the first release. It covers two responses, the monthly metrics (for OFL-045) and the overall summary (for OFL-044), plus a shared error format that OFL-046 can reuse. Each field is documented with its name, data type, description, and whether it is required.

Conventions:

1. Money is returned as decimal strings with two decimal places (for example "12500.00") to avoid floating-point rounding errors, which follows the architecture doc.
2. Months use the YYYY-MM format (for example "2026-01"), dates use YYYY-MM-DD, and field names use snake_case.
3. Revenue, expenses, and refunds are all positive numbers.
4. Net cash flow equals revenue minus expenses minus refunds, and it can be negative.
5. Refunds are reported in a separate field (total_refunds) so there is no confusion. They are not netted into revenue or expenses.
6. The first release supports USD only. The currency field is still included so other currencies can be added later.
7. Empty months are included with zero values and a transaction count of 0, so charts have no gaps.
8. If there is no data at all, the API returns HTTP 200 with empty or zero values, not an error.
9. Category breakdowns are not part of these responses and will be added later.
10. A refund is counted in the month it was issued (the date of the refund record), not the month of the original sale.
11. Transaction dates are calendar dates (YYYY-MM-DD) with no timezone. Any timestamp the API returns is in UTC. A transaction belongs to the month of its date as recorded.
12. Every month in the requested range is returned. Months with no data, including months before the first or after the last transaction, are zero-filled (all amounts "0.00" and transaction_count 0).

Response 1: Monthly metrics (for OFL-045)

Request: GET /api/v1/metrics/monthly, with optional start_month and end_month (both YYYY-MM, both inclusive).
Defaults and rules for start_month and end_month:
1. If start_month is missing, it defaults to the first month that has data.
2. If end_month is missing, it defaults to the last month that has data.
3. If both are missing, the full range of the data is returned.
4. If there is no data at all and no range is given, the months list is empty.
5. If a range is given that extends past the data, every month in that range is returned, with zero-filled months where there is no data. The start_month and end_month in the response match the requested range.
6. If start_month is later than end_month, the API returns a 400 error.

Top-level fields:
1. currency (string, required): the currency code, always "USD" for now.
2. start_month (string or null, required): the first month in the response, which is the requested start or the first month with data. Null if there is no data and no range was requested.
3. end_month (string or null, required): the last month in the response, which is the requested end or the last month with data. Null if there is no data and no range was requested.
4. months (list, required): one entry per month in order. Empty if there is no data.

Fields in each month entry:
1. month (string, required): the month in YYYY-MM format.
2. total_revenue (decimal string, required): revenue for the month, not including refunds.
3. total_expenses (decimal string, required): expenses for the month.
4. total_refunds (decimal string, required): refunds for the month.
5. net_cash_flow (decimal string, required): revenue minus expenses minus refunds. Can be negative.
6. transaction_count (integer, required): number of transactions in the month, including refunds.

Example: for January 2026, total_revenue is "12500.00", total_expenses is "9800.50", total_refunds is "300.00", net_cash_flow is "2399.50", and transaction_count is 142. A month with no transactions shows "0.00" for every amount and 0 for transaction_count.

Response 2: Summary (for OFL-044)

Request: GET /api/v1/summary

Fields:
1. currency (string, required): the currency code, always "USD" for now.
2. first_transaction_date (date string or null, required): the earliest transaction date. Null if there is no data.
3. last_transaction_date (date string or null, required): the latest transaction date. Null if there is no data.
4. total_transactions (integer, required): total number of transactions, including refunds.
5. total_revenue (decimal string, required): all revenue, not including refunds.
6. total_expenses (decimal string, required): all expenses.
7. total_refunds (decimal string, required): all refunds.
8. net_cash_flow (decimal string, required): revenue minus expenses minus refunds. Can be negative.

Example: total_revenue "38100.00", total_expenses "31250.75", total_refunds "850.00", net_cash_flow "5999.25", total_transactions 410, from 2026-01-02 to 2026-03-30. When there is no data, the dates are null, total_transactions is 0, and all amounts are "0.00".

Error response (shared with OFL-046)

Every error uses the same format: an error object with three fields.
1. code (string, required): a short machine-readable code, for example "invalid_parameter".
2. message (string, required): a human-readable explanation, for example "start_month must be in YYYY-MM format."
3. field (string or null, optional): the input field that caused the error.

Example error response:
{
  "error": {
    "code": "invalid_parameter",
    "message": "start_month must be in YYYY-MM format.",
    "field": "start_month"
  }
}

Another example, for a range where start_month is later than end_month:
{
  "error": {
    "code": "invalid_range",
    "message": "start_month must not be later than end_month.",
    "field": "start_month"
  }
}

HTTP status codes: 200 for a successful request (including when there is no data), 400 for invalid input such as a badly formatted month, 404 when the requested item does not exist, and 500 for an unexpected server error.

Dependencies:

The sign convention, the net cash flow formula, and empty-month handling depend on OFL-030, OFL-032, OFL-034, and OFL-036. This spec will be updated if those change. The refund handling also assumes the data fields (OFL-007) can identify which records are refunds.

Decisions on the team questions:

1. Should the first release support only USD? Yes, USD only for simplicity.
2. Should refunds be netted into revenue and expenses? No, refunds are reported in a separate field so there is no confusion.
3. Should category breakdowns be part of this response? No, they will be implemented later.
