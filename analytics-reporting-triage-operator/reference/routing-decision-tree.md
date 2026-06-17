# Routing Decision Tree

Use this tree to determine which team owns a request. Follow each branch in order. Stop at the first match.

This tree implements §2 of rules.md.

---

## The Tree

```
START: Who should own this work?
│
├── Does the request describe something wrong with a live report or data feed?
│   │
│   ├── YES → Go to [A: Defect/Anomaly Branch]
│   │
│   └── NO → Continue ↓
│
├── Does the requester want access to something that already exists?
│   │
│   ├── YES → Route: ANALYTICS / BI TEAM (access management)
│   │          Apply Rule 5.1: default to item-level scope
│   │
│   └── NO → Continue ↓
│
├── Does the requester have their own SQL, query, or Excel logic
│   and want BI to wrap it in a report?
│   │
│   ├── YES → Route: SELF-SERVICE (redirect)
│   │          Apply Rule 2.2: do not accept user-authored logic as spec
│   │
│   └── NO → Continue ↓
│
├── Does the work require changes to a data pipeline, new data ingestion,
│   source system table modifications, or infrastructure?
│   │
│   ├── YES → Route: DATA ENGINEERING
│   │          BI team may be a secondary stakeholder for surface context
│   │
│   └── NO → Continue ↓
│
├── Does the request duplicate logic that is already calculated and
│   maintained in a source system (ERP, CRM, WMS, etc.)?
│   │
│   ├── YES → Route: SOURCE SYSTEM TEAM
│   │          Flag: Logic Duplication Risk — escalate to Analytics lead
│   │
│   └── NO → Continue ↓
│
├── Does the request require a strategic or architectural decision
│   (new tooling, platform direction, team process, major model change)?
│   │
│   ├── YES → Route: ANALYTICS DIRECTOR / LEAD (escalation)
│   │          Do not log to development backlog until direction is set
│   │
│   └── NO → Continue ↓
│
└── Default: Route to ANALYTICS / BI TEAM
    The work involves building, modifying, or maintaining a reporting
    artifact in the analytics layer.
```

---

## Branch A: Defect / Anomaly

When something is wrong with a live report or data:

```
[A: Defect/Anomaly Branch]
│
├── Is the claim "data is missing" or "numbers look wrong"?
│   │
│   ├── YES → VERIFY FIRST before routing:
│   │         Step 1: Is the data present in the source system?
│   │         Step 2: Was the report displaying it correctly before?
│   │         │
│   │         ├── Both YES → Classify as DEFECT
│   │         │              Route: ANALYTICS / BI TEAM
│   │         │
│   │         ├── Step 1 NO → Classify as DATA ANOMALY
│   │         │               Route: SOURCE SYSTEM TEAM or DATA ENGINEERING
│   │         │               (data never made it to analytics layer)
│   │         │
│   │         └── Step 2 NO or UNKNOWN → Classify as DATA ANOMALY
│   │                                    Route: ANALYTICS / BI TEAM (verify)
│   │                                    + DATA ENGINEERING (investigate)
│   │
│   └── NO → The report behavior is unexpected but data exists:
│            Apply Rule 1.1: Check filter state and display interaction
│            first — many "bugs" are filter defaults or slicer states
│            │
│            ├── Filter state explains it → Not a defect; user education
│            │
│            └── Filter state is correct → Classify as DEFECT
│                                          Route: ANALYTICS / BI TEAM
```

---

## Routing Quick Reference

| Route | Owns what |
|-------|-----------|
| **Analytics / BI Team** | Reports, dashboards, semantic models, measures, visualizations, access management for existing artifacts |
| **Data Engineering** | Pipelines, ingestion, lakehouse/medallion layers, data refresh scheduling, infrastructure |
| **Source System Team** | ERP, CRM, WMS, or other operational system data issues; exception and validation logic that lives in those systems |
| **Self-Service** | User has the query/data/tool access; redirect rather than build |
| **Analytics Director / Lead** | Strategic and architectural decisions; escalations requiring policy decisions |
| **Another Team** | Request was misrouted; note the correct team and redirect |

---

## Routing + Ownership Table for Common Request Types

| Request Type | Primary Route | Secondary Involvement |
|-------------|--------------|----------------------|
| Defect in live report (confirmed) | Analytics / BI Team | None |
| Data anomaly — source unclear | Data Engineering | Analytics / BI Team (surface context) |
| New report build — data ready | Analytics / BI Team | None |
| New report build — data not ready | Backlog (blocked on DE or source system) | Data Engineering to unblock |
| Report enhancement | Analytics / BI Team | None |
| Access request | Analytics / BI Team | BI Lead if workspace-level |
| Metric / lineage inquiry | Analytics / BI Team | Source system team if tracing upstream |
| Pipeline or refresh failure | Data Engineering | Analytics / BI Team (user communication) |
| Logic duplication from source system | Source System Team | Analytics lead (escalation) |
| Self-service redirect | Self-Service | Analytics / BI Team (guidance only) |
| Strategic / architectural decision | Analytics Director / Lead | Analytics Manager (inputs) |
