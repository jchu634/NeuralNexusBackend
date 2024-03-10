from pathlib import Path
import pytest
from test_folder.tests.unit.test_auth import test_login, test_login_with_admin_admin_scope


@pytest.mark.skip(reason="I have no idea how to get a token with OAUTH2 scopes")
@pytest.mark.dependency(depends=["test_login"])
def test_get_user(client):
    path = "/api/v1/admin/clear_inference_cache"

    token = test_login(client)
    admin_token = test_login_with_admin_admin_scope(client)
    unauth_response = client.get(
        path
    )
    missing_scope_response = client.get(
        path,
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get(
        path,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert unauth_response.status_code == 401
    assert unauth_response.json()["detail"] == "Not authenticated"
    assert missing_scope_response.status_code == 401
    assert missing_scope_response.json()["detail"] == "Not enough permissions"
    assert response.status_code == 200
    assert response.json()["success"] == "cache cleared"
