import dash_mantine_components as dmc
from dash import Input, Output, clientside_callback
from dash_iconify import DashIconify


def create_home_link(label: str) -> dmc.Anchor:
    icon = DashIconify(icon="carbon:satellite-radar", inline=True)
    return dmc.Anchor(
        [icon, " ", label],
        size="xl",
        href="/",
        underline=False,
    )


def create_header_link(
    icon: str, href: str, size: int = 22, color: str = "indigo"
) -> dmc.Anchor:
    return dmc.Anchor(
        dmc.ThemeIcon(
            DashIconify(
                icon=icon,
                width=size,
            ),
            variant="outline",
            radius=30,
            size=36,
            color=color,
        ),
        href=href,
        target="_blank",
    )


def create_header(nav_data: list | dict) -> dmc.Header:
    # NOTE: extract first item if nav_data is returned as a nested list
    # template copied from https://github.com/snehilvj/dmc-docs/
    # but there are no nested pages
    try:
        next(iter(nav_data))["name"]
    except TypeError:
        nav_data = nav_data[0]
    finally:
        _select_list = [
            {
                "label": component["name"],
                "value": component["path"],
            }
            for component in nav_data
            if component["name"] not in ["Home", "Not found 404"]
        ]

    return dmc.Header(
        height=70,
        fixed=True,
        px=25,
        children=[
            dmc.Stack(
                justify="center",
                style={"height": 70},
                children=dmc.Grid(
                    children=[
                        dmc.Col(
                            [
                                dmc.MediaQuery(
                                    create_home_link("FlowEHR"),
                                    styles={"display": "none"},
                                ),
                            ],
                            span="content",
                            pt=12,
                        ),
                        # Create a search box and pre-populate with page names
                        dmc.Col(
                            span="auto",
                            children=dmc.Group(
                                position="right",
                                spacing="xl",
                                children=[
                                    dmc.MediaQuery(
                                        dmc.Select(
                                            id="select-component",
                                            style={"width": 250},
                                            placeholder="Search",
                                            nothingFound="No match found",
                                            searchable=True,
                                            clearable=True,
                                            data=_select_list,
                                            icon=DashIconify(
                                                icon="radix-icons:magnifying-glass"
                                            ),
                                        ),
                                        smallerThan=1200,
                                        styles={"display": "none"},
                                    ),
                                    create_header_link(
                                        "radix-icons:github-logo",
                                        "https://github.com/UCLH-Foundry/FlowEHR",
                                    ),
                                    create_header_link(
                                        "carbon:help", "https://www.flowehr.io/"
                                    ),
                                    dmc.MediaQuery(
                                        dmc.ActionIcon(
                                            DashIconify(
                                                icon="radix-icons:hamburger-menu",
                                                width=18,
                                            ),
                                            id="drawer-hamburger-button",
                                            variant="outline",
                                            size=36,
                                        ),
                                        largerThan=1500,
                                        styles={"display": "none"},
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )


clientside_callback(
    """ function(children) { return null } """,
    Output("select-component", "value"),
    Input("_pages_content", "children"),
)

clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "pathname"),
    Input("select-component", "value"),
)

clientside_callback(
    """function(n_clicks) { return true }""",
    Output("components-navbar-drawer", "opened"),
    Input("drawer-hamburger-button", "n_clicks"),
    prevent_initial_call=True,
)
