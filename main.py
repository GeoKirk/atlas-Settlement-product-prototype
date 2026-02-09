"""
Atlas Settlement – Fintech Settlement Operations Prototype

This script generates a mock settlement operations dashboard for a fintech
lending / factoring business.

Key capabilities:
- Client payout aggregation and status tracking
- Rolling reserve and partner RR calculations
- Credit limit monitoring
- Portfolio repayment and interest projections
- HTML dashboard output for operational review

This prototype is designed for product discovery, stakeholder demos – not for production use.
"""

import pandas as pd
from tabulate import tabulate
import webbrowser
import os

# Business Parameters
INTEREST_RATE = 0.07
CREDIT_LIMIT = 250000  # New Credit Limit

# Visual Parameters
status_column_width = 150  # Width of the "Status" column in pixels
summary_table_width = '80%'  # Width of the "Merchant Payout Summary" table

# --- RE-DEFINING SOURCE FILE PATHS ---

# 1. Your main source Excel file
#    It's called "Merchant_Data" and is in the same folder.
#    *** IMPORTANT: CONFIRM THE FILE EXTENSION (.xlsx or .xls) ***
file_path = os.path.join('example_data', 'Merchant_Data.xlsx') # Assuming .xlsx

# 2. Your logo file
logo_path = 'my_company_logo.png' # <--- UPDATE THIS WITH YOUR LOGO FILENAME

# 3. Where the HTML report will be saved
html_file_path = 'BackofficeReport.html'

# 4. Where the summary Excel file will be saved
output_file_path = 'MerchantPayoutSummary.xlsx'

# --- END OF RE-DEFINING SOURCE FILE PATHS ---


# Check if the logo file exists
if not os.path.exists(logo_path):
    print(f"Logo file not found at: {os.path.abspath(logo_path)}")
    logo_html = '<p>Logo not found</p>'
else:
    logo_html = f'<img src="{logo_path}" alt="Logo">'

try:
    df = pd.read_excel(file_path)
    print(f"Successfully loaded Excel file from: {os.path.abspath(file_path)}")
except Exception as e:
    print(f"Error reading the Excel file '{file_path}': {e}")
    print("Please ensure the Excel file exists in the same directory as the script and the filename is correct.")
    exit()

# Add a 'Status' column with default values (modify this as needed)
df['Status'] = 'Ready'

# --- FIX FOR COLUMN MAPPING ---
# Summarize the payout amounts using the actual column names from your Excel file
summary = df.groupby(['Vertrieb_ID', 'Vertrieb_Name', 'Status']).agg({
    'Barzahlungspreis': 'sum',
    'Broker_Payout' : 'sum',           # Merchant_Payout
    'Marge_CY': 'sum',                 # <--- CHANGED FROM 'Marge' to 'Marge_CY'
    'Sicherheitseinbehalt': 'sum',
    'Sicherheitensatz': 'mean'
}).reset_index()

# Rename the columns for the summary DataFrame
# The order here must match the order of columns produced by the .agg() method
summary.columns = [
    'Merchant ID',       # Corresponds to Vertrieb_ID
    'Merchant Name',     # Corresponds to Vertrieb_Name
    'Status',          # Corresponds to Status
    'Receivables',     # Corresponds to Barzahlungspreis
    'Merchant_Payout',   # Corresponds to Broker Payout
    'Partner_Payout',  # Corresponds to Marge_CY
    'Merchant_RR',       # Corresponds to Sicherheitseinbehalt
    'Merchant_RR_%'      # Corresponds to Sicherheitensatz
]
# --- END FIX FOR COLUMN MAPPING ---


# Calculate the new column 'Partner_RR' with the logic Receivables * Merchant_RR_% - Merchant_RR
summary['Partner_RR'] = summary.apply(lambda row: (row['Receivables'] * row['Merchant_RR_%']) - row['Merchant_RR'], axis=1)


# Format the columns to display values in euros
for col in ['Receivables', 'Partner_Payout', 'Merchant_RR', 'Merchant_Payout', 'Partner_RR']:
    summary[col] = summary[col].apply(lambda x: f"€{x:,.0f}")

# Format the 'Merchant_RR_%' column to display as a percentage with 0 decimal places
summary['Merchant_RR_%'] = summary['Merchant_RR_%'].apply(lambda x: f"{x * 100:.0f}%" if pd.notnull(x) else x)

