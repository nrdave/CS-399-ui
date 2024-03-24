import streamlit as st
from data import get_mirror_info, normalize_times
import pandas as pd
import altair as alt


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
                match key:
                    case "delay":
                        (normalized_delays, units) = normalize_times(
                            [m["delay"] for m in selected_mirrors]
                        )

                        match units:
                            case "hours":
                                delay_label = "Delay (hours)"
                                max_acceptable_delay = 1
                            case "minutes":
                                delay_label = "Delay (minutes)"
                                max_acceptable_delay = 60
                            case _:
                                delay_label = "Delay (seconds)"
                                max_acceptable_delay = 60 * 60

                        data = pd.DataFrame(
                            {
                                "Mirror": [m["url"] for m in selected_mirrors],
                                delay_label: normalized_delays,
                            }
                        )
                        print(data)

                        st.caption(
                            (
                                "A measure of the average difference between "
                                "the last sync time and last mirror check "
                                'for each mirror. "Due to the timing of '
                                "mirror checks, any value under one hour "
                                'should be viewed as ideal." - archlinux.org.'
                                "\n\nDelays over 1 hour are drawn as red to "
                                "indicate that they should not be used."
                            )
                        )

                        chart = (
                            alt.Chart(data)
                            .mark_bar()
                            .encode(
                                x="Mirror",
                                y=delay_label,
                                color=alt.condition(
                                    alt.datum[delay_label] > max_acceptable_delay,
                                    alt.value("#ff2a00"),
                                    alt.value("#00a9ff"),
                                ),
                            )
                        )

                        st.altair_chart(chart, use_container_width=True)

    except ConnectionError:
        return


if __name__ == "__main__":
    main()
