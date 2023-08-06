import pathlib

host = "localhost"
port = 1234
watcher_interval = 1.0
recursive = True

httpwatcher_script = "httpwatcher.bundle.js"
websocket_uri = f"ws://{host}:{port}/httpwatcher"
httpwatcher_script_url = (
    pathlib.Path(__file__).parent.absolute()
    / "httpwatcher"
    / "build"
    / httpwatcher_script
)

WEBSOCKET_JS_TEMPLATE = f"""
    <!--RELOAD-->
    <script type='application/javascript' src='{httpwatcher_script}'></script>
    <script type='application/javascript'>httpwatcher('{websocket_uri}');</script>
    <!--ENDRELOAD-->
    </body>
"""
