from datetime import datetime

import pytest
from httpx import AsyncClient

from app.bookings.dao import BookingDAO


async def test_add_and_get_bookings_dao():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2
    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None


@pytest.mark.parametrize(
    "room_id, date_to, date_from, booked_rooms, status_code",
    [
        (4, "2030-05-01", "2030-05-25", 3, 200),
        (4, "2030-05-01", "2030-05-25", 4, 200),
        (4, "2030-05-01", "2030-05-25", 5, 200),
        (4, "2030-05-01", "2030-05-25", 6, 200),
        (4, "2030-05-01", "2030-05-25", 7, 200),
        (4, "2030-05-01", "2030-05-25", 8, 200),
        (4, "2030-05-01", "2030-05-25", 9, 200),
    ],
)
async def test_add_and_get_bookings_api(
    authenticated_client: AsyncClient,
    room_id,
    date_to,
    date_from,
    booked_rooms,
    status_code,
):
    response = await authenticated_client.post(
        "/bookings",
        params={"room_id": room_id, "date_from": date_to, "date_to": date_from},
    )
    assert response.status_code == status_code
    response = await authenticated_client.get("/bookings")
    assert len(response.json()) == booked_rooms
