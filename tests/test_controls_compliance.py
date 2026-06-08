from pathlib import Path

from controls_compliance.build_controls_report import (
    ROLE_ACCESS_MATRIX,
    SEGREGATION_OF_DUTIES_RULES,
    APPROVAL_POLICY,
    AUDIT_LOG_SAMPLE,
    build_controls_artifacts,
    controls_summary,
)


def test_role_access_matrix_enforces_payment_separation():
    procurement_manager = next(
        role for role in ROLE_ACCESS_MATRIX
        if role["role"] == "procurement_manager"
    )

    assert procurement_manager["can_create_po"] is True
    assert procurement_manager["can_approve_po"] is True
    assert procurement_manager["can_release_payment"] is False


def test_segregation_of_duties_blocks_high_risk_violations():
    violations = [
        rule for rule in SEGREGATION_OF_DUTIES_RULES
        if rule["decision"] == "block_release"
    ]

    assert len(violations) == 2
    assert any(v["violation"] == "same_user_created_and_approved_po" for v in violations)
    assert any(v["severity"] == "critical" for v in violations)


def test_approval_policy_requires_finance_and_executive_review():
    assert APPROVAL_POLICY["purchase_order_amount"] == 125000
    assert APPROVAL_POLICY["required_approval_levels"] == 2
    assert APPROVAL_POLICY["finance_review_required"] is True
    assert APPROVAL_POLICY["executive_review_required"] is True


def test_audit_log_tracks_failed_control_checks():
    failed_events = [
        event for event in AUDIT_LOG_SAMPLE
        if event["control_check"] == "failed"
    ]

    assert len(failed_events) == 1
    assert failed_events[0]["event"] == "payment_release_requested"


def test_controls_summary_blocks_release_when_controls_fail():
    summary = controls_summary()

    assert summary["roles_defined"] == 4
    assert summary["sod_violations"] == 2
    assert summary["failed_audit_events"] == 1
    assert summary["release_decision"] == "block_release"


def test_controls_artifacts_are_written(tmp_path):
    build_controls_artifacts(tmp_path)

    assert (tmp_path / "role_access_matrix.json").exists()
    assert (tmp_path / "segregation_of_duties_rules.json").exists()
    assert (tmp_path / "approval_policy.json").exists()
    assert (tmp_path / "audit_log_sample.json").exists()
