import json
from pathlib import Path


INTEGRATION_MAPS = {
    "sap_integration_map.json": [
        {
            "source_system": "SAP S/4HANA",
            "target_system": "Enterprise Process Lab",
            "business_object": "Purchase Order",
            "data_contract": ["purchase_order_id", "vendor_id", "approval_status", "net_value"],
            "validation_rule": "purchase_order_id and vendor_id must be present before approval",
            "failure_mode": "PO approval blocked due to missing supplier master data",
            "owner": "Procurement Systems",
            "test_case": "test_purchase_order_contract_validation",
            "implementation_status": "validated",
        },
        {
            "source_system": "SAP S/4HANA",
            "target_system": "Warehouse Management",
            "business_object": "Inventory Item",
            "data_contract": ["sku", "plant", "available_quantity", "reorder_threshold"],
            "validation_rule": "available_quantity must be greater than reorder_threshold for release readiness",
            "failure_mode": "Go-live blocked due to inventory mismatch",
            "owner": "Supply Chain Systems",
            "test_case": "test_inventory_readiness_validation",
            "implementation_status": "validated",
        },
    ],
    "oracle_integration_map.json": [
        {
            "source_system": "Oracle ERP Cloud",
            "target_system": "Enterprise Process Lab",
            "business_object": "Invoice",
            "data_contract": ["invoice_id", "purchase_order_id", "amount", "payment_status"],
            "validation_rule": "invoice amount must match approved purchase order amount",
            "failure_mode": "Invoice reconciliation exception",
            "owner": "Finance Systems",
            "test_case": "test_invoice_po_reconciliation",
            "implementation_status": "in_testing",
        },
        {
            "source_system": "Oracle SCM",
            "target_system": "Logistics Event Stream",
            "business_object": "Shipment Event",
            "data_contract": ["shipment_id", "carrier", "status", "expected_delivery_date"],
            "validation_rule": "delayed shipments must trigger readiness review",
            "failure_mode": "SLA breach from delayed carrier event",
            "owner": "Logistics Systems",
            "test_case": "test_shipment_delay_readiness_review",
            "implementation_status": "validated",
        },
    ],
    "workday_integration_map.json": [
        {
            "source_system": "Workday",
            "target_system": "Enterprise Approval Workflow",
            "business_object": "Employee Approval",
            "data_contract": ["employee_id", "manager_id", "approval_limit", "approval_status"],
            "validation_rule": "manager_id must exist and approval_limit must authorize transaction",
            "failure_mode": "Approval routing failure",
            "owner": "HR Systems",
            "test_case": "test_employee_approval_routing",
            "implementation_status": "validated",
        }
    ],
    "servicenow_integration_map.json": [
        {
            "source_system": "ServiceNow",
            "target_system": "Implementation Governance Board",
            "business_object": "Change Request",
            "data_contract": ["change_id", "risk_level", "approval_status", "rollback_plan"],
            "validation_rule": "high-risk changes require approval and rollback plan",
            "failure_mode": "Change blocked due to missing rollback plan",
            "owner": "ITSM Governance",
            "test_case": "test_change_request_governance_gate",
            "implementation_status": "validated",
        },
        {
            "source_system": "ServiceNow",
            "target_system": "Support Operations",
            "business_object": "Service Ticket",
            "data_contract": ["ticket_id", "priority", "assignment_group", "sla_status"],
            "validation_rule": "critical tickets must have assignment group and SLA status",
            "failure_mode": "SLA escalation due to unassigned ticket",
            "owner": "Support Operations",
            "test_case": "test_service_ticket_sla_validation",
            "implementation_status": "in_testing",
        },
    ],
}


def build_maps(output_dir="integration_mapping"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    for filename, records in INTEGRATION_MAPS.items():
        (output / filename).write_text(json.dumps(records, indent=2))

    return INTEGRATION_MAPS


def summarize_maps():
    records = [row for rows in INTEGRATION_MAPS.values() for row in rows]
    return {
        "systems_mapped": sorted({row["source_system"] for row in records}),
        "business_objects": sorted({row["business_object"] for row in records}),
        "total_integrations": len(records),
        "validated": sum(1 for row in records if row["implementation_status"] == "validated"),
        "in_testing": sum(1 for row in records if row["implementation_status"] == "in_testing"),
        "owners": sorted({row["owner"] for row in records}),
    }


def write_report(output_dir="integration_mapping"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)
    summary = summarize_maps()

    report = f"""# Enterprise Integration Mapping Report

## Summary

- Systems mapped: {len(summary["systems_mapped"])}
- Business objects: {len(summary["business_objects"])}
- Total integrations: {summary["total_integrations"]}
- Validated: {summary["validated"]}
- In testing: {summary["in_testing"]}

## Systems

{chr(10).join(f"- {system}" for system in summary["systems_mapped"])}

## Business Objects

{chr(10).join(f"- {obj}" for obj in summary["business_objects"])}

## Implementation Signal

This layer demonstrates enterprise integration design across ERP, HRIS, ITSM, logistics, finance, procurement, and support workflows.

Each integration map includes source system, target system, business object, data contract, validation rule, failure mode, owner, test case, and implementation status.
"""
    (output / "integration_mapping_report.md").write_text(report)
    return summary


if __name__ == "__main__":
    build_maps()
    write_report()
