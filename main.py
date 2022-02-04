from fastapi import FastAPI, Request, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from authentication import get_hashed_password, verify_token
from models import *

# signals
from tortoise.signals import post_save, pre_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

from emails import *

# response classes
from fastapi.responses import HTMLResponse

# templates
from fastapi.templating import Jinja2Templates

app = FastAPI()


@pre_save(User)
async def pre_save_user(
    sender: "Type[User]", instance: User, using_db, update_fields
) -> None:
    print("pre_save_user")
    print(sender, instance, using_db, update_fields)


@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    print("create_business")
    if created:
        print("create_business: created")
        business_obj = await Business.create(
            business_name=instance.username, owner=instance
        )

        await BusinessPydantic.from_tortoise_orm(business_obj)
        # send the email
        await send_email([instance.email], instance)


@app.post("/registration")
async def user_registrations(user: UserInPydantic):
    print("registration")
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    print("before user create")
    user_obj = await User.create(**user_info)
    print("after user create")
    new_user = await UserPydantic.from_tortoise_orm(user_obj)

    return {"status": "ok", "data": f"Hello {new_user.username}"}


templates = Jinja2Templates(directory="templates")


@app.get("/verification", response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse(
            "verification.html", {"request": request, "username": user.username}
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/")
def index():
    return {"message": "hello world"}


register_tortoise(
    app,
    db_url="mysql://root:890720@localhost:3306/e_commerce",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
