import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd


# Read in global data
gapminder = pd.read_csv("data/processed/gapminder_processed.csv")

txt_stl = {
    "width": "350px",
    "color": "#212121",
}

stat = dcc.RadioItems(
    id="stat",
    options=[
        {
            "label": "Life Expectancy",
            "value": "life_expectancy",
        },
        {
            "label": "Education Ratio",
            "value": "education_ratio",
        },
        {"label": "Population Density", "value": "pop_density"},
        {
            "label": "Child Mortality",
            "value": "child_mortality",
        },
        {"label": "Children per Woman", "value": "children_per_woman"},
    ],
    value="education_ratio",
    labelStyle={"display": "block"},
)


region = dcc.Dropdown(
    id="region",
    options=[{"label": reg, "value": reg} for reg in gapminder["region"].unique()],
    value=None,
    style=txt_stl,
)

sub_region = dcc.Dropdown(
    id="sub_region",
    value=None,
    style=txt_stl,
)


income_grp = dcc.Dropdown(
    id="income_grp",
    options=[
        {"label": reg, "value": reg}
        for reg in ["Low", "Lower middle", "Upper middle", "High"]
    ],
    value=None,
    style=txt_stl,
)


pop_size = dcc.RangeSlider(
    id="pop_size",
    min=1e4,
    max=1_500_000_000,
    value=[200_000_000, 1_100_000_000],
    step=1e7,
    marks={
        10_000: {"label": "10, 000", "style": {"color": "white"}},
        200_000_000: {"label": "200 M", "style": {"color": "white"}},
        500_000_000: {"label": "500 M", "style": {"color": "white"}},
        800_000_000: {"label": "0.8 B", "style": {"color": "white"}},
        1_100_000_000: {"label": "1.1 B", "style": {"color": "white"}},
        1_500_000_000: {"label": "1.5 B", "style": {"color": "white"}},
    },
)

year = dcc.RangeSlider(
    id="year",
    min=1950,
    max=2018,
    value=[1965, 2000],
    step=1,
    marks={
        1950: {"label": "1950", "style": {"color": "white"}},
        1965: {"label": "1965", "style": {"color": "white"}},
        1980: {"label": "1980", "style": {"color": "white"}},
        2000: {"label": "2000", "style": {"color": "white"}},
        2010: {"label": "2010", "style": {"color": "white"}},
        2018: {"label": "2018", "style": {"color": "white"}},
    },
)


five_countries = dcc.RadioItems(
    id="five_countries",
    options=[
        {
            "label": "Top 5 countries based on my selection",
            "value": "Top",
        },
        {
            "label": "Bottom 5 countries based on my selection",
            "value": "Bottom",
        },
    ],
    value="Bottom",
    labelStyle={"display": "block"},
)