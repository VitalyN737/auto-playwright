import pytest
from tests.server import run_server
import socket

@pytest.fixture(scope="session")
def test_server():
    port = 3000
    # Find an open port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                break
            port += 1

    run_server(port)
    yield f"http://localhost:{port}"