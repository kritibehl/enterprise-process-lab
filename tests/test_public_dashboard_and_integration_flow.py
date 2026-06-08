from pathlib import Path

from enterprise_process_lab.integration_scenarios.po_to_approval_flow import (
    run_purchase_order_integration_flow,
)


def test_purchase_order_integration_flow_validates_four_systems():
    result = run_purchase_order_integration_flow()

    assert result["business_object"] == "Purchase Order"
    assert result["status"] == "approved"
    assert result["integrations_validated"] == 4
    assert result["total_integrations"] == 4

    systems = set(result["systems"])
    assert "SAP S/4HANA" in systems
    assert "Oracle Finance" in systems
    assert "ServiceNow" in systems
    assert "Workday" in systems


def test_dashboard_exists_and_shows_executive_metrics():
    dashboard = Path("public_dashboard/index.html")
    assert dashboard.exists()

    text = dashboard.read_text()
    assert "Readiness Score" in text
    assert "84" in text
    assert "DO_NOT_RELEASE" in text
    assert "SAP Purchase Order" in text
    assert "Oracle Finance" in text
    assert "ServiceNow Change Ticket" in text
    assert "Workday Approval" in text
