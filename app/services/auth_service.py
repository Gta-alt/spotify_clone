from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.user import User


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, email: str, username: str, password: str):
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(400, "Email already registered")

        user = User(
            email=email,
            username=username,
            hashed_password=hash_password(password)
        )
        return await self.repo.create(user)

    async def login(self, email: str, password: str):
        user = await self.repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})

        return access, refresh