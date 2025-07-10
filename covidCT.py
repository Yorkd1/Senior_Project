import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("covid19.csv", parse_dates=["date"])

# Keep only 2020-2022
df = df[(df["date"].dt.year >= 2020) & (df["date"].dt.year <= 2022)]

# Clean FIPS codes
df["fips"] = (
    df["fips"]
    .fillna(0)
    .astype(int)
    .astype(str)
    .str.zfill(5)
)

# ---------- 1)  SORT FIRST  ----------
df_sorted = (
    df.sort_values(["date", "fips"], kind="mergesort")  # stable sort
      .reset_index(drop=True)
)

# ---------- 2)  THEN GROUP, *without* resorting ----------
county_df_sorted = (
    df_sorted
      .groupby(["date", "fips"], as_index=False, sort=False)["cases"]
      .sum()
)

# ---------- 3)  STRING VERSION OF DATE FOR ANIMATION ----------
county_df_sorted["date_str"] = county_df_sorted["date"].dt.strftime("%Y-%m-%d")

# ---------- 4)  PLOT ----------
fig = px.choropleth(
    county_df_sorted,
    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
    locations="fips",
    color="cases",
    color_continuous_scale="Reds",
    scope="usa",
    animation_frame="date_str",      # uses the string column
    labels={"cases": "Total Cases"},
)

fig.update_layout(
    title_text="COVID-19 Cases by US County (2020 – 2022)",
)
fig.show()

