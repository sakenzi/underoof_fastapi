import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_email_success():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/auth/email/send",
            json={"email": "dias@gmail.com"}
        )

        assert response.status_code == 200  
        response_json = response.json()
        assert response_json["message"] == "Verification code sent to your email"
        assert "access_token" in response_json
        assert response_json["user"] is None 

@pytest.mark.asyncio
async def test_send_email_invalid_input():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/auth/email/send",
            json={"email": "invalid-email"}
        )

        assert response.status_code == 422  
        assert "detail" in response.json()