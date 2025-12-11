import pytest
from os import environ
from datetime import datetime, timedelta

from jose import jwt, JWTError
from unittest.mock import patch, MagicMock

from freezegun import freeze_time

from app.core.auth import verify_hashed, get_hash, \
    create_access_token
from app.settings import settings


def test_verify_hashed():
    b_str = 'qwerty123456'
    h_str = get_hash(b_str)

    assert verify_hashed(b_str, h_str)


def test_get_hash_returns_bytes():
    result = get_hash("password123")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_hash_different_for_same_input():
    hash1 = get_hash("password123")
    hash2 = get_hash("password123")
    assert hash1 != hash2


def test_verify_hashed_correct_password():
    password = "secure_password"
    hashed = get_hash(password)
    result = verify_hashed(password, hashed)
    assert result is True


def test_verify_hashed_incorrect_password():
    password = "secure_password"
    wrong_password = "wrong_password"
    hashed = get_hash(password)
    result = verify_hashed(wrong_password, hashed)
    assert result is False


def test_verify_hashed_empty_string():
    hashed = get_hash("")
    result = verify_hashed("", hashed)
    assert result is True
    result = verify_hashed("not_empty", hashed)
    assert result is False


def test_verify_hashed_special_characters():
    password = "p@ssw0rd!#$%^&*()"
    hashed = get_hash(password)
    result = verify_hashed(password, hashed)
    assert result is True
    result = verify_hashed("different", hashed)
    assert result is False


def test_create_token_with_default_expiration():
    # Подготавливаем тестовые данные
    test_data = {"user_id": 123, "username": "testuser"}
    # Мокаем текущее время для предсказуемости теста
    with freeze_time("2024-01-01 12:00:00"):
        # Вызываем функцию
        token = create_access_token(test_data)
        # Декодируем токен для проверки
        decoded = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )
        # Проверяем, что данные сохранились
        assert decoded["user_id"] == 123
        assert decoded["username"] == "testuser"
        # Проверяем, что expiration установлен правильно
        expected_exp = datetime(2024, 1, 1, 12, 0) + timedelta(
            minutes=settings.AUTH_TOKEN_LIFETIME_IN_MIN
        )
        assert datetime.fromtimestamp(decoded["exp"]) == expected_exp

def test_create_token_with_custom_expiration():
    test_data = {"user_id": 456}
    custom_delta = timedelta(hours=2)
    with freeze_time("2024-01-01 12:00:00"):
        token = create_access_token(test_data, expires_delta=custom_delta)
        decoded = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )
        # Проверяем кастомное время жизни
        expected_exp = datetime(2024, 1, 1, 12, 0) + custom_delta
        assert datetime.fromtimestamp(decoded["exp"]) == expected_exp



def test_token_does_not_modify_original_data():
    original_data = {"user_id": 789, "email": "test@example.com"}
    data_copy = original_data.copy()
    token = create_access_token(original_data)
    # Проверяем, что исходные данные не изменились
    assert original_data == data_copy
    assert "exp" not in original_data


def test_token_contains_exp_claim():
    test_data = {"sub": "test"}
    token = create_access_token(test_data)
    decoded = jwt.decode(
        token,
        settings.AUTH_SECRET_KEY,
        algorithms=[settings.AUTH_ALGORITHM]
    )
    assert "exp" in decoded


def test_token_with_empty_data():
    test_data = {}
    token = create_access_token(test_data)
    decoded = jwt.decode(
        token,
        settings.AUTH_SECRET_KEY,
        algorithms=[settings.AUTH_ALGORITHM]
    )
    # Проверяем, что токен создан и содержит только exp
    assert "exp" in decoded
    assert len(decoded) == 1  # только exp


def test_token_with_nested_data():
    test_data = {
        "user": {
            "id": 1,
            "roles": ["admin", "user"]
        },
        "metadata": {
            "created_at": "2024-01-01"
        }
    }
    token = create_access_token(test_data)
    decoded = jwt.decode(
        token,
        settings.AUTH_SECRET_KEY,
        algorithms=[settings.AUTH_ALGORITHM]
    )
    # Проверяем, что вложенные данные сохранились
    assert decoded["user"]["id"] == 1
    assert "admin" in decoded["user"]["roles"]
    assert decoded["metadata"]["created_at"] == "2024-01-01"


def test_expires_delta_none_uses_default():
    test_data = {"id": 1}
    with freeze_time("2024-01-01 12:00:00"):
        token = create_access_token(test_data, expires_delta=None)
        decoded = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )
        # Проверяем дефолтное время жизни
        expected_exp = datetime(2024, 1, 1, 12, 0) + timedelta(
            minutes=settings.AUTH_TOKEN_LIFETIME_IN_MIN
        )
        assert datetime.fromtimestamp(decoded["exp"]) == expected_exp


@pytest.mark.parametrize("expires_delta", [
    timedelta(seconds=30),  # Очень короткое время
    timedelta(days=30),  # Долгое время
    timedelta(hours=1, minutes=30, seconds=15),  # Сложный delta
])
def test_various_expires_delta_values(expires_delta):
    test_data = {"test": "data"}
    with freeze_time("2024-01-01 12:00:00"):
        token = create_access_token(test_data, expires_delta=expires_delta)
        decoded = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )
        expected_exp = datetime(2024, 1, 1, 12, 0) + expires_delta
        actual_exp = datetime.fromtimestamp(decoded["exp"])
        # Используем приблизительное сравнение для микросекунд
        time_diff = abs((actual_exp - expected_exp).total_seconds())
        assert time_diff < 1  # Разница менее 1 секунды
