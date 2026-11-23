"""
Gera a marca do site a partir do próprio app: o logotipo "Moettá" (desenho
monolinear de interface/logotipo.py) em SVG, e as logos das três edições.

    python exportar_marca.py
"""
import sys
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parents[1] / "assets" / "marca"
DEST.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(RAIZ / "Moetta_Dev"))
from interface import logotipo  # noqa: E402  (só usa a geometria, sem Qt)

# cores do app: tema claro usa texto escuro e destaque #1E9C82; escuro, #2EC4A6
(DEST / "moetta-nome.svg").write_text(logotipo.svg_nome("#161614", "#1E9C82"), encoding="utf-8")
(DEST / "moetta-nome-claro.svg").write_text(logotipo.svg_nome("#FFFFFF", "#2EC4A6"), encoding="utf-8")

edicoes = {"moetta": "Moetta", "moetta-ia": "Moetta_IA", "moetta-dev": "Moetta_Dev"}
for nome, pasta in edicoes.items():
    im = Image.open(RAIZ / pasta / "interface" / "marca" / "logo.png").convert("RGBA")
    for lado in (512, 128):
        im.resize((lado, lado), Image.LANCZOS).save(DEST / f"{nome}-{lado}.png", optimize=True)
    im.resize((512, 512), Image.LANCZOS).save(DEST / f"{nome}.webp", "WEBP", quality=92, method=6)
    print(nome, "ok")

# ícone do site: a logo da edição base
Image.open(RAIZ / "Moetta" / "interface" / "marca" / "logo.png").convert("RGBA").save(
    DEST / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("marca exportada em", DEST)
