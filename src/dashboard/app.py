import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
from vega_datasets import data as datasets

# import controls as ctrs
from src.dashboard import controls as ctrs

# Read in global data
gapminder = pd.read_csv("data/processed/gapminder_processed.csv", parse_dates=["year"])

# Create dictionary for stat labels
labels = {
    "life_expectancy": "Life Expectancy",
    "education_ratio": "Education Ratio",
    "pop_density": "Population Density",
    "child_mortality": "Child Mortality",
    "children_per_woman": "Children per Woman",
}

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


controls = dbc.Card(
    [
        # control panel title
        html.H2("Control Panel", className="text-center"),
        # filter for Statistic of Interest
        html.Hr(),
        dbc.FormGroup(
            [
                html.H5("1. Statistic of Interest", className="text-left"),
                ctrs.stat,
            ]
        ),
        html.Hr(),
        # filter for Region
        dbc.FormGroup(
            [
                html.H5("2. Region", className="text-left"),
                ctrs.region,
            ]
        ),
        html.Hr(),
        # filter for Sub Region
        dbc.FormGroup(
            [html.H5("3. Sub Region", className="text-left"), ctrs.sub_region]
        ),
        html.Hr(),
        # filter for Income Group
        dbc.FormGroup(
            [html.H5("4. Income Group", className="text-left"), ctrs.income_grp]
        ),
        html.Hr(),
        # filter for population size
        dbc.FormGroup(
            [html.H5("5. Population Size", className="text-left"), ctrs.pop_size]
        ),
        html.Hr(),
        # filter for year
        dbc.FormGroup([html.H5("6. Year", className="text-left"), ctrs.year]),
        html.Hr(),
        # filter for year
        dbc.FormGroup([html.H5("7. Show me", className="text-left"), ctrs.top_btm]),
        html.Small(
            "*Education Ratio calculated as # of years in school men / # of years in school women. Higher values indicate larger gap between the education levels for men and women."
        ),
    ],
    color="secondary",
    inverse=True,
    body=True,
)

world_map = html.Iframe(
    id="world_map",
    style={
        "border-width": "0",
        "width": "100%",
        "height": "600px",
    },
)

bar = html.Iframe(
    id="bar",
    style={
        "border-width": "0",
        "width": "100%",
        "height": "400px",
    },
)

line = html.Iframe(
    id="line",
    style={
        "border-width": "0",
        "width": "100%",
        "height": "400px",
    },
)

