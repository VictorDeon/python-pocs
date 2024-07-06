# flake8: noqa
from fastapi import APIRouter
router = APIRouter()
from .users.controllers.create import create_user
