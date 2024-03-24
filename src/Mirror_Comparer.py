import streamlit as st
from requests import get
from data import get_mirror_info


def main():
    st.title("Arch Linux Mirrors")

    try:
        mirror_data = get_mirror_info()

        country_set = sorted({m["country"] for m in mirror_data})
        selected_countries = st.multiselect(
            "Select Mirror Country/Countries: ", list(country_set)
        )

        valid_mirrors = [
            m for m in mirror_data if m["country"] in selected_countries]

        valid_keys = [
            k
            for k in mirror_data[0].keys()
            if isinstance(mirror_data[0][k], (int, float))
            and not isinstance(mirror_data[0][k], bool)
        ]

        selected_keys = st.multiselect(
            "Select data values to compare", valid_keys)

        selected_mirrors = st.multiselect(
            "Select mirrors to compare",
            valid_mirrors,
            format_func=lambda m: m["url"],
        )

        for key in selected_keys:
            data = {m["url"]: m[key] for m in selected_mirrors}

            st.subheader(key)
            st.bar_chart(data)

    except ConnectionError:
        return


if __name__ == "__main__":
    main()