from pathlib import Path
from src.config import ID_MODE, PLANTNET_KEY


def identificar(img_bytes: bytes, nome_temp: str | None = None) -> list[dict]:
    if ID_MODE == "plantnet":
        return _plantnet(img_bytes)
    return _bioclip(img_bytes, nome_temp)


def _plantnet(img_bytes: bytes, top_n: int = 3) -> list[dict]:
    import requests

    if not PLANTNET_KEY:
        raise RuntimeError("PLANTNET_KEY não configurada. Veja .env.example")

    url = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_KEY}"
    files = {"images": ("img.jpg", img_bytes, "image/jpeg")}
    r = requests.post(url, files=files, data={"organs": "auto"}, timeout=30)
    if r.status_code != 200:
        return []
    res = r.json().get("results", [])
    return [
        {
            "nome_cientifico": x["species"]["scientificNameWithoutAuthor"],
            "familia": x["species"].get("family", {}).get("scientificNameWithoutAuthor"),
            "score": x["score"],
        }
        for x in res[:top_n]
    ]


_classificador = None


def _bioclip(img_bytes: bytes, nome_temp: str | None, top_n: int = 3) -> list[dict]:
    from pybioclip import TreeOfLifeClassifier, Rank
    from PIL import Image
    from io import BytesIO

    global _classificador
    if _classificador is None:
        _classificador = TreeOfLifeClassifier()

    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    resultados = _classificador.predict(img, Rank.SPECIES)
    return [
        {"nome_cientifico": r["species"], "familia": None, "score": r["score"]}
        for r in resultados[:top_n]
    ]