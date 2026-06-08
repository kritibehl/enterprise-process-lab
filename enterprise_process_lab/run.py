from enterprise_process_lab.core import generate_artifacts
from enterprise_process_lab.scenario_engine import write_scenario_artifacts
from integration_mapping.build_integration_mapping import build_maps, write_report

if __name__ == "__main__":
    generate_artifacts()
    write_scenario_artifacts()
    build_maps()
    write_report()
    print("Generated enterprise process artifacts in ./artifacts and ./integration_mapping")
