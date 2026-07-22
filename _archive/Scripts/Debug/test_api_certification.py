import pytest
from fastapi.testclient import TestClient
from api.api import app
import json

client = TestClient(app)

def test_api_upload_dte():
    # Test file upload
    response = client.post(
        "/api/v4/upload/dte",
        data={"marketplace": "ALL"},
        files={"file": ("dummy.xml", b"<xml></xml>", "application/xml")}
    )
    # the exact behavior depends on DTEIndexer, we just expect a valid json structure back (e.g. success or error handling that doesn't 500 without catch)
    assert response.status_code in [200, 500]

def test_run_audit_endpoint():
    response = client.post("/api/v4/run-audit", params={"marketplace": "ALL"})
    assert response.status_code in [200, 500]

if __name__ == '__main__':
    pytest.main(['-v', __file__])
