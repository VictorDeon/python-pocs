# flake8: noqa
from fastapi import APIRouter
router = APIRouter()
from src.crud.users.controllers.create import create_user
