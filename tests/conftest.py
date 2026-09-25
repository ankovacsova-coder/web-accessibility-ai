import os
import sys
import time
import subprocess
import pytest
import requests


def get_test_port():
    raw = os.getenv("STREAMLIT_SERVER_PORT", "8501").strip()
    try:
        port = int(raw)
        return port if 1 <= port <= 65535 else 8501
    except ValueError:
        return 8501


@pytest.fixture(scope="session", autouse=True)
def run_streamlit():
    port = get_test_port()
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            str(port),
            "--server.headless",
            "true",
        ]
    )

    timeout = 30
    start_time = time.time()
    url = f"http://localhost:{port}"

    while time.time() - start_time < timeout:
        try:
            if requests.get(url).status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)

    yield
    proc.terminate()