import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("hello83@mail.ru", "8723990", 200),
        ("hello83@mail.ru", "8723990", 409),
        ("test", "8723990", 422),
    ],
)
async def test_register_user(
    email,
    password,
    status_code,
    client: AsyncClient,
):
    response = await client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("nouser@example.com", "not", 401),
    ],
)
async def test_login_user(
    email,
    password,
    status_code,
    client: AsyncClient,
):
    response = await client.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == status_code
