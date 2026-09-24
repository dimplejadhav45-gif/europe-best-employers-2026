
import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Europe’s Best Employers 2026: Ranking by Financial Times",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "ft_europe_best_employers_2026.csv",
        encoding="utf-8-sig"
    )

    df.columns = df.columns.str.strip()
    return df

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("💼 Europe’s Best Employers 2026: Ranking by Financial Times")

st.write(
    "Explore Europe's Best Employers 2026 by country and industry."
)

st.caption(
    "Use the filters below to discover employers that match where "
    "and in which sector you want to work."
)

st.markdown(
    "📖 [Learn more about the survey methodology and the full ranking]"
    "(https://www.ft.com/content/4837bb92-8db3-4fe6-ada5-7f83c6486a14)"
)

st.divider()

# -----------------------------
# FILTERS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox(
        "🌍 Country",
        ["All"] + sorted(df["Country"].dropna().unique().tolist())
    )

# Filter dataset according to selected country
if country == "All":
    country_df = df.copy()
else:
    country_df = df[df["Country"] == country].copy()

with col2:
    industry = st.selectbox(
        "🏢 Industry",
        ["All"] + sorted(
            country_df["Industry"].dropna().unique().tolist()
        )
    )

with col3:
    search = st.text_input(
        "🔎 Search employer",
        placeholder="e.g. Airbus"
    )

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = country_df.copy()

if industry != "All":
    filtered_df = filtered_df[
        filtered_df["Industry"] == industry
    ]

if search:
    filtered_df = filtered_df[
        filtered_df["Name"]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]

# Sort by FT ranking
filtered_df = filtered_df.sort_values("Rank")

# -----------------------------
# KPIs
# -----------------------------
st.subheader("Results")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "Employers found",
    len(filtered_df)
)

kpi2.metric(
    "Industries",
    filtered_df["Industry"].nunique()
)

kpi3.metric(
    "Countries",
    filtered_df["Country"].nunique()
)

st.divider()

# -----------------------------
# RESULTS TABLE
# -----------------------------
if len(filtered_df) > 0:

    display_columns = [
        "Rank",
        "Name",
        "Final score",
        "Country",
        "Industry"
    ]

    available_columns = [
        col for col in display_columns
        if col in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[available_columns],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Rank": st.column_config.NumberColumn(
                "Rank",
                format="%d"
            ),
            "Name": st.column_config.TextColumn(
                "Employer"
            ),
            "Final score": st.column_config.NumberColumn(
                "Final Score",
                format="%.2f"
            ),
            "Country": st.column_config.TextColumn(
                "Country"
            ),
            "Industry": st.column_config.TextColumn(
                "Industry"
            )
        }
    )

else:
    st.warning(
        "No employers found for these filters. "
        "Try another country or industry."
    )

# -----------------------------
# ABOUT PROJECT
# -----------------------------
st.divider()

with st.expander("About this project"):

    st.write(
        """
        This interactive application was developed to make the
        Financial Times' Europe’s Best Employers 2026 ranking
        easier to explore.

        Users can filter employers by country and industry and
        search for individual companies, turning the original
        ranking into an interactive employer-discovery tool.

        The application was built using Python, Pandas and Streamlit.

        Project created by Dimple Jadhav.
        """
    )

    st.markdown(
        "[View the original Financial Times ranking and methodology]"
        "(https://www.ft.com/content/4837bb92-8db3-4fe6-ada5-7f83c6486a14)"
    )
