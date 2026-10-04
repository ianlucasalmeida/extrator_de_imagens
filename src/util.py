# util.py
import re, imagehash
from PIL import Image
from io import BytesIO

def hash_perceptual(img_bytes):
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    return str(imagehash.phash(img))

def normalizar_nome(cientifico: str) -> str:
    # "Tibouchina granulosa" → "Tibouchina_granulosa"
    return re.sub(r"[^A-Za-z0-9]+", "_", cientifico).strip("_")