from typing import Annotated

from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from api.db import DB
from api.logger import logger
from api.utils import is_valid_api_key, get_username
from api.models import UpdateBalanceRequest
from bank_config import DEFAULT_BALANCE


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
app = FastAPI()
db = DB()


@app.post("/v1/set_balance")
async def set_balance(
    request_data: UpdateBalanceRequest, api_key: Annotated[str, Depends(oauth2_scheme)]
):
    if not is_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    username = request_data.owner_username
    new_balance = request_data.new_balance

    result = db.execute_query(
        "UPDATE cards SET balance = %s WHERE owner_username = %s",
        (
            new_balance,
            username,
        ),
    )

    if result is not False:
        return True

    return False


@app.get("/v1/create_balance")
async def create_balance(api_key: Annotated[str, Depends(oauth2_scheme)]):
    if not is_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    username = get_username(api_key)

    result = db.execute_query(
        "INSERT INTO cards (owner_username, balance) VALUES (%s, %s);",
        [username, DEFAULT_BALANCE],
    )

    return result


@app.get("/v1/get_balance")
async def get_balance(api_key: Annotated[str, Depends(oauth2_scheme)]):
    if not is_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    username = get_username(api_key)

    result = db.execute_query(
        "SELECT balance FROM cards WHERE owner_username = %s;", (username,)
    )

    if result == []:
        raise HTTPException(status_code=404, detail="User not found")

    return result[0]
