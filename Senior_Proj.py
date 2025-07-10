import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────────
# Data loading & preprocessing
# ──────────────────────────────────────────────────────────────────────────────

# Load COVID‑19 data
covid_df = pd.read_csv("covid19.csv", parse_dates=["date"])

# Keep only 2020‑2022 data
covid_df = covid_df[(covid_df["date"].dt.year >= 2020) & (covid_df["date"].dt.year <= 2022)]

# Clean FIPS codes
covid_df["fips"] = (
    covid_df["fips"].fillna(0).astype(int).astype(str).str.zfill(5)
)

# State abbreviations for the state‑level map
state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

covid_df["state_abbrev"] = covid_df["state"].map(state_abbrev)

# ──────────────────────────────────────────────────────────────────────────────
# State‑level dataset
# ──────────────────────────────────────────────────────────────────────────────
state_df = (
    covid_df.dropna(subset=["state_abbrev"])
            .groupby(["state_abbrev", "date"], as_index=False)[["cases", "deaths"]]
            .sum()
            .sort_values("date")
)

# ──────────────────────────────────────────────────────────────────────────────
# County‑level dataset
# ──────────────────────────────────────────────────────────────────────────────
county_sorted = (
    covid_df.dropna(subset=["fips"]).copy()
              .sort_values(["date", "fips"], kind="mergesort")  # stable sort
              .reset_index(drop=True)
)

county_df_sorted = (
    county_sorted.groupby(["date", "fips"], as_index=False, sort=False)[["cases", "deaths"]]
                 .sum()
)

# Add string version of the date for the animation frame – this guarantees
# that Plotly shows the very first frame for (2020‑01‑21)
county_df_sorted["date_str"] = county_df_sorted["date"].dt.strftime("%Y-%m-%d")

# ──────────────────────────────────────────────────────────────────────────────
#  Population data
# ──────────────────────────────────────────────────────────────────────────────

pop_df = pd.read_csv("us_pop_by_state.csv")

# ──────────────────────────────────────────────────────────────────────────────
#  Figure factories
# ──────────────────────────────────────────────────────────────────────────────

def get_covid_state_figure() -> go.Figure:
    """Animated state‑level COVID map (cases & deaths)."""
    df = state_df.copy()
    df["cases_clipped"] = df["cases"].clip(upper=800000)

    fig = px.choropleth(
        df,
        locations="state_abbrev",
        locationmode="USA-states",
        color="cases_clipped", 
        animation_frame="date",
        scope="usa",
        color_continuous_scale="Reds",
        labels={
            "cases_clipped": "Total Cases",
            "state_abbrev": "State",
            "deaths": "Total Deaths",
            "date": "Date"
        },
        hover_data={
        "cases": True,       
        "deaths": True,
        "cases_clipped": False  
    },
    )
    fig.update_layout(
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=800,
    )
    return fig


def get_covid_county_figure() -> go.Figure:
    """Animated county‑level COVID map using the pre‑sorted county_df_sorted."""

    df = county_df_sorted.copy()
    df["cases_clipped"] = df["cases"].clip(upper=10000)

    fig = px.choropleth(
        df,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations="fips",
        color="cases_clipped",
        color_continuous_scale="Reds",
        animation_frame="date_str",
        scope="usa",
        labels={
            "cases_clipped": "Total Cases",
            "fips": "County FIPS Code",
            "deaths": "Total Deaths",
            "date_str": "Date"
        },
        hover_data={
        "cases": True,
        "deaths": True,
        "cases_clipped": False
        }
    )

    fig.update_layout(
        geo_scope="usa",
        margin=dict(l=20, r=20, t=50, b=20),
        height=800,
    )

    return fig


def get_population_figure() -> go.Figure:
    """Static state‑level population map (2020 Census)."""
    fig = px.choropleth(
        pop_df,
        locations="state_code",
        locationmode="USA-states",
        color="2020_census",
        scope="usa",
        color_continuous_scale="Viridis",
        range_color=(1_000_000, 40_000_000),
        labels={"2020_census": "Population",
                "state_code": "State Code"},
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        height=700,
    )
    return fig

# ──────────────────────────────────────────────────────────────────────────────
#  Dash app
# ──────────────────────────────────────────────────────────────────────────────

app = dash.Dash(__name__)
app.title = "US Heatmaps"

app.layout = html.Div(
    [
        html.H1("US 2020-2022 Heatmaps", style={"textAlign": "center"}),

        html.Div(
    [
        html.P(
            "This dashboard visualizes US COVID‑19 data and population statistics from 2020 to 2022. "
            "Use the dropdown below to explore a static map of population by state based on the 2020 US Census, or " \
            "animated maps of COVID‑19 cases by state and county.",
            style={"maxWidth": "800px", "margin": "0 auto", "textAlign": "center", "fontSize": "18px"}
        )
    ],
    style={"marginBottom": "30px"}),

        html.Div(
            [
                dcc.Dropdown(
                    id="map-selector",
                    options=[
                        {"label": "COVID‑19 Cases by State", "value": "covid_state"},
                        {"label": "COVID‑19 Cases by County", "value": "covid_county"},
                        {"label": "2020 Population", "value": "population"},
                    ],
                    value="population",
                    clearable=False,
                    style={"width": "300px", "margin": "0 auto"},
                )
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        dcc.Loading(
            id="loading-spinner",
            type="circle",
            color="#666",
            children=[dcc.Graph(id="map-graph")]
        ),
    ],
    style={"padding": "40px"},
)


@app.callback(Output("map-graph", "figure"), Input("map-selector", "value"))
def update_graph(selected_map: str):
    if selected_map == "covid_state":
        return get_covid_state_figure()
    elif selected_map == "covid_county":
        return get_covid_county_figure()
    else:
        return get_population_figure()


if __name__ == "__main__":
    app.run(debug=True)