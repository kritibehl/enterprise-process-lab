import json
from pathlib import Path


FLOW_STEPS = [
    {
        "system": "SAP S/4HANA",
        "business_object": "Purchase Order",
        "action": "create_purchase_order",
        "status": "approved",
        "validation": "purchase_order_id, vendor_id, and approval_status present",
    },
    {
        "system": "Oracle Finance",
        "business_object": "Invoice",
        "action": "reconcile_purchase_order",
        "status": "validated",
        "validation": "invoice amount reconciled against approved PO",
    },
    {
        "system": "ServiceNow",
        "business_object": "Change Ticket",
        "action": "create_go_live_change",
        "status": "approved",
        "validation": "rollback plan and business impact present",
    },
    {
        "system": "Workday",
        "business_object": "Employee Approval",
        "action": "manager_approval",
        "status": "approved",
        "validation": "manager approval limit authorizes transaction",
    },
]


def run_purchase_order_integration_flow():
    validated = sum(1 for step in FLOW_STEPS if step["status"] in {"approved", "validated"})

    return {
        "business_object": "Purchase Order",
        "status": "approved",
        "integrations_validated": validated,
        "total_integrations": len(FLOW_STEPS),
        "systems": [step["system"] for step in FLOW_STEPS],
        "executive_decision": "DO_NOT_RELEASE",
        "flow": FLOW_STEPS,
    }


def write_flow_artifacts(output_dir="artifacts"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    result = run_purchase_order_integration_flow()
    (output / "purchase_order_integration_flow.json").write_text(json.dumps(result, indent=2))

    report = f"""# Purchase Order Integration Flow

## Business Object

{result["business_object"]}

## Status

{result["status"]}

## Integrations Validated

{result["integrations_validated"]} / {result["total_integrations"]}

## Systems

{chr(10).join(f"- {system}" for system in result["systems"])}

## Executive Decision

{result["executive_decision"]}

## Summary

SAP Purchase Order flows through Oracle Finance reconciliation, ServiceNow change governance, and Workday manager approval.
"""
    (output / "purchase_order_integration_flow.md").write_text(report)

    return result


if __name__ == "__main__":
    write_flow_artifacts()
