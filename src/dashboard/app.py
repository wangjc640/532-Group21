import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import controls as ctrs

# Read in global data
gapminder = pd.read_csv("data/processed/world-data-gapminder_processed.csv")

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


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
    ],
    color="secondary",
    inverse=True,
    body=True,
)

bar = html.Iframe(
    id="bar",
    style={
        "border-width": "0",
        "width": "100%",
        "height": "800px",
    },
)

line = html.Iframe(
    id="line",
    style={
        "border-width": "0",
        "width": "100%",
        "height": "800px",
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
                        dbc.Row(dbc.Col(dcc.Graph(id="cluster-graph2"))),
                        dbc.Row(
                            [
                                dbc.Col([bar], md=6),
                                dbc.Col([line], md=6),
                            ]
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
    subs = gapminder[gapminder["region"] == region]["sub_region"].unique()
    opts = []
    for s in subs:
        opts.append({"label": s, "value": s})
    return opts


# Set up callbacks/backend
@app.callback(
    Output("bar", "srcDoc"),
    Input("stat", "value"),
    Input("region", "value"),
    Input("sub_region", "value"),
    Input("income_grp", "value"),
    Input("pop_size", "value"),
    Input("year", "value"),
)
def plot_bar(stat, region, sub_region, income_grp, pop_size, year):
    chart = (
        alt.Chart(gapminder)
        .mark_bar()
        .encode(y=alt.Y("country", sort="-x"), x=stat, color="country")
        .transform_window(
            rank="rank(stat)",
            sort=[alt.SortField(stat, order="descending")],
        )
        .transform_filter((alt.datum.rank < 6))
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)