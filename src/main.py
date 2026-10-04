# main.py
from pathlib import Path
from collections import defaultdict
import csv, json
from ingest import extrair_pdf, extrair_pptx
from associacao import legenda_mais_proxima
from identificacao import identificar_plantnet
from util import hash_perceptual, normalizar_nome

ENTRADA = Path("entrada")
SAIDA = Path("saida")
(SAIDA / "imagens").mkdir(parents=True, exist_ok=True)
(SAIDA / "imagens" / "_duplicatas").mkdir(exist_ok=True)

LIMIAR_SCORE = 0.30   # abaixo disso → indeterminada
contador = defaultdict(int)
hashes_vistos = {}
inventario = []

arquivos = list(ENTRADA.glob("*.pdf")) + list(ENTRADA.glob("*.pptx"))

for arq in arquivos:
    itens = extrair_pdf(arq) if arq.suffix.lower() == ".pdf" else extrair_pptx(arq)
    imagens = [i for i in itens if i["tipo"] == "imagem"]
    textos  = [i for i in itens if i["tipo"] == "texto"]

    for img in imagens:
        h = hash_perceptual(img["bytes"])
        if h in hashes_vistos:
            destino = SAIDA / "imagens" / "_duplicatas" / f"{h}.jpg"
            destino.write_bytes(img["bytes"])
            inventario.append({"arquivo": str(destino), "origem": arq.name,
                               "pagina": img["pagina"], "status": "duplicata",
                               "hash": h})
            continue
        hashes_vistos[h] = True

        legenda = legenda_mais_proxima(img, textos)
        palpite = identificar_plantnet(img["bytes"]) or []
        melhor = palpite[0] if palpite and palpite[0]["score"] >= LIMIAR_SCORE else None

        if melhor:
            base = normalizar_nome(melhor["nome_cientifico"])
        else:
            base = "indeterminada"

        contador[base] += 1
        nome_arquivo = f"{base}_{contador[base]:03d}.jpg"
        destino = SAIDA / "imagens" / nome_arquivo
        destino.write_bytes(img["bytes"])

        inventario.append({
            "arquivo": nome_arquivo,
            "origem": arq.name,
            "pagina": img["pagina"],
            "legenda_original": legenda["texto"] if legenda else "",
            "especie": melhor["nome_cientifico"] if melhor else "",
            "familia": melhor["familia"] if melhor else "",
            "score": round(melhor["score"], 3) if melhor else "",
            "alternativas": "; ".join(p["nome_cientifico"] for p in palpite[1:]),
            "hash": h,
            "status": "ok" if melhor else "indeterminada",
        })

# inventário
with open(SAIDA / "inventario.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=inventario[0].keys())
    w.writeheader(); w.writerows(inventario)

(SAIDA / "inventario.json").write_text(
    json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8"
)

# padronização
with open(SAIDA / "padronizacao.txt", "w", encoding="utf-8") as f:
    f.write("PADRÃO DE NOMENCLATURA\n")
    f.write("=" * 40 + "\n")
    f.write("Espécie identificada: Genero_especie_NNN.jpg\n")
    f.write("Não identificada:    indeterminada_NNN.jpg\n")
    f.write("Duplicatas:          _duplicatas/<phash>.jpg\n\n")
    f.write("ESPÉCIES ENCONTRADAS\n" + "-" * 40 + "\n")
    for nome, qtd in sorted(contador.items()):
        f.write(f"{nome}: {qtd}\n")