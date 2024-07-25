import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Header
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                    dbc.Col(dbc.NavbarBrand("Quinto Andar Clone", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
        ]
    ),
    color="dark",
    dark=True,
)

# Filters
filters = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="city-dropdown",
                        options=[
                            {"label": "São Paulo", "value": "SP"},
                            {"label": "Rio de Janeiro", "value": "RJ"},
                        ],
                        placeholder="Select a City",
                    ),
                    md=3,
                ),
                dbc.Col(
                    dcc.Input(id="min-price", type="number", placeholder="Min Price", className="mb-2"),
                    md=2,
                ),
                dbc.Col(
                    dcc.Input(id="max-price", type="number", placeholder="Max Price", className="mb-2"),
                    md=2,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="type-dropdown",
                        options=[
                            {"label": "Apartment", "value": "apartment"},
                            {"label": "House", "value": "house"},
                        ],
                        placeholder="Select Property Type",
                    ),
                    md=3,
                ),
                dbc.Col(
                    dbc.Button("Search", id="search-button", color="primary", className="mb-2"),
                    md=2,
                ),
            ]
        )
    ],
    className="my-4",
)

# Property Cards
property_cards = dbc.Container(id="property-cards", className="my-4")

# Layout
app.layout = html.Div(
    [
        header,
        filters,
        property_cards,
    ]
)

# Callback to update property cards based on filters
@app.callback(
    Output("property-cards", "children"),
    Input("search-button", "n_clicks"),
    [
        Input("city-dropdown", "value"),
        Input("min-price", "value"),
        Input("max-price", "value"),
        Input("type-dropdown", "value"),
    ],
)
def update_properties(n_clicks, city, min_price, max_price, property_type):
    # Dummy data for properties
    properties = [
        {
            "title": "Beautiful Apartment in São Paulo",
            "price": "R$ 3,000",
            "location": "São Paulo",
            "type": "apartment",
            "image": "/assets/property1.jpg",
        },
        {
            "title": "Spacious House in Rio de Janeiro",
            "price": "R$ 5,000",
            "location": "Rio de Janeiro",
            "type": "house",
            "image": "/assets/property2.jpg",
        },
    ]
    
    # Filtering logic (for demonstration, actual implementation would query a database)
    filtered_properties = [prop for prop in properties if (not city or prop["location"] == city) and
                                                      (not min_price or int(prop["price"].replace("R$", "").replace(",", "")) >= min_price) and
                                                      (not max_price or int(prop["price"].replace("R$", "").replace(",", "")) <= max_price) and
                                                      (not property_type or prop["type"] == property_type)]

    # Creating property cards
    cards = []
    for prop in filtered_properties:
        card = dbc.Card(
            [
                dbc.CardImg(src=prop["image"], top=True),
                dbc.CardBody(
                    [
                        html.H4(prop["title"], className="card-title"),
                        html.H6(prop["price"], className="card-subtitle"),
                        html.P(f"Location: {prop['location']}"),
                        html.P(f"Type: {prop['type']}"),
                    ]
                ),
            ],
            style={"width": "18rem"},
        )
        cards.append(dbc.Col(card, md=4))
    
    return dbc.Row(cards)

if __name__ == "__main__":
    app.run_server(debug=True)
