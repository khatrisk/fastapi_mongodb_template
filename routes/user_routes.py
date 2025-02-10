"""
User registration router
"""

from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from auth.current_user import get_current_user
from models.user_model import UserBase, UserIn, UserUpdate, UserOut
from models.message_models import Message
from models.thing_model import MyThing, MyThingIn, MyThingOut
from controllers.user_controllers import (
    create_user,
    get_users,
    add_something_to_user,
    delete_user_by_id,
    update_user_data,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_route = APIRouter()


# Create
@user_route.post("/register")
async def add_user_to_db(user: UserIn) -> UserOut:
    """To create a new user, you only need to pass in email, username, and
        password of type: UserIn.

    - The password will be converted to a hash before saving.
    - A generic avatar will be generated.
    - Return is a newly created user of type  UserBase.
    """
    new_user = await create_user(user)

    return new_user


@user_route.post("/add_thing")
async def add_something(
    thing: MyThingIn, current_user: Annotated[UserBase, Depends(get_current_user)]
) -> MyThingOut:
    """
    Route works for currently logged in user.
    - Takes a "thing" of type: MyThingIn, and adds it to the current logged-in
    user things.
    - Returns the added "thing" of type: MyThingOut
    """

    result = await add_something_to_user(thing, current_user)
    return result


# Read
@user_route.get("/all")
async def read_all_users(
    current_user: Annotated[UserBase, Depends(get_current_user)]
) -> list[UserOut]:
    """Route works for currently logged in user.
    - This route should be reserved
    for users with "admin" privileges (not implemented)
    - Returns a list of users of type: UserOut
    """
    users_list = await get_users()

    return users_list


@user_route.get("/me")
async def read_user_me(
    current_user: Annotated[UserBase, Depends(get_current_user)]
) -> UserOut:
    """Route works for currently logged in user.
    Returns the current user of type: UserOut
    """
    return current_user


@user_route.get("/my_things")
async def get_my_things(
    current_user: Annotated[UserBase, Depends(get_current_user)]
) -> list[MyThingOut]:
    """Route works for currently logged in user.
    Returns a list of "things" of type: MyThingOut
    """
    user = await UserBase.get(current_user.id, fetch_links=True)
    return user.things


# Update
@user_route.patch("/update")
async def update_user(
    update_data: UserUpdate,
    current_user: Annotated[UserBase, Depends(get_current_user)],
) -> UserOut:
    """Route works for currently logged in user.
    - It takes update data as a parameter of type: UserUpdate, and updates current user.
    - Returns updated user of type UserOut
    """
    updated_this = await update_user_data(update_data, current_user)
    return updated_this


# Delete
@user_route.delete("/me/remove")
async def delete_user(
    current_user: Annotated[UserBase, Depends(get_current_user)]
) -> Message:
    """
    Route deletes currently logged in user.
    """
    user_has_been_deleted = await delete_user_by_id(current_user.id)

    return user_has_been_deleted