# Calculate totals for each column except 'Merchant_RR_%'
totals = summary[['Receivables', 'Merchant_Payout', 'Merchant_RR', 'Partner_Payout', 'Partner_RR']].replace('[€,]', '', regex=True).astype(float).sum()

# Reorder columns to move 'Merchant_RR_%' to the end
summary = summary[['Merchant ID', 'Merchant Name', 'Status', 'Receivables', 'Merchant_Payout', 'Merchant_RR', 'Partner_Payout' , 'Partner_RR', 'Merchant_RR_%']]

# Append the totals row to the summary DataFrame
totals_row = pd.DataFrame([['Total', '', '', f"€{totals['Receivables']:,.0f}", f"€{totals['Partner_Payout']:,.0f}", f"€{totals['Merchant_RR']:,.0f}", f"€{totals['Merchant_Payout']:,.0f}", f"€{totals['Partner_RR']:,.0f}", '']], columns=summary.columns)
summary = pd.concat([summary, totals_row], ignore_index=True)

# Convert the summary DataFrame to an HTML table with formatting
summary_html = tabulate(summary, headers='keys', tablefmt='html', showindex=False, numalign="center", stralign="left", colalign=("left", "center", "center", "center", "center", "center", "center", "center", "center"))

# Add CSS styles for formatting
summary_html = summary_html.replace('<table>', f'<table class="summary-table" style="font-family: Arial; border-collapse: collapse; width: {summary_table_width};">')
summary_html = summary_html.replace('<th>Status', f'<th style="width: {status_column_width}px;">Status')
summary_html = summary_html.replace('<td>Ready', f'<td class="status-cell" style="width: {status_column_width}px;">Ready')
summary_html = summary_html.replace('<th>', '<th style="padding: 8px; text-align: center; border: 1px solid #ddd;">')
summary_html = summary_html.replace('<td>', '<td style="padding: 8px; text-align: center; border: 1px solid #ddd;">')
summary_html = summary_html.replace('<tr>', '<tr style="border-bottom: 1px solid #ddd;">')
summary_html = summary_html.replace('<tr><td>Total', '<tr style="font-weight: bold;"><td>Total')

# Add links to Merchant IDs in the summary table
for Merchant_id in summary['Merchant ID'].unique():
    if Merchant_id != 'Total':
        summary_html = summary_html.replace(f'<td>{Merchant_id}</td>', f'<td><a href="#Merchant_{Merchant_id}">{Merchant_id}</a></td>')

# Create account boxes per Merchant with subaccounts
account_boxes_html = ""
for _, row in summary.iterrows():
    if row['Merchant Name'] == 'Total':
        continue
    Merchant_name = row['Merchant Name']
    Merchant_id = row['Merchant ID']

    factoring = float(row['Receivables'].replace('€', '').replace(',', ''))
    settlement = float(row['Merchant_Payout'].replace('€', '').replace(',', ''))
    rolling_reserve = float(row['Merchant_RR'].replace('€', '').replace(',', ''))
    Partner_rr = float(row['Partner_RR'].replace('€', '').replace(',', ''))

    sicherheitensatz = row['Merchant_RR_%']

    # Calculate Rolling Reserve Rate and percentage
    rolling_reserve_rate = rolling_reserve / factoring if factoring != 0 else 0
    rolling_reserve_percentage = rolling_reserve_rate * 100

    # Calculate Credit Limit Ratio
    CREDIT_LIMIT_ratio = factoring / CREDIT_LIMIT if CREDIT_LIMIT != 0 else 0

    account_box = pd.DataFrame({
        'Subaccount': ['Factoring', 'Settlement', 'Rolling Reserve', 'Rolling Reserve Rate', 'Partner_RR', 'Merchant_RR_%', 'Credit Limit', 'Credit Limit Ratio'],
        'Amount': [factoring, settlement, rolling_reserve, f"{rolling_reserve_percentage:.2f}%", Partner_rr, sicherheitensatz, f"€{CREDIT_LIMIT:,.0f}", f"{CREDIT_LIMIT_ratio * 100:.2f}%"]
    })
    account_box['Amount'] = account_box['Amount'].apply(lambda x: f"€{x:,.0f}" if isinstance(x, (int, float)) and not isinstance(x, str) else x)
    account_box_str = tabulate(account_box, headers='keys', tablefmt='html', showindex=False, numalign="center", stralign="left", colalign=("left", "center"))
    account_boxes_html += f'<a name="Merchant_{Merchant_id}"></a><h2>Merchant: {Merchant_name} (ID: {Merchant_id})</h2>{account_box_str}<br>'

