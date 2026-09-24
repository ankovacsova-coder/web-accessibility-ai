import sys
import time
import subprocess
import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def run_streamlit():
    proc = subprocess.Popen([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.port",
        "8501",
        "--server.headless",
        "true",
    ])

    timeout = 30
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            if requests.get("http://localhost:8501").status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)

    yield
    proc.terminate()