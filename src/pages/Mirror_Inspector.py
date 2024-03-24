import streamlit as st
import data


def main():
    st.set_page_config(page_title="Inspect an Arch Linux Mirror Server")
    st.title("Inspect Individual Mirror")

    try:
        mirror_data = data.get_mirror_info()

        country_set = sorted({m["country"] for m in mirror_data})
        selected_countries = st.selectbox(
            "Select Mirror Country: ", list(country_set))

        # If no countries are selected, allow selecting any mirror
        if not selected_countries:
            selected_countries = list(country_set)

        valid_mirrors = [
            m for m in mirror_data if m["country"] in selected_countries]

        # Had to disable my formatter for this to get it to fit in 79
        # characters
        # fmt: off
        selected_mirror = st.selectbox(
            "Select a mirror: ",
            valid_mirrors,
            format_func=lambda m: m["url"],
            index=None
        )
        # fmt: on

        if selected_mirror:
            st.json(selected_mirror)

    except ConnectionError:
        return


if __name__ == "__main__":
    main()
