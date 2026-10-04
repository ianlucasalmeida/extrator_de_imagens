import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAIZ = Path(__file__).resolve().parent.parent
PASTA_ENTRADA = RAIZ / "entrada"
PASTA_SAIDA = RAIZ / "saida"
PASTA_IMAGENS = PASTA_SAIDA / "imagens"
PASTA_DUPLICATAS = PASTA_IMAGENS / "_duplicatas"

ID_MODE = os.getenv("ID_MODE", "local").lower()
PLANTNET_KEY = os.getenv("PLANTNET_KEY", "")
LIMIAR_SCORE = 0.30