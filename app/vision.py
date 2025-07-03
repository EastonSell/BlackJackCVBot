"""Utility functions for recognizing card values from images."""

from io import BytesIO
from typing import Optional

from PIL import Image
import pytesseract

from .blackjack import normalize_card


def recognize_card(image: Image.Image) -> Optional[str]:
    """Return canonical card value detected in the given image.

    The detection uses Tesseract OCR to read any text in the image and then
    maps it to the internal card representation using :func:`normalize_card`.
    """
    text = pytesseract.image_to_string(image, config="--psm 6").strip()
    if not text:
        return None
    return normalize_card(text)


def recognize_card_bytes(data: bytes) -> Optional[str]:
    """Convenience wrapper that accepts raw image bytes."""
    with Image.open(BytesIO(data)) as img:
        return recognize_card(img)
