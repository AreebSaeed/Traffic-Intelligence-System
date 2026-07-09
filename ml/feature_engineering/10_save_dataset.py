import subprocess
import sys
from pathlib import Path

from config import FINAL_DATASET_PATH, LABELED_OUTPUT

PIPELINE_SCRIPTS = [
    "01_extract_roads.py",
    "02_extract_weather.py",
    "03_extract_holidays.py",
    "04_extract_school.py",
    "05_extract_office.py",
    "06_extract_events.py",
    "07_create_time_features.py",
    "08_merge_all.py",
    "09_generate_labels.py",
]


def run_pipeline() -> None:
    script_dir = Path(__file__).resolve().parent

    for script in PIPELINE_SCRIPTS:
        print(f"\nRunning {script}...")
        subprocess.run([sys.executable, str(script_dir / script)], check=True)

    labeled = __import__("pandas").read_csv(LABELED_OUTPUT)
    FINAL_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    labeled.to_csv(FINAL_DATASET_PATH, index=False)
    print(f"\nFinal dataset saved to {FINAL_DATASET_PATH} ({len(labeled)} rows)")


if __name__ == "__main__":
    run_pipeline()
