from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, ConfigDict
from starlette.background import BackgroundTask, BackgroundTasks

from common.auth import CurrentUser, get_current_user, get_admin_user
from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: str = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


@router.post("/login")
@inject
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(Provide[Container.user_service])
):
    access_token = user_service.login(email=form_data.username, password=form_data.password)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("", status_code=201)
@inject
def create_user(user: CreateUserBody,
                background_tasks: BackgroundTasks,
                user_service: UserService = Depends(Provide[Container.user_service]), ) -> UserResponse:
    created_user = user_service.create_user(name=user.name, email=user.email,
                                            password=user.password)
    return created_user


@router.put("/{user_id}")
@inject
def update_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        user: UpdateUserBody,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    user = user_service.update_user(
        user_id=current_user.id,
        name=user.name,
        password=user.password
    )
    return user


@router.get("")
@inject
def get_users(
        page: int = 1,
        items_per_page: int = 10,
        current_user=Depends(get_admin_user),
        user_service: UserService = Depends(Provide[Container.user_service])
) -> GetUsersResponse:
    total_count, users = user_service.get_users(page, items_per_page)

    return GetUsersResponse(
        total_count=total_count,
        page=page,
        users=[UserResponse.model_validate(user) for user in users]
    )


@router.delete("", status_code=204)
@inject
def delete_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        user_service: UserService = Depends(Provide[Container.user_service])
):
    user_service.delete_user(current_user.id)