app.layout = dbc.Container(
    [
        html.Div(
            style={
                "textAlign": "center",
                "color": "DarkSlateGray",
                "font-size": "26px",
            },
            children=[
                html.H1("GapExpresser"),
            ],
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(
                    [
                        dbc.Row(world_map, align="center"),
                        dbc.Row([dbc.Col([bar], md=6), dbc.Col([line], md=6)]),
                        html.Small(
                            "Note: empty plots mean that we don't have data based on your selection"
                        ),
                    ],
                    md=8,
                ),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


# Set up callbacks/backend
@app.callback(
    Output("sub_region", "options"),
    Input("region", "value"),
)
def get_subregion(region):
    if region is not None:
        subs = gapminder[gapminder["region"] == region]["sub_region"].unique()
        opts = []
        for s in subs:
            opts.append({"label": s, "value": s})
    else:
        opts = [
            {"label": sub_reg, "value": sub_reg}
            for sub_reg in gapminder["sub_region"].unique()
        ]
    return opts


# Set up callbacks/backend
@app.callback(
    Output("world_map", "srcDoc"),
    Input("stat", "value"),
    Input("region", "value"),
    Input("sub_region", "value"),
    Input("income_grp", "value"),
    Input("year", "value"),
)
def plot_map(stat, region, sub_region, income_grp, year):
    alt.data_transformers.disable_max_rows()

    # filter by Region, sub-region & Income group
    data = filter_data(region, sub_region, income_grp)

    # filter on year
    data = data[(data["year"] == f"{year[1]}")]

    # create world_map
    world_map = alt.topo_feature(datasets.world_110m.url, "countries")

    map_chart = (
        alt.Chart(world_map, title=f"{labels[stat]} by Country for {year[1]}")
        .mark_geoshape()
        .transform_lookup(
            lookup="id", from_=alt.LookupData(data, key="id", fields=["name", stat])
        )
        .encode(
            tooltip=["name:O", stat + ":Q"],
            color=alt.Color(stat + ":Q", title=f"{labels[stat]}"),
        )
        .project(type="equalEarth")
        .properties(width=1400, height=500)
    )
    return map_chart.to_html()


@app.callback(
    Output("bar", "srcDoc"),
    Input("stat", "value"),
    Input("region", "value"),
    Input("sub_region", "value"),
    Input("income_grp", "value"),
    Input("top_btm", "value"),
    Input("year", "value"),
)
def plot_bar(stat, region, sub_region, income_grp, top_btm, year):
    alt.data_transformers.disable_max_rows()

    # filter by Region, sub-region & Income group
    data = filter_data(region, sub_region, income_grp)

    # filter on year
    data = data[(data["year"] == f"{year[1]}")]

    # filter on top/bottom selection
    data = get_topbtm_data(data, stat, top_btm, year)

    chart = (
        alt.Chart(
            data,
            title=f"{labels[stat]} - {top_btm} 5 Countries for {year[1]}",
        )
        .mark_bar()
        .encode(
            y=alt.Y("country", sort="-x", title="Country"),
            x=alt.X(stat, title=labels[stat]),
            color=alt.Color("country", title="Country"),
            tooltip=("name:O", stat + ":Q"),
        )
        .properties(width=400, height=300)
    )
    return chart.to_html()


@app.callback(
    Output("line", "srcDoc"),
    Input("stat", "value"),
    Input("region", "value"),
    Input("sub_region", "value"),
    Input("income_grp", "value"),
    Input("top_btm", "value"),
    Input("year", "value"),
)
def plot_line(stat, region, sub_region, income_grp, top_btm, year):
    alt.data_transformers.disable_max_rows()

    # filter by Region, sub-region & Income group
    data = filter_data(region, sub_region, income_grp)

    # filter on top/bottom selection
    data = get_topbtm_data(data, stat, top_btm, year)

    # filter on year
    data = data[(data["year"] >= f"{year[0]}") & (data["year"] <= f"{year[1]}")]

    zoom = alt.selection_interval(
        bind="scales",
        on="[mousedown[!event.shiftKey], mouseup] > mousemove",
        translate="[mousedown[!event.shiftKey], mouseup] > mousemove!",
    )

    line = (
        alt.Chart(
            data,
            title=f"{labels[stat]} Trend - {top_btm} 5 Countries from {year[0]} - {year[1]}",
        )
        .mark_line()
        .encode(
            alt.X("year:T", title="Year"),
            alt.Y(stat, title=labels[stat]),
            color=alt.Color("country", sort="-y", title="Country"),
            tooltip=("name:O", stat + ":Q"),
        )
        .properties(width=400, height=300)
    ).add_selection(zoom)

    return line.to_html()


def get_topbtm_data(data, stat, top_btm, year):

    top_countries = list(
        data[data["year"] == f"{year[1]}"]
        .sort_values(by=stat, ascending=False)["country"]
        .head()
    )

    btm_countries = list(
        data[data["year"] == f"{year[1]}"]
        .sort_values(by=stat, ascending=True)["country"]
        .head()
    )

    if top_btm == "Top":
        data = data.query("country == @top_countries")
    else:
        data = data.query("country == @btm_countries")
    return data


def filter_data(region, sub_region, income_grp):
    if region is not None and sub_region is not None and income_grp is not None:
        data = gapminder[
            (gapminder["region"] == region)
            & (gapminder["sub_region"] == sub_region)
            & (gapminder["income_group"] == income_grp)
        ]
    elif region is not None and sub_region is None and income_grp is None:
        data = gapminder[(gapminder["region"] == region)]
    elif region is None and sub_region is not None and income_grp is None:
        data = gapminder[(gapminder["sub_region"] == sub_region)]
    elif region is None and sub_region is None and income_grp is not None:
        data = gapminder[(gapminder["income_group"] == income_grp)]
    elif region is not None and sub_region is not None and income_grp is None:
        data = gapminder[
            (gapminder["region"] == region) & (gapminder["sub_region"] == sub_region)
        ]
    elif region is None and sub_region is not None and income_grp is not None:
        data = gapminder[
            (gapminder["sub_region"] == sub_region)
            & (gapminder["income_group"] == income_grp)
        ]
    elif region is not None and sub_region is None and income_grp is not None:
        data = gapminder[
            (gapminder["region"] == region) & (gapminder["income_group"] == income_grp)
        ]
    else:
        data = gapminder
    return data


if __name__ == "__main__":
    app.run_server(debug=True)