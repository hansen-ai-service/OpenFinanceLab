1. Upload success - Every valid sample CSV file should upload successfully (target: 100%). We will verify this by uploading all provided sample files and confirming that each one loads.

2. Detection of data errors. -  The platform should find every planted error, including duplicates, missing categories, and invalid dates (target: 100%). We will verify this by seeding a test file with a known number of each error type and comparing what the platform detects with what we planted.

3. Row reconciliation - The number of rows read should equal the number accepted plus the number rejected (target: exact match). We will verify this by comparing the data-quality summary counts with the known row count of the test file.

4. Accuracy of monthly figures -  Monthly revenue, expenses, and net cash flow should be correct (target: $0.00 difference). We will verify this by calculating the same figures independently in a spreadsheet and comparing them with the app's output.

5. Category totals - The expense category totals should add up to the total expenses (target: exact match). We will verify this by summing the category totals and comparing the result with total expenses.

6. Data-quality summary first - The data-quality summary should appear before any financial results (target: 100% of uploads). We will verify this by walking through the upload flow and confirming the order.

7. Invalid file handling - Empty or malformed files should produce a clear error message and should not crash the app. We will verify this by uploading deliberately broken files.

8. Speed -  The monthly summary should be produced in under 5 seconds on the sample dataset. We will verify this by timing the request on the sample data.

9. Setup time - A new contributor should be able to set up the project from the documentation in under 30 minutes. We will verify this by having a new team member follow the setup document while another member times the process and notes any blockers.
