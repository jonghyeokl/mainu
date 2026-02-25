from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from uuid import UUID

import jwt
from fastapi import HTTPException

from app.resources.config import conf


class JwtService:
    ACCESS_TOKEN_EXPIRATION = timedelta(minutes=60)

    @classmethod
    def build(cls) -> "JwtService":
        return cls()

    def _create_jwt_token(
        self,
        payload: Dict[str, Any],
        secret_key: str,
    ) -> str:
        return jwt.encode(payload, secret_key, algorithm="HS256")

    def _decode_jwt_token(
        self,
        token: str,
        secret_key: str,
    ) -> Dict[str, Any]:
        jwt_token = token.encode("utf-8")
        return jwt.decode(jwt_token, secret_key, algorithms=["HS256"])

    def create_access_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + self.ACCESS_TOKEN_EXPIRATION,
        }
        return self._create_jwt_token(payload, conf.ACCESS_TOKEN_SECRET_KEY)

    def validate_access_token(self, access_token: str) -> UUID:
        try:
            user_id = self._decode_jwt_token(
                access_token, conf.ACCESS_TOKEN_SECRET_KEY
            )["user_id"]
            if user_id is None:
                raise HTTPException(status_code=401, detail="Token invalid")
            return UUID(user_id)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token invalid")
