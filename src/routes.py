# flake8: noqa
from fastapi import APIRouter
router = APIRouter()
from src.crud.permissions.controllers import *
from src.crud.groups.controllers import *
from src.crud.users.controllers import *
from src.crud.companies.controllers import *
