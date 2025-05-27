from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObjectId = Annotated[str, BeforeValidator(str)]


class MongoIdModel(BaseModel):
    """
    A Pydantic model that represents a MongoDB document with an optional ObjectId field.

    Attributes:
        id (Optional[PyObjectId]): The unique identifier for the document, mapped from the MongoDB "_id" field.

    Config:
        populate_by_name (bool): Allows population of fields by their name as well as by alias.
        arbitrary_types_allowed (bool): Allows arbitrary types (such as custom PyObjectId) to be used as field types.
    """

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class FlexibleModel(MongoIdModel):
    """
    Modelo flexible que permite atributos adicionales
    """
    model_config = ConfigDict(
        extra="allow",  # Permite atributos adicionales
    )


class APIResponse(BaseModel):
    """
    Modelo de respuesta de la API
    """
    code: int
    status: str
    message: str
    data: Optional[dict] = None
