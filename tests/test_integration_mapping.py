from integration_mapping.build_integration_mapping import (
    INTEGRATION_MAPS,
    build_maps,
    summarize_maps,
)


REQUIRED_FIELDS = {
    "source_system",
    "target_system",
    "business_object",
    "data_contract",
    "validation_rule",
    "failure_mode",
    "owner",
    "test_case",
    "implementation_status",
}


def test_all_integration_records_have_required_fields():
    for records in INTEGRATION_MAPS.values():
        for record in records:
            assert REQUIRED_FIELDS <= set(record)


def test_integration_maps_cover_target_enterprise_platforms():
    summary = summarize_maps()
    systems = set(summary["systems_mapped"])

    assert "SAP S/4HANA" in systems
    assert "Oracle ERP Cloud" in systems
    assert "Workday" in systems
    assert "ServiceNow" in systems


def test_integration_maps_cover_core_business_objects():
    summary = summarize_maps()
    objects = set(summary["business_objects"])

    assert "Purchase Order" in objects
    assert "Inventory Item" in objects
    assert "Invoice" in objects
    assert "Employee Approval" in objects
    assert "Change Request" in objects


def test_integration_summary_counts_are_stable():
    summary = summarize_maps()

    assert summary["total_integrations"] == 7
    assert summary["validated"] == 5
    assert summary["in_testing"] == 2


def test_build_maps_writes_files(tmp_path):
    build_maps(tmp_path)

    assert (tmp_path / "sap_integration_map.json").exists()
    assert (tmp_path / "oracle_integration_map.json").exists()
    assert (tmp_path / "workday_integration_map.json").exists()
    assert (tmp_path / "servicenow_integration_map.json").exists()
