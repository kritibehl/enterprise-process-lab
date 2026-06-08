from pathlib import Path


def test_abap_reports_exist_and_have_sap_patterns():
    files = [
        "abap/z_po_exception_report.abap",
        "abap/z_inventory_shortage_report.abap",
        "abap/z_vendor_master_validation.abap",
        "abap/z_shipment_delay_report.abap",
    ]

    for filename in files:
        text = Path(filename).read_text()
        assert "REPORT z_" in text
        assert "SELECTION-SCREEN" in text
        assert "TYPES: BEGIN OF" in text
        assert "STANDARD TABLE" in text
        assert "START-OF-SELECTION" in text
        assert "WRITE:" in text
        assert "BLOCK:" in text


def test_lifecycle_docs_cover_google_implementation_language:
    for phase in ["analyze", "design", "build", "test", "implement", "support"]:
        path = Path(f"implementation_lifecycle/{phase}.md")
        assert path.exists()
        assert path.read_text().strip().startswith(f"# {phase.title()}")


def test_visual_assets_exist_for_readme():
    for asset in [
        "process_flow.svg",
        "readiness_dashboard.svg",
        "traceability_matrix.svg",
        "abap_report_output.svg",
        "executive_summary.svg",
    ]:
        assert Path("assets/screenshots", asset).exists()
