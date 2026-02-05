# Atlas Settlement – System Architecture

## Overview
Atlas Settlement is a **prototype internal settlement and payout operations platform** for fintech operations teams.  
The system is designed to centralize client payouts, monitor rolling reserves, track credit exposure, and model portfolio repayments.  

This document outlines the **architecture, modules, data flow, and key design decisions**.

---

## Architecture Diagram (tbd) )


**Input Excel -> Data Processing -> Business Logic -> Presentation Layer**
 
**Input**: Merchant Data, Receivables/Loan Amount, Fees, Duration
**Data Processing**: Pandas for aggregation, status column, Rolling Reserve calculation
**Business Logic** : Payout Simulation ,Credit Limit Checks, Merchant Rolling Reserve, Portfolio Outstanding Amortization
**Presentation Layer** : HTML/CSS dashboard, Summary table, Merchant subaccounts, Repayment schedule|

---

## Modules

| Module | Description |
|--------|-------------|
| `domain/` | Core business entities such as Clients, Accounts, and Transactions. |
| `services/` | Business logic for payout calculations, rolling reserve, and credit exposure. |
| `infrastructure/` | Data handling: reading Excel files, logging, output generation. |
| `presentation/` | HTML table generation, dashboard formatting, interactive client drilldowns. |
| `assets/` | Static resources (logos, icons) used in dashboard prototype. |
| `example_data/` | Sample Excel files used for testing and demo purposes. |
| `docs/` | Documentation including PRODUCT_BRIEF, SYSTEM_ARCHITECTURE, and roadmap. |

---

## Data Flow

1. **Input**: Users upload Excel files containing client accounts, receivables, margins, and payouts.  
2. **Processing**: Data is read and aggregated using `pandas`.  
   - Add `Status` column for payout readiness  
   - Aggregate rolling reserves (`Client_RR`)  
   - Compute `Partner_RR` and other derived fields  
3. **Business Logic**:  
   - Calculate portfolio repayment schedule  
   - Perform credit limit checks and exposure ratios  
   - Simulate payout execution  
4. **Output / Presentation**:  
   - Generate HTML tables and interactive dashboard  
   - Include client-level drilldowns and subaccount summaries  
   - Highlight totals and percentages  
5. **Optional Export**: Save summary tables to Excel for offline use  

---

## Key Design Decisions

- **Modular Structure**: Separation of domain, services, infrastructure, and presentation allows for easy extension and maintainability.  
- **Prototype-Focused**: HTML dashboard allows interactive exploration without full backend integration.  
- **Data-First**: Uses mock Excel data to simulate real operational flows safely.  
- **Risk Awareness**: Calculations include rolling reserve, partner RR, and credit limits, demonstrating fintech risk modeling.  
- **Portfolio Modeling**: Simulates amortization and interest schedules to showcase financial understanding.  

---

## Next Steps (Future Architecture Enhancements)

- Introduce **role-based access control** for operational safety  
- Connect to **real-time banking APIs** for live payouts  
- Add **audit trail and logging** for compliance  
- Implement **automated alerts** for credit limit breaches or payout issues  

---

*This document demonstrates the candidate’s ability to think like a PM: translating business needs into system design, defining modules, and showing operational workflows in a scalable and understandable way.*
