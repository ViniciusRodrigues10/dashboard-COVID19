import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

df = pd.read_csv("HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")

# Pegando apenas dados dos estados do Brasil
df_states=df[(~df["estado"].isna()) & (df["codmun"].isna())] 
df_brasil=df[df["regiao"]== "Brasil"] 
df_states.to_csv("df_states.csv")
df_states.to_csv("df_brasil.csv")

df_states = pd.read_csv("df_states.csv")
df_states = pd.read_csv("df_brasil.csv")
df_data = df_states[df_states["estado"]=="RJ"]

# Data de início
df_states_ = df_states[df_states["data"] == "2020-05-13"]

# lendo o json
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# ======================== Instalação do Dash ========================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos", 
                           center={"lat": -16.95, "lon": -47.78}, zoom=4,
                           geojson=brazil_states, color_continuous_scale="Redor", opacity=0.4, 
                           hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True})

fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10,r=10,t=10,b=10)
)

# ======================== Construção Layout ========================
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url("logo_dark.png"), height=50),
                html.H5("Evolução COVID-19"),
                dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
            ], style={}),
            html.P("Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),
            html.Div(id="div-test", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brasil["data"].min(),
                    max_date_allowed=df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="MMMM D, YYYY",
                    style={"border": "0px solid black"}
                )
            ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Casos recuperados"),
                        html.H3(style={"color":"#adfc92"}, id="casos-recuperados-text"),
                        html.Span("Em acompanhamento"),
                        html.H5(id="em-acompanhamento-text"),
                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0)",
                                        "color": "#FFFFFF"})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Casos confirmados totais"),
                        html.H3(style={"color":"#389fd6"}, id="casos-confirmados-text"),
                        html.Span("Novos casos na data"),
                        html.H5(id="novos-casos-text"),
                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0)",
                                        "color": "#FFFFFF"})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Óbitos confirmados"),
                        html.H3(style={"color":"#DF2935"}, id="obitos-text"),
                        html.Span("Óbitos na data"),
                        html.H5(id="obitos-na-data-text"),
                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0)",
                                        "color": "#FFFFFF"})
            ], md=4),
        ]),

            dcc.Graph(id="line-graph", figure=fig2)
        ]),

        dbc.Col([
            dcc.Graph(id="choropleth-map", figure=fig)
        ])
    ])
)

if __name__ == "__main__":
    app.run_server(debug=True)