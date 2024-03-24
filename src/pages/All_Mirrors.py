import streamlit as st
from requests import get
import data


def main():
    st.title("All Arch Linux Mirrors")
    try:
        mirror_data = data.get_mirror_info()

        selectable_keys = list(mirror_data[0].keys())

        # URL will always be included in the dataframe, so remove it from the
        # selectable options
        selectable_keys.remove("url")

        selected_key = st.multiselect(
            "Select statistics: ",
            selectable_keys,
            default=["score"],
        )

        # Prepend the selected keys list with URL so that the leftmost entry
        # in the table is the mirror's URL
        fields = ["url"] + selected_key

        st.dataframe(
            [
                {key: val for key, val in m.items() if key in fields}
                for m in mirror_data
            ],
            use_container_width=True,
        )
    except ConnectionError:
        return


if __name__ == "__main__":
    main()
