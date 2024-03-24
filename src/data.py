import streamlit as st
from requests import get
from requests.exceptions import RequestException
from datetime import datetime
from dateutil import tz


# Arch Linux mirror checks generally run around every 7 minutes
@st.cache_data(show_spinner="Fetching data from archlinux.org", ttl=60 * 7)
def get_mirror_info() -> list:
    """Fetch current mirror data from archlinux.org/mirrors/status/json"""
    MIRROR_STATUS_URL = "https://archlinux.org/mirrors/status/json/"

    try:
        # Get mirror info
        mirror_status = get(MIRROR_STATUS_URL, timeout=5).json()

        if not mirror_status:
            raise ConnectionError("Unable to connect to archlinux.org")

        # Extract information about each mirror
        mirrors = mirror_status.get("urls")

        # Filter out mirrors with either a score of Null or completion_pct of
        # zero. These mirrors are likely not valid at the moment
        # fmt: off
        valid_mirrors = [
            m for m in mirrors if m["completion_pct"] > 0
            and m["score"] is not None
        ]
        # fmt: on

        # Convert completion_pct in the mirror info to an actual percent
        for m in valid_mirrors:
            m["completion_pct"] *= 100

        return valid_mirrors

    except (ConnectionError, RequestException):
        st.error("Failed to connect to archlinux.org")
        raise ConnectionError

    return []


def get_last_update(status: dict) -> str:
    if status["last_check"]:
        # Time zone conversion taken from
        # https://github.com/wolfpaulus/weather_ui/blob/main/app/data.py
        t = datetime.fromisoformat(status["last_check"])
        t = t.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
        return t.strftime("%A, %B %d, %Y, %-I:%M:%S %p %Z")

    return ""


def normalize_delays(delays: list[float]) -> list[float]:
    """
    Scale a list of delays based on the maximum delay

    delays should be a list of delay values (in seconds)
    """
    MINUTES = 60
    HOURS = 60 * MINUTES
    # Determine how to scale the delays based on the maximum delay
    if (max(delays)) >= 5 * HOURS:  # 5 hours -> convert to hours
        delays = [d / HOURS for d in delays]
    elif (max(delays)) >= 5 * MINUTES:  # 5 minutes -> convert to minutes
        delays = [d / MINUTES for d in delays]

    return delays
