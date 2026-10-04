# associacao.py
def distancia_centros(b1, b2):
    c1 = ((b1[0]+b1[2])/2, (b1[1]+b1[3])/2)
    c2 = ((b2[0]+b2[2])/2, (b2[1]+b2[3])/2)
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2) ** 0.5

def legenda_mais_proxima(img, textos, max_dist=300):
    mesma_pag = [t for t in textos if t["pagina"] == img["pagina"]]
    if not mesma_pag:
        return None
    return min(mesma_pag, key=lambda t: distancia_centros(img["bbox"], t["bbox"]))