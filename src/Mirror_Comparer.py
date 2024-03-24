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

                BAR_GOOD_COLOR = "#00a9ff"
                BAR_BAD_COLOR = "#ff2a00"

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

                        # fmt: off
                        chart = (
                            alt.Chart(data)
                            .mark_bar()
                            .encode(
                                x="Mirror",
                                y=delay_label,
                                color=alt.condition(
                                    alt.datum[delay_label]
                                    > max_acceptable_delay,
                                    alt.value(BAR_BAD_COLOR),
                                    alt.value(BAR_GOOD_COLOR),
                                ),
                            )
                        )
                        # fmt: on

                        st.altair_chart(chart, use_container_width=True)

                    case "completion_pct":
                        data = pd.DataFrame(
                            {
                                "Mirror": [m["url"] for m in selected_mirrors],
                                "Completion Percent": [
                                    m[key] for m in selected_mirrors
                                ],
                            }
                        )

                        st.caption(
                            (
                                '"The number of mirror checks that have '
                                "successfully connected and disconnected "
                                "from the given URL. If this is below 100%, "
                                'the mirror may be unreliable." - '
                                "archlinux.org. "
                                "\n\nCompletion Percents below 100% are drawn"
                                " as red to indicate that the mirror should "
                                "not be used"
                            )
                        )

                        chart = (
                            alt.Chart(data)
                            .mark_bar()
                            .encode(
                                x="Mirror",
                                y="Completion Percent",
                                color=alt.condition(
                                    alt.datum["Completion Percent"] < 100,
                                    alt.value(BAR_BAD_COLOR),
                                    alt.value(BAR_GOOD_COLOR),
                                ),
                            )
                        )

                        st.altair_chart(chart, use_container_width=True)

                    case "score":
                        st.caption(
                            (
                                '"A very rough calculation for ranking '
                                "mirrors. It is currently calculated as "
                                "(hours delay + average duration + standard "
                                "deviation) / completion percentage. Lower "
                                'is better." - archlinux.org'
                            )
                        )

                        data = {m["url"]: m[key] for m in selected_mirrors}

                        st.bar_chart(data, color=BAR_GOOD_COLOR)

                    case "duration_avg":
                        st.caption(
                            (
                                '"The average (mean) time it took to connect '
                                "and retrieve the lastsync file from the "
                                "given URL. Note that this connection "
                                "time is from the location of the Arch "
                                "server; your geography may product "
                                'different results." - archlinux.org.'
                            )
                        )

                        data = {m["url"]: m[key] for m in selected_mirrors}

                        st.bar_chart(data, color=BAR_GOOD_COLOR)

                    case "duration_stddev":
                        st.caption(
                            (
                                '"The standard deviation of the time it took '
                                "to connect and retrieve the lastsync file "
                                "from the given URL. Note that this "
                                "connection time is from the location of "
                                "the Arch server; your geography may product "
                                'different results." - archlinux.org.'
                            )
                        )

                        data = {m["url"]: m[key] for m in selected_mirrors}

                        st.bar_chart(data, color=BAR_GOOD_COLOR)
                    case _:
                        data = {m["url"]: m[key] for m in selected_mirrors}

                        st.bar_chart(data, color=BAR_GOOD_COLOR)

    except ConnectionError:
        return


if __name__ == "__main__":
    main()
