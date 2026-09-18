import io

from PIL import Image
from rembg import new_session, remove

# 起動時に1回だけセッション作成
_session = None


def get_session():
    global _session
    if _session is None:
        _session = new_session("u2net")
    return _session


def remove_background(image_bytes: bytes) -> bytes:
    """画像の背景を透過してPNGで返す"""
    input_image = Image.open(io.BytesIO(image_bytes))
    output_image = remove(input_image, session=get_session())

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    return buf.getvalue()