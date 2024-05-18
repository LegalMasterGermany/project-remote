import requests
from io import BytesIO
from PIL import ImageGrab
from flask import request, jsonify


def screen_to_api(uuid):
    try:
        screenshot = ImageGrab.grab()
        bytes_io = BytesIO()
        screenshot.save(bytes_io, format="PNG")
        screenshot_bytes = bytes_io.getvalue()
        bytes_io.close()
        api_url = "http://localhost:5000/api/screenshot"
        data = {"uuid": uuid}
        files = {"screenshot": ("screenshot.png", screenshot_bytes)}
        response_api = requests.post(api_url, files=files, data=data)
        print(response_api.text)

        return response_api
    except Exception as e:
        return str(e)


def init_screenshot(uuid):
    screen_to_api(uuid)

