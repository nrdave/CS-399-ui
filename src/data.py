import streamlit as st
from requests import get


def get_mirror_info():
    MIRROR_STATUS_URL = "https://archlinux.org/mirrors/status/json/"

    mirror_status = get(MIRROR_STATUS_URL, timeout=5).json()

    mirrors = mirror_status.get("urls")

    return mirrors
