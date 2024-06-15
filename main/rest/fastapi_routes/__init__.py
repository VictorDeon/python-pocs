# flake8: noqa
# pylint: disable=wrong-import-position
from fastapi import APIRouter
router = APIRouter()
from .not_blocked_requests import (
    blocking_request1,
    blocking_request2,
    not_blocking_request1,
    not_blocking_request2,
    not_blocking_request3
)
from .pdf_generator import create_invoice
from .pdf_reader import list_invoices
from .retrieve_user import retrieve_user

__all__ = ["router"]