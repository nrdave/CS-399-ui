import streamlit as st
from requests import get

mirror_status = get(
    "https://archlinux.org/mirrors/status/json/", timeout=5).json()

mirrors = mirror_status.get("urls")
st.title("Arch Linux Mirrors")
st.table(mirrors)
