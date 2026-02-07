# Atlas Settlement – Product Decision Log

## Overview
This document captures key product and design decisions made during the development of the Atlas Settlement prototype.  
The goal is to demonstrate **product thinking**, trade-off evaluation, and structured decision-making typical of fintech product management.

---

## Decision 1 – HTML Dashboard Instead of Full Web App

**Context:**  
The goal was to demonstrate settlement workflows quickly without building a full frontend/backend stack. 

**Options Considered:**
- Full web application (React + backend API)
- Business intelligence dashboard
- Static HTML dashboard generated from Python

**Decision:**  
Use a dynamically generated HTML dashboard.

**Rationale:**
- Faster prototyping
- Focus remains on product workflows rather than infrastructure
- Easy to demonstrate data transformations and user journeys

**Trade-offs:**
- Limited interactivity
- No authentication or persistence

**Future Direction:**
- Replace with web-based UI in MVP phase

---

## Decision 2 – Excel-Based Input Data

**Context:**  
Prototype needed realistic operational data without requiring live integrations.

**Options Considered:**
- Banking API integration
- Database backend
- Static Excel files

**Decision:**  
Use Excel input as primary data source.

**Rationale:**
- Reflects real-world fintech operations workflows
- Easy to simulate portfolio changes
- Simplifies onboarding for demo users

**Trade-offs:**
- Manual data loading
- No real-time updates

**Future Direction:**
- Replace with database ingestion or API pipelines

---

## Decision 3 – Rolling Reserve & Partner RR Visibility

**Context:**  
Rolling reserves are central to factoring and fintech settlement risk management.

**Decision:**  
Expose:
- Client rolling reserve (`Client_RR`)
- Partner rolling reserve (`Partner_RR`)
- Rolling reserve percentages

**Rationale:**
- Demonstrates fintech financial literacy
- Shows risk monitoring in operational workflow
- Helps simulate exposure management

**Trade-offs:**
- Simplified financial modeling
- No dynamic policy configuration

**Future Direction:**
- Add configurable reserve policies

---

## Decision 4 – Status-Based Payout Workflow

**Context:**  
Needed a simple but realistic settlement lifecycle.

**Decision:**  
Introduce payout statuses:
- `Ready`
- `Requested`
- `Blocked` (conceptual)

**Rationale:**
- Reflects real operational approval steps
- Demonstrates workflow thinking
- Enables simulation of execution events

**Trade-offs:**
- No approval hierarchy
- No audit logging in prototype

**Future Direction:**
- Add dual-approval workflow
- Introduce audit trails

---

## Decision 5 – Portfolio Repayment Modeling

**Context:**  
Needed to demonstrate financial modeling beyond simple aggregation.

**Decision:**  
Include repayment schedule:
- Monthly principal
- Expected interest
- Outstanding balances

**Rationale:**
- Shows forward-looking financial analysis
- Demonstrates understanding of lending mechanics
- Adds strategic value to dashboard

**Trade-offs:**
- Linear amortization assumption
- No client-specific repayment structures

**Future Direction:**
- Add scenario simulation
- Introduce risk-weighted projections

---

## Decision 6 – Modular Folder Structure

**Context:**  
Prototype also serves as a product portfolio artifact.

**Decision:**  
Separate system into:
- `domain`
- `services`
- `infrastructure`
- `presentation`
- `docs`

**Rationale:**
- Demonstrates scalable system thinking
- Improves maintainability
- Communicates architecture clearly to recruiters

**Trade-offs:**
- Slightly more upfront structure for a prototype

**Future Direction:**
- Convert modules into deployable services

---

## Lessons Learned

- Product prototypes are most powerful when they simulate real workflows  
- Risk modeling increases credibility in fintech product portfolios  
- Clear documentation improves stakeholder understanding  
- Structured decisions communicate maturity as a product manager  

---

*This decision log demonstrates the candidate’s ability to reason through trade-offs, prioritize features, and design fintech products with operational realism.*
