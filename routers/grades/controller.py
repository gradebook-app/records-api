from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from helpers.db import get_db
from routers.auth.service import validateGenesisAuthToken
from routers.grades.dto import WidgetContentBodyDTO, WidgetContentDTO
from routers.grades.service import widget_content

router = APIRouter()


@router.post("/widget", response_model=WidgetContentDTO)
async def get_widget_content(
    body: WidgetContentBodyDTO,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    token, email, password = body.token, body.email, body.password

    if not await validateGenesisAuthToken(token):
        # TODO: If the token is invalid, attempt login with email and password

        # If the login fails, raise an HTTPException with status code 401
        raise HTTPException(status_code=401, detail="Genesis token expired or invalid")

    return await widget_content(token, "", db)
