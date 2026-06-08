from enterprise_process_lab.scenario_engine import scenario_catalog, governance_summary


def test_scenario_catalog_has_enterprise_implementation_risks():
    scenarios = scenario_catalog()
    assert len(scenarios) == 4
    assert any(s["affected_process"] == "inventory_validation" for s in scenarios)
    assert any(s["affected_process"] == "logistics_execution" for s in scenarios)


def test_blocking_scenarios_drive_executive_decision():
    summary = governance_summary()
    assert summary["blocked"] == 2
    assert summary["requires_review"] == 1
    assert summary["approved"] == 1
    assert summary["executive_decision"] == "do_not_release"


def test_every_scenario_has_business_impact_and_action():
    for scenario in scenario_catalog():
        assert scenario["business_impact"]
        assert scenario["recommended_action"]
        assert scenario["readiness_decision"] in {"approve", "review", "block"}
