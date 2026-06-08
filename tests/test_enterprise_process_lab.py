from enterprise_process_lab.core import (
    workflow_explorer,
    requirements_traceability_matrix,
    implementation_readiness_dashboard,
    process_analytics,
    change_management_center,
)


def test_workflow_explorer_contains_supply_chain_entities():
    workflows = workflow_explorer()
    assert workflows
    assert {"purchase_order", "vendor", "inventory_status", "shipment_status"} <= set(workflows[0])


def test_traceability_links_business_to_validation():
    matrix = requirements_traceability_matrix()
    assert all("business_requirement" in row for row in matrix)
    assert all("technical_implementation" in row for row in matrix)
    assert all("test_case" in row for row in matrix)
    assert all(row["validation_status"] == "PASS" for row in matrix)


def test_readiness_blocks_failed_or_blocked_workflows():
    dashboard = implementation_readiness_dashboard()
    assert dashboard["blocked"] == 1
    assert dashboard["failed_validation"] == 1
    assert dashboard["release_decision"] == "blocked"


def test_process_analytics_metrics_are_computed():
    analytics = process_analytics()
    assert analytics["throughput"] == 5
    assert analytics["exception_rate"] == 0.4
    assert analytics["sla_adherence"] == 0.6


def test_change_management_governance_signal():
    changes = change_management_center()
    assert changes["change_requests"] == 12
    assert changes["governance_decision"] == "requires_review"
