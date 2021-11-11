import dash_bootstrap_components as dbc
import dash_html_components as html


def Navbar():
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/img/brand_img.png', height="40px")),
                        dbc.Col(dbc.NavbarBrand("Music Recommendations", href="/home", className="ml-2 text-center")),
                    ],
                ),
            ),
            dbc.NavItem(dbc.NavLink("Recommendations", href="/app", className="ml-2 text-center"),
                        style={'padding-left': '750px', 'color': 'black'}),
        ],
        sticky="top",
    )
    return navbar
