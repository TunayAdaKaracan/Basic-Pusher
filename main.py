from lib import server
from quart import Quart
import threading

app = Quart(__name__)

server = server.Server()
server.create_channel("test")


@app.route("/")
async def index():
    await server.trigger("test", "test-event", {
        "message": "Hi",
        "yeet": "lol"
    })
    return "Sent"


if __name__ == "__main__":
    threading.Thread(target=server.run).start()
    app.run()
