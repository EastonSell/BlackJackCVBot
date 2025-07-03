from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generate_card_image(text: str) -> bytes:
    img = Image.new("RGB", (200, 200), "white")
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    except Exception:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    draw.text((40, 40), text, fill="black", font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_recognize_card_endpoint():
    data = generate_card_image("A")
    response = client.post(
        "/recognize_card",
        files={"file": ("card.png", data, "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["card"] == "A"
