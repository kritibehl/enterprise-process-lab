from enterprise_process_lab.core import generate_artifacts
from enterprise_process_lab.scenario_engine import write_scenario_artifacts

if __name__ == "__main__":
    generate_artifacts()
    write_scenario_artifacts()
    print("Generated enterprise process artifacts in ./artifacts")
