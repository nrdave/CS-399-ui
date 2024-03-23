import streamlit as st
import data


def main():
    st.title("Inspect Individual Mirror")
    mirror_data = data.get_mirror_info()

    country_set = sorted({m["country"] for m in mirror_data})
    selected_countries = st.multiselect(
        "Select Mirror Country/Countries: ", list(country_set)
    )

    valid_mirrors = [
        m for m in mirror_data if m["country"] in selected_countries]

    selected_mirror = st.selectbox(
        "Select a mirror: ", valid_mirrors, format_func=lambda m: m["url"]
    )

    if selected_mirror:
        st.json(selected_mirror)


if __name__ == "__main__":
    main()
