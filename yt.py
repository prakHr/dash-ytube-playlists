from dash import Dash, dcc, html, Input, Output, State, callback
import dash_player
from dash.dependencies import Input, Output

app = Dash()

app.layout = html.Div(
    [
        dcc.Input(
            id='my-input',
            type='text',
            placeholder='Type yt video id & See the latest video...',
            value='',
            style = {"width":"33%","color":"red",'textAlign': 'center',"margin-left":"33%"}
        ),
        html.Div(
            [
                html.Div(
                    style={"width": "33%", "height":"100%", "padding": "10px"},
                    children=[],
                    id = "yt-div",
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
            },
        ),
        dcc.Input(
            id='my-playlist-input',
            type='text',
            placeholder='Type yt video id  & See the latest videos with extended playlist options...',
            value='',
            style = {"width":"33%","color":"gold",'textAlign': 'center',"margin-left":"33%"}
        ),
        html.Div(
            [
                html.Div(
                    style={"width": "33%", "height":"100%", "padding": "10px"},
                    children=[],
                    id = "yt-extended-div",
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
            },
        ),
    ]
)

@app.callback(
    Output('yt-div', 'children'),
    Input('my-input', 'value'),
    prevent_initial_call=True 
)
def update_output(value):
    try:
        children = [
            dash_player.DashPlayer(
                id=f"{value}",
                url=f"https://youtu.be/{value}",
                controls=True,
            ),
        ]
        return children
    except Exception as e:
        children = [f"{e}"]
        return children



@app.callback(
    Output('yt-extended-div', 'children'),
    Input('my-playlist-input', 'value'),
    Input('yt-extended-div', 'children'),
    prevent_initial_call=True 
)
def update_output(value,children):
    if value=="" or value is None:
        small_children = []
        children+=small_children
        return children
    try:
        small_children = [
            dash_player.DashPlayer(
                id=f"{value}",
                url=f"https://youtu.be/{value}",
                controls=True,
            ),
        ]
        children+=small_children
        return children
    except Exception as e:
        small_children = []
        children+=small_children
        return children


if __name__ == "__main__":
    app.run(debug=True)
