import json
from pathlib import Path


ROLE_ACCESS_MATRIX = [
    {
        "role": "procurement_requester",
        "can_create_po": True,
        "can_approve_po": False,
        "can_release_payment": False,
        "can_modify_vendor_master": False,
    },
    {
        "role": "procurement_manager",
        "can_create_po": True,
        "can_approve_po": True,
        "can_release_payment": False,
        "can_modify_vendor_master": False,
    },
    {
        "role": "finance_controller",
        "can_create_po": False,
        "can_approve_po": False,
        "can_release_payment": True,
        "can_modify_vendor_master": False,
    },
    {
        "role": "vendor_master_admin",
        "can_create_po": False,
        "can_approve_po": False,
        "can_release_payment": False,
        "can_modify_vendor_master": True,
    },
]

SEGREGATION_OF_DUTIES_RULES = [
    {
        "user": "user_104",
        "violation": "same_user_created_and_approved_po",
        "severity": "high",
        "decision": "block_release",
    },
    {
        "user": "user_208",
        "violation": "vendor_master_admin_released_payment",
        "severity": "critical",
        "decision": "block_release",
    },
    {
        "user": "user_315",
        "violation": "none",
        "severity": "none",
        "decision": "pass",
    },
]

APPROVAL_POLICY = {
    "purchase_order_amount": 125000,
    "required_approval_levels": 2,
    "finance_review_required": True,
    "executive_review_required": True,
    "policy_decision": "requires_finance_and_executive_review",
}

AUDIT_LOG_SAMPLE = [
    {
        "event": "purchase_order_created",
        "actor": "procurement_requester",
        "timestamp": "2026-06-08T11:42:00Z",
        "control_check": "passed",
    },
    {
        "event": "purchase_order_approved",
        "actor": "procurement_manager",
        "timestamp": "2026-06-08T12:00:00Z",
        "control_check": "passed",
    },
    {
        "event": "payment_release_requested",
        "actor": "vendor_master_admin",
        "timestamp": "2026-06-08T12:15:00Z",
        "control_check": "failed",
    },
]


def build_controls_artifacts(output_dir="controls_compliance"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    artifacts = {
        "role_access_matrix.json": ROLE_ACCESS_MATRIX,
        "segregation_of_duties_rules.json": SEGREGATION_OF_DUTIES_RULES,
        "approval_policy.json": APPROVAL_POLICY,
        "audit_log_sample.json": AUDIT_LOG_SAMPLE,
    }

    for filename, payload in artifacts.items():
        (output / filename).write_text(json.dumps(payload, indent=2))

    return artifacts


def controls_summary():
    violations = [
        row for row in SEGREGATION_OF_DUTIES_RULES
        if row["decision"] == "block_release"
    ]
    failed_audit_events = [
        row for row in AUDIT_LOG_SAMPLE
        if row["control_check"] == "failed"
    ]

    release_decision = "block_release" if violations or failed_audit_events else "approve_release"

    return {
        "roles_defined": len(ROLE_ACCESS_MATRIX),
        "sod_violations": len(violations),
        "failed_audit_events": len(failed_audit_events),
        "required_approval_levels": APPROVAL_POLICY["required_approval_levels"],
        "finance_review_required": APPROVAL_POLICY["finance_review_required"],
        "executive_review_required": APPROVAL_POLICY["executive_review_required"],
        "release_decision": release_decision,
    }


def write_controls_report(output_dir="controls_compliance"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    summary = controls_summary()

    report = f"""# Controls Compliance Report

## Summary

- Roles defined: {summary["roles_defined"]}
- Segregation-of-duties violations: {summary["sod_violations"]}
- Failed audit events: {summary["failed_audit_events"]}
- Required approval levels: {summary["required_approval_levels"]}
- Finance review required: {summary["finance_review_required"]}
- Executive review required: {summary["executive_review_required"]}

## Release Decision

`{summary["release_decision"]}`

## Compliance Signal

This module demonstrates role-based access control, approval-chain enforcement, segregation-of-duties monitoring, audit-log review, and release-blocking governance for SAP-style procurement and ERP integration workflows.
"""
    (output / "controls_compliance_report.md").write_text(report)
    return summary


if __name__ == "__main__":
    build_controls_artifacts()
    write_controls_report()
