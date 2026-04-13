import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Limites
TEMP_MIN = -50
TEMP_MAX = 50

app.layout = html.Div([
    html.H1(
        "Medidor de Temperatura",
        style={
            'textAlign': 'center',
            'fontFamily': 'Arial',
            'marginTop': '50px'
        }
    ),

    html.Div([
        dcc.Graph(
            id='thermometer-graph',
            config={'displayModeBar': False}
        )
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.Div([
        dcc.Input(
            id='input-temp',
            type='number',
            placeholder='Digite a temperatura (°C)',
            style={
                'padding': '10px',
                'width': '220px',
                'marginRight': '10px',
                'borderRadius': '5px',
                'border': '1px solid #ccc'
            }
        ),
        html.Button(
            'Medir',
            id='btn-medir',
            n_clicks=0,
            style={
                'padding': '10px 20px',
                'cursor': 'pointer',
                'backgroundColor': '#4CAF50',
                'color': 'white',
                'border': 'none',
                'borderRadius': '5px'
            }
        )
    ], style={'textAlign': 'center', 'marginTop': '30px'})
],
style={'fontFamily': 'Arial', 'backgroundColor': '#f5f5f5', 'height': '100vh'}
)

@app.callback(
    Output('thermometer-graph', 'figure'),
    Input('btn-medir', 'n_clicks'),
    State('input-temp', 'value')
)
def update_thermometer(n_clicks, value):

    # Valor padrão
    temp = TEMP_MIN if value is None else float(value)

    # Limite
    temp = max(TEMP_MIN, min(TEMP_MAX, temp))

    fig = go.Figure()

    # MERCÚRIO (coluna vermelha)
    fig.add_trace(go.Bar(
        x=[0],
        y=[temp - TEMP_MIN],
        base=[TEMP_MIN],
        marker=dict(color='red'),
        width=0.2,
        hoverinfo='skip'
    ))

    # BULBO EXTERNO (preto)
    fig.add_trace(go.Scatter(
        x=[0],
        y=[TEMP_MIN - 2],
        mode='markers',
        marker=dict(size=50, color='black'),
        hoverinfo='skip'
    ))

    # BULBO INTERNO (vermelho)
    fig.add_trace(go.Scatter(
        x=[0],
        y=[TEMP_MIN - 2],
        mode='markers',
        marker=dict(size=35, color='red'),
        hoverinfo='skip'
    ))

    # MARCAÇÕES (2 em 2 graus) + ANOTAÇÕES SÓ A CADA 10 GRAUS À DIREITA
    tick_shapes = []
    tick_annotations = []

    for y in range(TEMP_MIN, TEMP_MAX + 1, 2):

        # Marca maior a cada 10 graus
        if y % 10 == 0:
            x0 = 0.12
            x1 = 0.35
            width = 2
            font_size = 12
        else:
            x0 = 0.12
            x1 = 0.25
            width = 1
            font_size = 10

        # linhas das marcações (mantém todas as 2 em 2)
        tick_shapes.append(
            dict(
                type="line",
                x0=x0, x1=x1,
                y0=y, y1=y,
                line=dict(color="black", width=width),
                layer='above'
            )
        )

        # Somente anotar os múltiplos de 10 (à direita)
        if y % 10 == 0:
            x_text = 0.42  # ajuste horizontal das anotações (aumente para mover mais à direita)
            tick_annotations.append(
                dict(
                    x=x_text,
                    y=y,
                    xref='x',
                    yref='y',
                    text=f"{y}°C",
                    showarrow=False,
                    xanchor='left',
                    yanchor='middle',
                    font=dict(color='black', size=font_size, family='Arial')
                )
            )

    # Layout
    fig.update_layout(
        shapes=[
            # Tubo
            dict(
                type="rect",
                x0=-0.1, x1=0.1,
                y0=TEMP_MIN, y1=TEMP_MAX,
                line=dict(color="black", width=2),
                fillcolor="white",
                layer='below'
            ),

            # Marcações
            *tick_shapes
        ],

        annotations=tick_annotations,

        template="none",

        xaxis=dict(
            showticklabels=False,
            range=[-1, 1],
            fixedrange=True,
            showgrid=False,
            zeroline=False
        ),

        # Oculta os rótulos padrão do eixo Y (retira números do lado esquerdo)
        yaxis=dict(
            range=[TEMP_MIN - 15, TEMP_MAX + 15],
            showticklabels=False,
            tickmode='linear',
            tick0=TEMP_MIN,
            dtick=10,
            showline=False,
            fixedrange=True,
            showgrid=False,
            zeroline=False  
        ),

        height=650,
        width=400,
        margin=dict(l=100, r=100, t=20, b=20),

        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
