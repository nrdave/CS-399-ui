import streamlit as st
from requests import get


# Arch Linux mirror checks generally run around every 7 minutes
@st.cache_data(show_spinner="Fetching data from archlinux.org", ttl=60 * 7)
def get_mirror_info():
    """Fetch current mirror data from archlinux.org/mirrors/status/json"""
    MIRROR_STATUS_URL = "https://archlinux.org/mirrors/status/json/"

    try:
        # Get mirror info
        mirror_status = get(MIRROR_STATUS_URL, timeout=5).json()

        # Extract information about each mirror
        mirrors = mirror_status.get("urls")

        # Filter out mirrors with either a score of Null or completion_pct of
        # zero. These mirrors are likely not valid at the moment
        valid_mirrors = [
            m for m in mirrors if m["completion_pct"] > 0 and m["score"] is not None
        ]

        # Convert completion_pct in the mirror info to an actual percent
        for m in valid_mirrors:
            m["completion_pct"] *= 100

    except OSError as err:
        st.error(str(err))

    return valid_mirrors
