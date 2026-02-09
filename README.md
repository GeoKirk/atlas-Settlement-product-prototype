# Atlas Settlement – Fintech Operations Product Prototype

## Dashboard Preview
![Atlas Settlement Dashboard](docs/dashboard_overview.png)


## Repository Structure

- /domain – Business entities and financial models
- /services – Settlement and payout logic
- /infrastructure – Data ingestion and exports
- /presentation – Dashboard generation
- /docs – Product documentation
- /example_data – Mock fintech portfolio datasets



## Overview
Atlas Settlement is a **prototype internal settlement and payout operations platform** for a fintech lender/factoring business.  

It demonstrates real operational workflows for fintech backoffice teams:

- **Merchant payout orchestration**  
- **Rolling reserve calculation**  
- **Credit limit monitoring**  
- **Portfolio repayment projection**  
- **Operational dashboards**  

This project is a **product-focused prototype**, highlighting fintech domain knowledge, risk awareness, and system-level thinking.

---

## Problem
Settlement and Finance Operation teams in fintech often manage payouts, reserves, and exposures manually in spreadsheets.  
This creates:

- Operational risk  
- Delayed portfolio visibility  
- Manual reconciliation issues  

---

## Solution
Atlas Settlement centralizes operations in a **dashboard-style workflow**, allowing:

- Uploading portfolio data  
- Reviewing client payout readiness  
- Calculating rolling reserves  
- Monitoring credit exposure  
- Simulating portfolio repayments
- Executing payments to SEPA network (tbd)

---

## Core Features
- **Client payout workflow**: status tracking & execution simulation  
- **Risk monitoring**: exposure alerts, credit limit tracking  
- **Portfolio modeling**: repayment schedule with interest projections  
- **Client-level drilldowns**: subaccounts for factoring, settlement, rolling reserve, and partner RR  
- **Operational dashboard**: interactive HTML table prototype  

---

## Personas
- Risk Analysts  
- Settlement Operations  
- Finance Controllers  
- Credit Managers  

---

## Tech Stack
- Python (pandas, tabulate)  
- HTML/CSS for dashboard prototyping  
- GitHub for version control  

---

## Next Steps / Roadmap
1. **Prototype:** HTML dashboard, payout simulation, portfolio aggregation  
2. **MVP:** Approval workflows, audit trails, role-based permissions  
3. **Production-ready:** Banking API integration, real-time exposure, automated alerts  

---

## Notes
This is a **product portfolio prototype** created to demonstrate **fintech operations, risk modeling, and product management thinking** — ideal for PM interviews and portfolio showcases.


### Example data

The `example_data/` folder contains anonymised merchant data used to run
the settlement dashboard locally.

This data is for demonstration purposes only and does not represent
real merchants or transactions.

