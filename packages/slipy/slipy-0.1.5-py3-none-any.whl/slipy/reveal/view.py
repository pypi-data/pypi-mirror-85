import pathlib
import shutil
import logging
import errno
import socket
import asyncio
import signal
import webbrowser
import json

import websockets
import watchdog.events, watchdog.observers

from . import reload
from .. import build

# from . import build


def view(folder):
    project_dir = pathlib.Path(folder).absolute()
    webbrowser.open(str(project_dir / "build" / "index.html"))


def preview(folder, rebuild=True):
    project_dir = pathlib.Path(folder).absolute()

    # init the logger
    # ---------------

    logger = logging.getLogger(__file__)

    loop = asyncio.get_event_loop()

    # add automatic build (if set)
    # ----------------------------
    # and keep watching

    build.build(project_dir)

    if rebuild:

        class BuildHandler(watchdog.events.FileSystemEventHandler):
            def on_any_event(self, event):
                print("\tBUILD WATCHER")
                print("\t", event.event_type, event.src_path)
                src_path = pathlib.Path(event.src_path)
                if src_path.parent.name == "assets":
                    print("\tASSETS")
                    shutil.copy2(str(src_path), str(project_dir / "build" / "assets"))
                else:
                    build.build(project_dir)

        build_handler = BuildHandler()
        build_observer = watchdog.observers.Observer()
        build_observer.schedule(build_handler, path=project_dir / "src", recursive=True)
        build_observer.start()

    # start the server
    # ----------------
    # and keep watching

    class ViewHandler(watchdog.events.FileSystemEventHandler):
        # async def on_any_event(self, event):
        def on_any_event(self, event):
            print("\tVIEW WATCHER")
            print("\t", event.event_type, event.src_path)

            async def send_reload_signal():
                async with websockets.connect(reload.websocket_uri) as websocket:
                    await asyncio.sleep(1)
                    await websocket.send(json.dumps({"command": "reload"}))

            asyncio.run(send_reload_signal())

    view_handler = ViewHandler()
    view_observer = watchdog.observers.Observer()
    view_observer.schedule(view_handler, path=project_dir / "build", recursive=True)
    view_observer.start()

    # set server
    start_server = websocket_server(reload.host, reload.port)

    # TODO: watcher_interval=1.0,  # maximum reload frequency (seconds)

    # Connect everything to the loop
    # ------------------------------

    webbrowser.open(str(project_dir / "build" / "index.html"))

    def close(loop):
        print(f"Finalazing...")
        build_observer.stop()
        if rebuild:
            view_observer.stop()
        loop.stop()

    loop.add_signal_handler(signal.SIGINT, close, loop)

    asyncio.get_event_loop().run_until_complete(start_server)
    loop.run_forever()
    loop.close()
    print("Stop watching for updates.")


def websocket_server(host, port):
    """
    Make a generic server that broadcast the messages from the clients to all the
    other clients.
    """
    USERS = set()

    def users_event():
        return json.dumps({"type": "users", "count": len(USERS)})

    async def notify_message(message):
        if USERS:  # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in USERS])

    async def notify_users():
        if USERS:  # asyncio.wait doesn't accept an empty list
            message = users_event()
            await asyncio.wait([user.send(message) for user in USERS])

    async def register(websocket):
        USERS.add(websocket)
        await websocket.send("[START] Connected to the server")
        await notify_users()

    async def unregister(websocket):
        USERS.remove(websocket)
        await websocket.send("[EXIT] Disconnected from the server")
        await notify_users()

    async def connect(websocket, path):
        """
        This function is run any time a new client will try to connect to the
        websocket.
        """
        # register(websocket) sends user_event() to websocket
        await register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["command"] == "reload":
                    await notify_message(json.dumps(data))
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await unregister(websocket)

    return websockets.serve(connect, host, port)


def test_free_connection(host, port):
    """
    Test if already connected
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print("Server running")
            return False
        else:
            # something else raised the OSError exception
            print(e)
            s.close()

    return True
