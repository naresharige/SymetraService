from pydantic import BaseModel
from typing import List


class Subcategory(BaseModel):
    name: str  # The name of the subcategory.


class Product(BaseModel):
    name: str  # The name of the product.
    subcategories: List[Subcategory]  # List of subcategories associated with the product.


class Category(BaseModel):
    name: str  # The name of the category.
    products: List[Product]  # List of products associated with the category.


class ProductsResponse(BaseModel):
    categories: List[Category]  # List of categories containing products.
