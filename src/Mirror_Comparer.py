import streamlit as st
from data import get_mirror_info, normalize_times


def main():
    st.title("Arch Linux Mirror Comparer")

    try:
        mirror_data = get_mirror_info()

        country_set = sorted({m["country"] for m in mirror_data})
        selected_countries = st.multiselect(
            "Select Mirror Country/Countries: ", list(country_set)
        )

        # If no countries are selected, allow selecting any mirror
        if not selected_countries:
            selected_countries = list(country_set)

        valid_mirrors = [
            m for m in mirror_data if m["country"] in selected_countries]

        valid_keys = [
            k
            for k in mirror_data[0].keys()
            if isinstance(mirror_data[0][k], (int, float))
            and not isinstance(mirror_data[0][k], bool)
        ]

        selected_keys = st.multiselect("Select statistics", valid_keys)

        selected_mirrors = st.multiselect(
            "Select mirrors to compare",
            valid_mirrors,
            format_func=lambda m: m["url"],
        )

        if selected_mirrors:
            for key in selected_keys:
                st.subheader(key)
                if key == "delay":
                    (normalized_delays, units) = normalize_times(
                        [m["delay"] for m in selected_mirrors]
                    )
                    # fmt: off
                    data = {
                        m["url"]: n for m, n in
                        zip(selected_mirrors, normalized_delays)
                    }
                    # fmt: on
                    st.text("Units: " + units)
                else:
                    data = {m["url"]: m[key] for m in selected_mirrors}

                st.bar_chart(data)

    except ConnectionError:
        return


if __name__ == "__main__":
    main()
