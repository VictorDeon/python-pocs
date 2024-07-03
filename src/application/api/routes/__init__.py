# flake8: noqa
# pylint: disable=wrong-import-position
from fastapi import APIRouter
router = APIRouter()
from .blocked_requests import *
from .pdf_generator import *
from .pdf_reader import *
from .list_pokemons import list_pokemons
from .find_pokemon import *
from .list_permissions import list_permission
from .create_permission import create_permission
from .retrieve_permission import retrieve_permission
from .update_permission import update_permission
from .delete_permissions import delete_permission
from .list_groups import list_groups
from .create_group import create_group
from .retrieve_group import retrieve_group
from .update_group import update_group
from .delete_group import delete_group
from .list_companies import list_companies
from .create_company import create_company
from .retrieve_company import retrieve_company
from .update_company import update_company
from .delete_company import delete_company
from .list_users import list_user
from .create_user import create_user
from .retrieve_user import retrieve_user
from .update_user import update_user
from .delete_user import delete_user
