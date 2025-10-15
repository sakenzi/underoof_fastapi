import pytest
from httpx import AsyncClient
from datetime import datetime
from passlib.context import CryptContext


@pytest.mark.asyncio
async def test_send_email_success(httpx_client: AsyncClient, test_db):
    test_email = "dias@gmail.com"
    await test_db.execute(
        "INSERT INTO users (email, verification_code, verification_code_created_at, is_active) "
        "VALUES (:email, :code, :created_at, :is_active)",
        {
            "email": test_email,
            "code": "123456",
            "created_at": datetime.utcnow(),
            "is_active": False
        }
    )

    response = await httpx_client.post(
        "/api/auth/email/send",
        json={"email": test_email}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Verification code sent to your email"
    assert "access_token" in response_json
    assert response_json["user"] is None

@pytest.mark.asyncio
async def test_send_email_invalid_input(httpx_client: AsyncClient):
    response = await httpx_client.post(
        "/api/auth/email/send",
        json={"email": "invalid-email"}
    )

    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_verify_email_success(httpx_client: AsyncClient, test_db):
    test_email = "dias@gmail.com"
    test_code = "123456"
    await test_db.execute(
        "INSERT INTO users (email, first_name, last_name, surname, phone_number, verification_code, verification_code_created_at, is_active) "
        "VALUES (:email, :first_name, :last_name, :surname, :phone_number, :code, :created_at, :is_active)",
        {
            "email": test_email,
            "first_name": "Dias",
            "last_name": "Lastname",
            "surname": "Surname",
            "phone_number": "+1234567890",
            "code": test_code,
            "created_at": datetime.utcnow(),
            "is_active": False
        }
    )

    await test_db.execute(
        "INSERT INTO roles (role_name) VALUES (:role_name) ON CONFLICT (role_name) DO NOTHING",
        {"role_name": "user"}
    )
    await test_db.execute(
        "INSERT INTO user_roles (user_id, role_id) "
        "VALUES ((SELECT id FROM users WHERE email = :email), (SELECT id FROM roles WHERE role_name = :role_name))",
        {"email": test_email, "role_name": "user"}
    )

    send_response = await httpx_client.post(
        "/api/auth/email/send",
        json={"email": test_email}
    )
    assert send_response.status_code == 200
    token = send_response.json()["access_token"]

    response = await httpx_client.post(
        f"/api/auth/email/verify/{token}",
        json={"code": test_code}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Token generated successfully"
    assert "access_token" in response_json
    assert "access_token_expire_time" in response_json
    assert response_json["user"] is not None
    assert response_json["user"]["email"] == test_email
    assert response_json["user"]["first_name"] == "Dias"
    assert response_json["user"]["last_name"] == "Lastname"
    assert response_json["user"]["surname"] == "Surname"
    assert response_json["user"]["phone_number"] == "+1234567890"
    assert response_json["user"]["role"] == "user"

@pytest.mark.asyncio
async def test_verify_email_invalid_code(httpx_client: AsyncClient, test_db):
    test_email = "dias@gmail.com"
    await test_db.execute(
        "INSERT INTO users (email, verification_code, verification_code_created_at, is_active) "
        "VALUES (:email, :code, :created_at, :is_active)",
        {
            "email": test_email,
            "code": "123456",
            "created_at": datetime.utcnow(),
            "is_active": False
        }
    )

    send_response = await httpx_client.post(
        "/api/auth/email/send",
        json={"email": test_email}
    )
    assert send_response.status_code == 200
    token = send_response.json()["access_token"]

    response = await httpx_client.post(
        f"/api/auth/email/verify/{token}",
        json={"code": "invalid"}
    )

    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_verify_email_invalid_token(httpx_client: AsyncClient):
    response = await httpx_client.post(
        "/api/auth/email/verify/invalid-token",
        json={"code": "123456"}
    )

    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_register_success(httpx_client: AsyncClient, test_db):
    test_email = "dias@gmail.com"
    test_data = {
        "first_name": "John",
        "last_name": "Doe",
        "surname": "Smith",
        "email": test_email,
        "phone_number": "87772069568",
        "password": "dias.2020"
    }

    response = await httpx_client.post(
        "/api/auth/register",
        json=test_data
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Token generated successfully"
    assert "access_token" in response_json
    assert "access_token_expire_time" is not None
    assert response_json["user"]["email"] == test_email
    assert response_json["user"]["first_name"] == test_data["first_name"]
    assert response_json["user"]["last_name"] == test_data["last_name"]
    assert response_json["user"]["surname"] == test_data["surname"]
    assert response_json["user"]["phone_number"] == test_data["phone_number"]
    assert response_json["user"]["role"] == "user"

    user = await test_db.fetch_one(
        "SELECT * FROM users WHERE email = :email",
        {"email": test_email}
    )
    assert user is not None
    assert user["email"] == test_email
    assert user["is_active"] == True

    role = await test_db.fetch_one(
        "SELECT r.role_name FROM roles r "
        "JOIN user_roles ur ON r.id = ur.role_id "
        "JOIN users u ON ur.user_id = u.id "
        "WHERE u.email = :email",
        {"email": test_email}
    )
    assert role["role_name"] == "user"

@pytest.mark.asyncio
async def test_register_invalid_input(httpx_client: AsyncClient):
    test_data = {
        "first_name": "John",
        "last_name": "Doe",
        "surname": "Smith",
        "email": "invalid-email",
        "phone_number": "+1234567890",
        "password": "short"
    }

    response = await httpx_client.post(
        "/api/auth/register",
        json=test_data
    )
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_login_success(httpx_client: AsyncClient, test_db):
    test_email = "dias@gmail.com"
    test_password = "dias.2020"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(test_password)

    await test_db.execute(
        "INSERT INTO users (email, first_name, last_name, surname, phone_number, password, is_active) "
        "VALUES (:email, :first_name, :last_name, :surname, :phone_number, :password, :is_active)",
        {
            "email": test_email,
            "first_name": "John",
            "last_name": "Doe",
            "surname": "Smith",
            "phone_number": "+1234567890",
            "password": hashed_password,
            "is_active": True
        }
    )

    await test_db.execute(
        "INSERT INTO roles (role_name) VALUES (:role_name) ON CONFLICT (role_name) DO NOTHING",
        {"role_name": "user"}
    )
    await test_db.execute(
        "INSERT INTO user_roles (user_id, role_id) "
        "VALUES ((SELECT id FROM users WHERE email = :email), (SELECT id FROM roles WHERE role_name = :role_name))",
        {"email": test_email, "role_name": "user"}
    )

    response = await httpx_client.post(
        "/api/auth/login",
        json={"email": test_email, "password": test_password}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Token generated successfully"
    assert "access_token" in response_json
    assert "access_token_expire_time" in response_json
    assert response_json["user"] is not None
    assert response_json["user"]["email"] == test_email
    assert response_json["user"]["first_name"] == "John"
    assert response_json["user"]["last_name"] == "Doe"
    assert response_json["user"]["surname"] == "Smith"
    assert response_json["user"]["phone_number"] == "+1234567890"
    assert response_json["user"]["role"] == "user"

@pytest.mark.asyncio
async def test_login_invalid_input(httpx_client: AsyncClient, test_db):
    test_email = "dias@gmail.com"
    test_password = "dias.2020"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(test_password)

    await test_db.execute(
        "INSERT INTO users (email, password, is_active) "
        "VALUES (:email, :password, :is_active)",
        {"email": test_email, "password": hashed_password, "is_active": True}
    )

    response = await httpx_client.post(
        "/api/auth/login",
        json={"email": test_email, "password": "wrong-password"}
    )

    assert response.status_code == 422
    assert "detail" in response.json()

    response = await httpx_client.post(
        "/api/auth/login",
        json={"email": "invalid-email", "password": test_password}
    )

    assert response.status_code == 422
    assert "detail" in response.json()