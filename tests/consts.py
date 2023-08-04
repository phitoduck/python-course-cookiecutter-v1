from pathlib import Path

THIS_DIR = Path(__file__).parent

PROJECT_ROOT_DIR = (THIS_DIR / "../").resolve()
TEST_ARTIFACTS_DIR = (THIS_DIR / "artifacts").resolve()
