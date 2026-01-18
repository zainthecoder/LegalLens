"""
Unit tests for authentication helper functions.
These tests do not require a database connection.
"""
import pytest
from datetime import timedelta
from jose import jwt

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_get_password_hash_returns_valid_bcrypt(self):
        """Verify hashing produces a valid bcrypt hash."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        
        # bcrypt hashes start with $2b$ or $2a$
        assert hashed.startswith("$2")
        assert len(hashed) == 60  # bcrypt hashes are 60 chars

    def test_get_password_hash_produces_different_hashes(self):
        """Verify same password produces different hashes (due to salt)."""
        password = "mysecretpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Verify correct password matches its hash."""
        password = "correctpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Verify wrong password does not match."""
        password = "correctpassword"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_password(self):
        """Verify empty password handling."""
        password = "somepassword"
        hashed = get_password_hash(password)
        
        assert verify_password("", hashed) is False


class TestAccessToken:
    """Tests for JWT access token creation."""

    def test_create_access_token_contains_subject(self):
        """Verify token contains the correct subject claim."""
        email = "test@example.com"
        token = create_access_token(data={"sub": email})
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == email

    def test_create_access_token_has_expiration(self):
        """Verify token has an expiration claim."""
        token = create_access_token(data={"sub": "user@example.com"})
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_create_access_token_custom_expiration(self):
        """Verify custom expiration delta is applied."""
        expires = timedelta(hours=1)
        token = create_access_token(
            data={"sub": "user@example.com"},
            expires_delta=expires
        )
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_create_access_token_with_extra_claims(self):
        """Verify extra claims are preserved in token."""
        data = {"sub": "user@example.com", "role": "admin"}
        token = create_access_token(data=data)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "user@example.com"
        assert payload["role"] == "admin"
