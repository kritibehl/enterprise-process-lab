from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class EnterpriseScenario:
    scenario_id: str
    name: str
    affected_process: str
    severity: str
    business_impact: str
    recommended_action: str
    readiness_decision: str


SCENARIOS = [
    EnterpriseScenario(
        "SCN-001",
        "Shipment delay during procurement cutover",
        "logistics_execution",
        "high",
        "Delayed fulfillment and missed SLA risk",
        "Block go-live until shipment exception workflow is validated",
        "block",
    ),
    EnterpriseScenario(
        "SCN-002",
        "Inventory mismatch before purchase order approval",
        "inventory_validation",
        "critical",
        "Incorrect stock availability may trigger failed customer commitments",
        "Require inventory reconciliation and business signoff",
        "block",
    ),
    EnterpriseScenario(
        "SCN-003",
        "Vendor master data incomplete",
        "supplier_management",
        "medium",
        "Purchase order routing may fail for incomplete supplier records",
        "Send to data quality remediation queue",
        "review",
    ),
    EnterpriseScenario(
        "SCN-004",
        "All validation checks passed for standard procurement flow",
        "procurement",
        "low",
        "No major implementation risk detected",
        "Approve workflow for release candidate",
        "approve",
    ),
]


def scenario_catalog():
    return [asdict(s) for s in SCENARIOS]


def governance_summary():
    catalog = scenario_catalog()
    return {
        "total_scenarios": len(catalog),
        "approved": sum(1 for s in catalog if s["readiness_decision"] == "approve"),
        "blocked": sum(1 for s in catalog if s["readiness_decision"] == "block"),
        "requires_review": sum(1 for s in catalog if s["readiness_decision"] == "review"),
        "executive_decision": "do_not_release" if any(s["readiness_decision"] == "block" for s in catalog) else "release",
    }


def write_scenario_artifacts(output_dir="artifacts"):
    output = Path(output_dir)
    output.mkdir(exist_ok=True)

    catalog = scenario_catalog()
    summary = governance_summary()

    (output / "enterprise_scenarios.json").write_text(json.dumps(catalog, indent=2))
    (output / "executive_governance_summary.json").write_text(json.dumps(summary, indent=2))

    markdown = f"""# Executive Governance Summary

## Decision

`{summary["executive_decision"]}`

## Scenario Coverage

- Total scenarios: {summary["total_scenarios"]}
- Approved: {summary["approved"]}
- Blocked: {summary["blocked"]}
- Requires review: {summary["requires_review"]}

## Key Risk

Go-live should remain blocked while critical inventory and logistics execution scenarios still require validation.

## Recommended Executive Action

Hold release until blocked scenarios are remediated, retested, and signed off by business owners.
"""
    (output / "executive_governance_summary.md").write_text(markdown)
    return summary


if __name__ == "__main__":
    write_scenario_artifacts()
