from dataclasses import dataclass, asdict
from statistics import mean
import json
from pathlib import Path


@dataclass
class WorkflowRecord:
    process_id: str
    purchase_order: str
    vendor: str
    inventory_status: str
    shipment_status: str
    approval_status: str
    exception_type: str | None
    cycle_time_days: float
    sla_met: bool


WORKFLOWS = [
    WorkflowRecord("PRC-1001", "PO-9001", "Acme Components", "available", "delivered", "approved", None, 2.4, True),
    WorkflowRecord("PRC-1002", "PO-9002", "Nova Parts", "low_stock", "delayed", "blocked", "shipment_delay", 5.8, False),
    WorkflowRecord("PRC-1003", "PO-9003", "Global Freight", "available", "in_transit", "in_testing", None, 3.1, True),
    WorkflowRecord("PRC-1004", "PO-9004", "Vertex Supply", "stockout", "pending", "failed_validation", "inventory_mismatch", 6.2, False),
    WorkflowRecord("PRC-1005", "PO-9005", "Orion Vendors", "available", "delivered", "approved", None, 1.9, True),
]


REQUIREMENTS = [
    {
        "business_requirement": "Track purchase order approval status",
        "technical_implementation": "workflow_status_engine",
        "test_case": "test_purchase_order_status_tracking",
        "validation_status": "PASS",
    },
    {
        "business_requirement": "Detect delayed shipments",
        "technical_implementation": "shipment_exception_detector",
        "test_case": "test_shipment_delay_exception",
        "validation_status": "PASS",
    },
    {
        "business_requirement": "Block readiness when inventory validation fails",
        "technical_implementation": "readiness_gate",
        "test_case": "test_failed_validation_blocks_release",
        "validation_status": "PASS",
    },
    {
        "business_requirement": "Measure process SLA adherence",
        "technical_implementation": "process_analytics",
        "test_case": "test_sla_adherence_metric",
        "validation_status": "PASS",
    },
]


def workflow_explorer():
    return [asdict(item) for item in WORKFLOWS]


def requirements_traceability_matrix():
    return REQUIREMENTS


def implementation_readiness_dashboard():
    statuses = {}
    for item in WORKFLOWS:
        statuses[item.approval_status] = statuses.get(item.approval_status, 0) + 1

    decision = "approved"
    if statuses.get("blocked", 0) or statuses.get("failed_validation", 0):
        decision = "blocked"

    return {
        "approved": statuses.get("approved", 0),
        "blocked": statuses.get("blocked", 0),
        "in_testing": statuses.get("in_testing", 0),
        "failed_validation": statuses.get("failed_validation", 0),
        "release_decision": decision,
    }


def process_analytics():
    total = len(WORKFLOWS)
    exceptions = [w for w in WORKFLOWS if w.exception_type]
    sla_met = [w for w in WORKFLOWS if w.sla_met]

    return {
        "cycle_time_days_avg": round(mean(w.cycle_time_days for w in WORKFLOWS), 2),
        "exception_rate": round(len(exceptions) / total, 2),
        "throughput": total,
        "sla_adherence": round(len(sla_met) / total, 2),
    }


def change_management_center():
    return {
        "change_requests": 12,
        "approved": 8,
        "blocked": 2,
        "rollback_required": 1,
        "pending_business_signoff": 1,
        "governance_decision": "requires_review",
    }


def generate_artifacts(output_dir="artifacts"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    reports = {
        "workflow_explorer.json": workflow_explorer(),
        "requirements_traceability_matrix.json": requirements_traceability_matrix(),
        "implementation_readiness_dashboard.json": implementation_readiness_dashboard(),
        "process_analytics.json": process_analytics(),
        "change_management_center.json": change_management_center(),
    }

    for name, payload in reports.items():
        (output / name).write_text(json.dumps(payload, indent=2))

    summary = f"""# Enterprise Process Lab Report

## Implementation Readiness

- Approved: {reports["implementation_readiness_dashboard.json"]["approved"]}
- Blocked: {reports["implementation_readiness_dashboard.json"]["blocked"]}
- In testing: {reports["implementation_readiness_dashboard.json"]["in_testing"]}
- Failed validation: {reports["implementation_readiness_dashboard.json"]["failed_validation"]}
- Release decision: `{reports["implementation_readiness_dashboard.json"]["release_decision"]}`

## Process Analytics

- Average cycle time: {reports["process_analytics.json"]["cycle_time_days_avg"]} days
- Exception rate: {reports["process_analytics.json"]["exception_rate"]}
- Throughput: {reports["process_analytics.json"]["throughput"]} workflows
- SLA adherence: {reports["process_analytics.json"]["sla_adherence"]}

## Safe Claim

Built an enterprise process operations lab simulating supply-chain workflows, requirements traceability, readiness governance, process analytics, and change-management controls across ERP-style implementation lifecycles.
"""
    (output / "enterprise_process_report.md").write_text(summary)

    return reports


if __name__ == "__main__":
    generate_artifacts()
