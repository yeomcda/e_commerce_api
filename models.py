from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime


class MyAbstractBaseModel(Model):
    id = fields.IntField(pk=True, index=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        abstract = True


class User(MyAbstractBaseModel):
    username = fields.CharField(max_length=20, null=False, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        table = "user"


class Business(MyAbstractBaseModel):
    business_name = fields.CharField(max_length=20, null=False, unique=True)
    city = fields.CharField(max_length=100, null=False, default="Unspecified")
    region = fields.CharField(max_length=100, null=False, default="Unspecified")
    business_description = fields.TextField(null=True)
    logo = fields.CharField(max_length=200, null=False, default="default.jpg")
    owner = fields.ForeignKeyField("models.User", related_name="business")

    class Meta:
        table = "business"


class Product(MyAbstractBaseModel):
    name = fields.CharField(max_length=100, null=False, unique=True)
    category = fields.CharField(max_length=30, index=True)
    original_price = fields.DecimalField(max_digits=12, decimal_places=2)
    new_price = fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = fields.IntField()
    offer_expiration_date = fields.DateField(default=datetime.utcnow)
    product_image = fields.CharField(
        max_length=200, null=False, default="productDefault.jpg"
    )
    business = fields.ForeignKeyField("models.Business", related_name="products")

    class Meta:
        table = "product"


UserPydantic = pydantic_model_creator(User, name="User", exclude=("is_verified",))
UserInPydantic = pydantic_model_creator(
    User, name="UserIn", exclude=("is_verified", "join_date"), exclude_readonly=True
)
UserOutPydantic = pydantic_model_creator(User, name="UserOut", exclude=("password",))

BusinessPydantic = pydantic_model_creator(Business, name="Business")
BusinessInPydantic = pydantic_model_creator(
    Business, name="BusinessIn", exclude_readonly=True
)

ProductPydantic = pydantic_model_creator(Product, name="Product")
ProductInPydantic = pydantic_model_creator(
    Product, name="ProductIn", exclude=("percentage_discount", "id")
)
