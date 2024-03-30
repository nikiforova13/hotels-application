import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id,email, user_exsist",
    [
        (1, "test@test.com", True),
        (2, "artem@example.com", True),
        (10000, ".....", False),
    ],
)
async def test_find_user_by_id(user_id, email, user_exsist):
    user = await UserDAO.find_by_id(model_id=user_id)
    if user_exsist:
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
