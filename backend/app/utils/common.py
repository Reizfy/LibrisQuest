from datetime import datetime
import pytz
import base64


def get_current_datetime():
    to_zone = pytz.timezone("Asia/Jakarta")
    current_time = datetime.now(to_zone).replace(tzinfo=None)

    return current_time


def base_64_decoder(encoded_str: str) -> str:
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode("utf-8")

    return decoded_str
