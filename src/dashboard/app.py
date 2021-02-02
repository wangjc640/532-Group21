"""
This file contains all the components of the dashboard including layout,
control filters and altair plots. 
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
from vega_datasets import data as datasets

import controls as ctrs
#from src.dashboard import controls as ctrs

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
            "* Education Ratio calculated as # of years in school men / # of years in school women. Higher values indicate larger gap between the education levels for men and women."
        ),
        html.Small(
            "** Population Density (per square km).  Average number of people on each square km of land in the given country. "
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
    """Select sub regions to display based on region filter selection

    Parameters
    --------
    region: string
        Selection from the Region filter

    Returns
    --------
        Options list for sub region belonging to the selected region

    Example
    --------
    > get_subregion("Asia")
    """
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
    """
    Create map plot for statsitic of interested based on selected filters

    Parameters
    --------
    stat: string
        Selection from statistic of interest filter
    region: string
        Selection from the Region filter
    sub_region: sting
        Selection from Sub Region filter
    income_grp: string
        Selection from Income Group filter
    year: integer
        Year for which the data is displayed, from Year filter

    Returns
    --------
    map_chart
        map chart showing statistic of interest for specific region, subregion, income group and year

    Example
    --------
    > plot_map("education_ratio", "Asia", "Western Asia", "Lower middle", [1968, 2015])
    """
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
        .configure_title(fontSize=17)
        .configure_legend(labelFontSize=12)
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
    """
    Create bar chart for statsitic of interested based on selected filters, for top 5 or bottom 5 countries

    Parameters
    --------
    stat: string
        Selection from statistic of interest filter
    region: string
        Selection from the Region filter
    sub_region: sting
        Selection from Sub Region filter
    income_grp: string
        Selection from Income Group filter
    top_btm: string
        Selection from Top/Bottom filter
    year: integer
        Year for which the data is displayed, from Year filter

    Returns
    --------
    chart
        bar chart showing statistic of interest for top 5 or bottom 5 countries,
        in specific region, subregion, income group and year

    Example
    --------
    > plot_bar("education_ratio", "Asia", "Western Asia", "Lower middle", "Bottom", [1968, 2015])
    """
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
        .configure_axis(labelFontSize=12,  titleFontSize=14)
        .configure_title(fontSize=15)
        .configure_legend(labelFontSize=12)
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
    """
    Create line chart for statsitic of interested based on selected filters, for top 5 or bottom 5 countries

    Parameters
    --------
    stat: string
        Selection from statistic of interest filter
    region: string
        Selection from the Region filter
    sub_region: sting
        Selection from Sub Region filter
    income_grp: string
        Selection from Income Group filter
    top_btm: string
        Selection from Top/Bottom filter
    year: integer
        Year for which the data is displayed, from Year filter

    Returns
    --------
    line
        line chart showing statistic of interest for top 5 or bottom 5 countries,
        in specific region, subregion, income group and year range

    Example
    --------
    > plot_line("education_ratio", "Asia", "Western Asia", "Lower middle", "Bottom", [1968, 2015])
    """
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
        .configure_axis(labelFontSize=12,  titleFontSize=14)
        .configure_title(fontSize=15)
        .configure_legend(labelFontSize=12)
        .properties(width=400, height=300)
    ).add_selection(zoom)

    return line.to_html()


def get_topbtm_data(data, stat, top_btm, year):
    """
    Filter data based on top 5 or bottom 5 countries selection

    Parameters
    --------
    data: pandas dataframe
        Data to be filtered
    stat: string
        Selection from statistic of interest filter
    top_btm: string
        Selection from Top/Bottom filter
    year: integer
        Year for which the data is displayed, from Year filter

    Returns
    --------
    data
        dataset that has been filtered by top 5 or bottom 5 countries

    Example
    --------
    > get_topbtm_data(data, "education_ratio", "Bottom", [1968, 2015])
    """
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
    """
    Filter data based on region, sub region and income group selection

    Parameters
    --------
    region: string
        Selection from the Region filter
    sub_region: sting
        Selection from Sub Region filter
    income_grp: string
        Selection from Income Group filter

    Returns
    --------
    data
        dataset that has been filtered on region, sub region and income group selection

    Example
    --------
    > filter_data(d"Asia", "Western Asia", "Lower middle")
    """
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