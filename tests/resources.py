"""Misc fixtures and helpers for all tests"""
import os
import pathlib

import dotenv

from fs.subfs import ClosingSubFS
import fs.path

from fs.datalake import DatalakeFS

tests_directory = pathlib.Path(__file__).resolve().parent

remote_test_folder = "/billy/test_datalakefs"

# Loading test environment vars
_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)

tenant_id = os.getenv("DL_TENANT_ID")
store_name = os.getenv("DL_STORE_NAME")
client_id = os.getenv("DL_CLIENT_ID")
client_secret = os.getenv("DL_CLIENT_SECRET")
username = os.getenv("DL_USERNAME")
password = os.getenv("DL_PASSWORD")


def make_fs_username():
    filesystem = DatalakeFS(tenant_id, store_name, username=username, password=password)
    filesystem.makedirs(remote_test_folder, recreate=True)
    return filesystem.opendir(remote_test_folder, factory=ClosingSubFS)


def make_fs_client_id():
    filesystem = DatalakeFS(tenant_id, store_name, client_id=client_id, client_secret=client_secret)
    filesystem.makedirs(remote_test_folder, recreate=True)
    return filesystem.opendir(remote_test_folder, factory=ClosingSubFS)
