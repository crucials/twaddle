import subprocess
import os
import signal
from threading import Thread
import platform

from dotenv import load_dotenv
import waitress
import waitress.server
from flask import Flask
from werkzeug.exceptions import HTTPException

from utils.create_path_from_executable import create_path_from_executable
from ui.api_routes import routes


class UnsupportedOSError(Exception):
    pass


load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.errorhandler(HTTPException)
def send_json_error_response(error: HTTPException):
    return {
        "error": {"code": error.code, "explanation": error.description},
        "data": None,
    }, error.code or 500


for route_blueprint in routes:
    app.register_blueprint(route_blueprint)


def exit_after_electron_stopped(electron_subprocess_to_wait: subprocess.Popen):
    electron_subprocess_to_wait.wait()
    os.kill(os.getpid(), signal.SIGINT)


if os.environ.get("MODE") == "DEVELOPMENT":
    print(
        "launching electron in development mode, dont forget to install npm packages",
        "in './src/ui/electron' folder and build the vue frontend",
        "with 'npm run build'",
        "\n",
    )

    with subprocess.Popen(
        "cd ./src/ui/electron; npm run build; " + "npx electron .", shell=True
    ) as electron_subprocess:
        Thread(target=exit_after_electron_stopped, args=[electron_subprocess]).start()

        print("launching dev flask server", "\n")
        app.run()
else:
    print("launching electron in production mode, with bundled executable", "\n")

    if platform.system() == "Windows":
        ELECTRON_EXECUTABLE_FILENAME = "twaddle.exe"
    elif platform.system() == "Linux":
        ELECTRON_EXECUTABLE_FILENAME = "twaddle.AppImage"
    else:
        raise UnsupportedOSError(
            "only linux and windows operating systems are supported"
        )

    electron_executable_path = create_path_from_executable(
        "ui", "electron", "bin", ELECTRON_EXECUTABLE_FILENAME
    )

    with subprocess.Popen(
        [], executable=electron_executable_path, shell=True
    ) as electron_subprocess:
        Thread(target=exit_after_electron_stopped, args=[electron_subprocess]).start()

        print("launching waitress server for flask api", "\n")
        waitress.serve(app, port=5000)
