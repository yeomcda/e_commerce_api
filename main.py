from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


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
