from dash import Dash, dcc, html, Input, Output, State, ALL, ctx
import dash_player
import json
import os

app = Dash(__name__)

FILE_PATH = "saved_urls.json"

# --- file helpers ---
def load_urls():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return []

def save_urls(urls):
    with open(FILE_PATH, "w") as f:
        json.dump(urls, f, indent=4)

app.layout = html.Div(
    [
        dcc.Input(
            id='my-input',
            type='text',
            placeholder='Type yt video id & See the latest video...',
            value='',
            style={"width":"33%","color":"red",'textAlign': 'center',"margin-left":"33%"}
        ),

        html.Div(id="yt-div"),

        dcc.Input(
            id='my-playlist-input',
            type='text',
            placeholder='Add playlist videos...',
            value='',
            style={"width":"33%","color":"gold",'textAlign': 'center',"margin-left":"33%"}
        ),

        html.Div(id="yt-extended-div"),
    ]
)

# --- SINGLE VIDEO ---
@app.callback(
    Output('yt-div', 'children'),
    Input('my-input', 'value'),
    prevent_initial_call=True
)
def update_single(value):
    if not value:
        return []

    return [
        html.Div([
            dash_player.DashPlayer(
                url=f"https://youtu.be/{value}",
                controls=True,
            )
        ])
    ]


# --- PLAYLIST (WITH SAVE BUTTON PER CHILD) ---
@app.callback(
    Output('yt-extended-div', 'children'),
    Input('my-playlist-input', 'value'),
    State('yt-extended-div', 'children'),
    prevent_initial_call=True
)
def update_playlist(value, children):
    if children is None:
        children = []

    if not value:
        return children

    children.append(
        html.Div([
            dash_player.DashPlayer(
                url=f"https://youtu.be/{value}",
                controls=True,
            ),
            html.Button(
                "💾 Save",
                id={"type": "save-btn", "index": value},
                n_clicks=0
            )
        ])
    )

    return children


# --- SAVE WHEN ANY PLAYLIST BUTTON CLICKED ---
@app.callback(
    Output('my-input', 'placeholder'),  # dummy output (required)
    Input({"type": "save-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def save_from_playlist(n_clicks):
    if not ctx.triggered:
        return "Type yt video id..."

    video_id = ctx.triggered_id["index"]
    url = f"https://youtu.be/{video_id}"

    saved = load_urls()

    if url not in saved:
        saved.append(url)
        save_urls(saved)
        #print(f"Saved: {url}")

    return "Saved!"


if __name__ == "__main__":
    app.run(debug=True)