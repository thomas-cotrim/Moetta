import sys, pathlib
from PIL import Image

src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
for f in dst.glob("*.webp"):
    f.unlink()

telas = {
    "extracao": "extracao", "acervo_transformacoes": "transformacoes",
    "vis_series": "series", "vis_expectativas": "expectativas", "vis_correlacao": "correlacao",
    "vis_tecnica": "analise-tecnica", "vis_triangulo": "triangulo",
    "est_regressao": "regressao", "est_regressao_leitura": "leitura", "est_pca": "componentes",
    "est_markov": "regimes", "est_proprio": "modelo-proprio", "est_ardl": "ardl",
    "pred_univariada": "previsao", "manual": "manual",
}
for a, b in telas.items():
    im = Image.open(src / f"{a}.png").convert("RGB")
    im.save(dst / f"{b}.webp", "WEBP", quality=88, method=6)
    print(b, im.size)

# recortes da área de resultados (lado direito, sem barra lateral), para os cartões
W, H = Image.open(src / "vis_series.png").size
recortes = {
    "vis_series": ("c-series", (765, 155, 1858, 950)),
    "est_markov": ("c-regimes", (775, 215, 1845, 940)),
    "vis_triangulo": ("c-triangulo", (765, 205, 1856, 950)),
    "pred_univariada": ("c-previsao", (795, 155, 1858, 935)),
    "vis_correlacao": ("c-correlacao", (765, 155, 1858, 915)),
    "est_regressao_leitura": ("c-leitura", (780, 222, 1842, 905)),
    "est_proprio": ("c-proprio", (838, 575, 1845, 938)),
    "vis_tecnica": ("c-tecnica", (775, 155, 1858, 845)),
    "vis_expectativas": ("c-expectativas", (765, 155, 1858, 720)),
}
for a, (b, box) in recortes.items():
    im = Image.open(src / f"{a}.png").convert("RGB").crop(box)
    im.save(dst / f"{b}.webp", "WEBP", quality=90, method=6)
    print(b, im.size)
