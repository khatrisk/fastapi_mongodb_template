from fastapi import HTTPException, status

from beanie import UpdateResponse

from models.user_model import UserIn, UserBase
from models.thing_model import MyThing
from models.message_models import Message
from auth.password_hasher import get_password_hash


async def create_user(user: UserIn):
    """This function verifies that neither the username nor email passed in as
    'user' parameters, exist in the database.

    if user doesn't already exist, it takes this information information and
    passes it to the to the add_params() function.

    It creates a new user.
    """

    user_email = await UserBase.find_one({"email": user.email})
    user_username = await UserBase.find_one({"username": user.username})
    if user_email is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="user with that email already exists"
        )
    if user_username is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="user with that username already exists"
        )

    with_added_information = add_params(user)

    saved_user = await UserBase.create(with_added_information)
    return saved_user


def add_params(user_in: UserIn):
    """This function, takes the information passed in from 'create_user' and
    additionally generates:
    • hashed_password
    • uri to a generic avatar image

    It creates a user_dict excluding the password passed through 'UserIn' and
    register the new user.

    """
    hashed_password = get_password_hash(user_in.password)
    user_dict = user_in.dict(exclude={"password"})

    user_name = user_dict["username"]
    uri = f"https://api.multiavatar.com/{user_name}.png"
    avatar_dict = {"public_id": None, "uri": uri}
    user = UserBase(
        email=user_dict["email"],
        username=user_dict["username"],
        password_hash=hashed_password,
        avatar=avatar_dict,
    )
    return user


async def add_something_to_user(thing, user):
    """Function takes in a "thing" of type MyThingIn, and a "user" which is the
    "current_user" dependency.

    It creates a new instance of "thing", saves it, then appends it to the list
    of things owned by the user.
    """
    # Make a new thing instance
    new_thing = MyThing(
        thing_name=thing.thing_name, owner=user.username, category=thing.category
    )
    await MyThing.create(new_thing)

    # Get all the Thing document with fetch_links
    reveal_user_things = await UserBase.get(user.id, fetch_links=True)
    user_things = reveal_user_things.things

    # Get the names of the things the user has already
    user_things_names = []
    if user_things is not None:
        for existing in user_things:
            user_things_names.append(existing.thing_name)

    # Verify that the new thing  does not exist already
    if new_thing.thing_name in user_things_names:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="That thing already exists"
        )

    user.things.append(new_thing)
    await user.save()

    return user.things[-1]


async def get_user(id: str):
    """function takes the MongoDB document _id as a string, to search database.
    It has not yet been implemented. It should be limited to a user with "admin"
    privileges.
    """
    found = await UserBase.get(id)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return found


async def get_users():
    """function returns all users in the database as a list.
    Note: this function should be limited to a user with "admin" privileges
    """
    all_users = await UserBase.find().to_list()
    return all_users


async def update_user_data(user_update_data, current_user):
    """function updates the current_user with the data passed in the
    user_update_data object.
    """
    update_data = user_update_data.dict(exclude_unset=True)

    await UserBase.find_one(UserBase.id == current_user.id).update(
        {"$set": update_data}
    )
    updated_user = await UserBase.get(current_user.id)
    return updated_user


async def delete_user_by_id(id: str):
    """function takes the MongoDB document _id as a string, to search database
    for document and delete it.

    Note: this function should be limited to a user with "admin" privileges

    """
    success_message = Message(message="user deleted")
    user_found = await UserBase.get(id)

    if user_found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    await user_found.delete()
    return success_message
