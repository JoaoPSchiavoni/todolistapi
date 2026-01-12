from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from todolist_api.database import get_session
from todolist_api.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', email='alice@test', password='secret'
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'alice'))
    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }


def test_get_session():
    gen = get_session()

    session = next(gen)

    assert isinstance(session, Session)
    assert session.is_active
