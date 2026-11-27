# Dashboard Layout (OFL-049)

## Purpose

This wireframe shows the proposed layout for the first version of the
OpenFinanceLab dashboard. It focuses on data quality, monthly financial
metrics, trends, expense categories, and budget comparisons.

## Screen 1: Upload and Data-Quality Review

| OpenFinanceLab | |
|---|---|
| **Upload your financial data** | [ Choose file ] [ Upload ] |
| **Data-quality summary** | Rows reviewed: — · Accepted: — · Rejected: — |
| **Issues found** | Possible duplicates: — · Missing categories: — · Invalid dates: — |
| **Review** | [ View issues ] [ Review and Continue to dashboard ] |

The data-quality summary appears before financial results so the user can
review issues in the uploaded data.

## Screen 2: Financial Dashboard

| OpenFinanceLab | | |
|---|---|---|
| **Financial Dashboard** | | **Select month:** [ Month ▼ ] |
| **Total Revenue** | **Total Expenses** | **Net Cash Flow** |
| $— | $— | $— |
| **Monthly Financial Trends** | | **Expenses by Category** |
| Chart comparing revenue, expenses, and net cash flow across months | | Chart showing spending by category |
| **Budget vs. Actual Spending** | | |
| Category · Budget · Actual · Difference · Status | | [ View details ] |
| **Recent Transactions** | | |
| Date · Type · Category · Description · Amount | | [ View all ] |
| **Data-quality status** | | [ View summary ] |

If budget data is unavailable, the budget section displays: “Upload budget data to see this comparison.” 

Earlier we discussed budget comparison as part of the first release, but if the team has since decided it belongs in version 2, remove it from the main v1 dashboard sketch and add a note such as:
Budget comparison is a possible feature for a future release. Its release timing should be confirmed with the team.

## Notes

- The monthly financial cards show revenue, expenses, and net cash flow.
- The trend chart helps users compare financial performance across months.
- The expense chart helps users see which categories cost the most.
- The budget section helps users identify categories over or under budget.
- The user can return to the data-quality summary from the dashboard.
- Net cash flow is labeled separately from profit or loss because they are
  not necessarily the same.