# Calculate the Portfolio Repayment Schedule
sum_of_receivables = totals['Receivables']
periods = 60
principal = sum_of_receivables / periods

# Create the repayment schedule DataFrame
repayment_schedule = pd.DataFrame({
    'Period': range(1, periods + 1),
    'Principal': [principal] * periods,
    'Outstanding': [sum_of_receivables - principal * i for i in range(1, periods + 1)]
})

# Calculate the Expected Interest for each period
repayment_schedule['Expected Interest'] = repayment_schedule['Outstanding'].apply(lambda x: x * INTEREST_RATE / 12)

# Calculate totals for the repayment schedule
totals_principal = repayment_schedule['Principal'].sum()
totals_outstanding = repayment_schedule['Outstanding'].iloc[-1]
totals_interest = repayment_schedule['Expected Interest'].sum()

# Append the totals row to the repayment schedule DataFrame
totals_row = pd.DataFrame([['Total', totals_principal, totals_outstanding, totals_interest]], columns=repayment_schedule.columns)
repayment_schedule = pd.concat([repayment_schedule, totals_row], ignore_index=True)

# Format the 'Principal' and 'Outstanding' columns to display values in euros without decimals
repayment_schedule['Principal'] = repayment_schedule['Principal'].apply(lambda x: f"€{x:,.0f}")
repayment_schedule['Outstanding'] = repayment_schedule['Outstanding'].apply(lambda x: f"€{x:,.0f}")
repayment_schedule['Expected Interest'] = repayment_schedule['Expected Interest'].apply(lambda x: f"€{x:,.0f}")

# Convert the repayment schedule DataFrame to an HTML table
repayment_schedule_html = tabulate(repayment_schedule, headers='keys', tablefmt='html', showindex=False, numalign="center", stralign="left", colalign=("center", "center", "center", "center"))

# Combine all HTML tables into a single HTML file
html_content = f"""

<html>

<head>

    <title>Atlas Settlement Tool</title>

    <style>

        body {{

            font-family: Arial;

        }}

        table {{

            font-family: Arial;

            border-collapse: collapse;

            width: 50%;

        }}

        .summary-table {{

            width: {summary_table_width};

        }}

        th, td {{

            padding: 8px;

            text-align: center;

            border: 1px solid #ddd;

        }}

        tr {{

            border-bottom: 1px solid #ddd;

        }}

        tr:nth-child(even) {{

            background-color: #f2f2f2;

        }}

        tr:hover {{

            background-color: #ddd;

        }}

        tr.total {{

            font-weight: bold;

        }}

        .header {{

            display: flex;

            justify-content: flex-end;

            align-items: center;

        }}

        .header img {{

            max-height: 100px;

        }}

        .execute-button {{

            display: block;

            margin: 20px auto;

            padding: 10px 20px;

            font-size: 16px;

            background-color: #4CAF50;

            color: white;

            border: none;

            border-radius: 5px;

            cursor: pointer;

        }}

        .execute-button:hover {{

            background-color: #45a049;

        }}

    </style>

    <script>

        function executePayouts() {{

            var statusCells = document.getElementsByClassName('status-cell');

            for (var i = 0; i < statusCells.length; i++) {{

                if (statusCells[i].innerText === 'Ready') {{

                    statusCells[i].innerText = 'Requested';

                }}

            }}

            alert('Payout Executed (Pain001)');

        }}

    </script>

</head>

<body>

    <div class="header">

        {logo_html}

    </div>

    <h1> Atlas Settlement Tool </h1>

    <h2>Merchant Payout Summary</h2>

    {summary_html}

    <button class="execute-button" onclick="executePayouts()">Execute Payouts</button>

    <h2>Merchant SubAccounts</h2>

    {account_boxes_html}

    <h2>Portfolio Repayment Schedule</h2>

    {repayment_schedule_html}

</body>

</html>

"""

# Save the combined HTML content to a file
with open(html_file_path, 'w') as f:
    f.write(html_content)

# Open the HTML file in the default web browser
webbrowser.open('file://' + os.path.realpath(html_file_path))

# Save the summary to a new Excel file
try:
    summary.to_excel(output_file_path, index=False)
    print(f"Summary saved to {os.path.abspath(output_file_path)}")
except Exception as e:
    print(f"Error saving the Excel file: {e}")

