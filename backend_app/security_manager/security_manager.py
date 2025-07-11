import datetime
import redis
import json
import base64
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from .config.settings import settings
import logging

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = redis.from_url(settings.CELERY_BROKER_URL, decode_responses=True)
NONCE_LIFETIME_SECONDS = 300


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_signature(public_key_pem: str, signed_data_b64: str, signature_b64: str, nonce: str, user_id: int) -> bool:
    """Verifies a signature and uses Redis to prevent replay attacks."""
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
    try:
        nonce_key = f"nonce:{user_id}:{nonce}"
        if redis_client.exists(nonce_key):
            logger.warning(f"Replay attack detected for nonce: {nonce}")
            return False

        signature_bytes = base64.b64decode(signature_b64)
        data_bytes = base64.b64decode(signed_data_b64)

        public_key.verify(
            signature_bytes, data_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )

        redis_client.setex(nonce_key, NONCE_LIFETIME_SECONDS, "used")
        return True
    except InvalidSignature:
        logger.warning(f"Invalid signature for nonce: {nonce}")
        return False
    except Exception as e:
        logger.error(f"Signature verification error for user {user_id}: {e}")
        return False