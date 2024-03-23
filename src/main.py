import streamlit as st
from requests import get
import data


def main():
    st.title("Arch Linux Mirrors")
    try:
        mirror_data = data.get_mirror_info()

        fields = st.multiselect(
            "Select data fields to display: ",
            list(mirror_data[0].keys()),
            default=["url", "score"],
        )

        st.dataframe(
            [
                {key: val for key, val in m.items() if key in fields}
                for m in mirror_data
            ],
            use_container_width=True,
        )
    except ConnectionError:
        st.text("Failed to connect to archlinux.org")


if __name__ == "__main__":
    main()
