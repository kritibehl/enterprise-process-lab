from enterprise_process_lab.core import generate_artifacts
from enterprise_process_lab.scenario_engine import write_scenario_artifacts
from enterprise_process_lab.integration_scenarios.po_to_approval_flow import write_flow_artifacts
from integration_mapping.build_integration_mapping import build_maps, write_report

if __name__ == "__main__":
    generate_artifacts()
    write_scenario_artifacts()
    write_flow_artifacts()
    build_maps()
    write_report()
    print("Generated enterprise process artifacts, integration maps, and public dashboard")
