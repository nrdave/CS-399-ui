import streamlit as st
from requests import get
import data


st.title("Arch Linux Mirrors")
st.table(data.get_mirror_info())
