"""
Abre o Moettá Dev com a última sessão salva, aciona os modelos e grava
as telas com resultados em _captura/telas/. Não altera os seus dados: trabalha
sobre uma cópia de ~/.macrolab (em _captura/home_macrolab, refeita a cada vez).

Rodar com o Python do instalador (o mesmo pandas que gravou a sessão):
    ..\\..\\Instalador\\_amb\\Scripts\\python.exe capturar_telas.py
Depois: python exportar_imagens.py telas ..\\assets\\img
"""
import os, sys, shutil, traceback, warnings
from pathlib import Path

APP = Path(__file__).resolve().parents[2] / "Moetta_Dev"
SCR = Path(__file__).resolve().parent
HOME = SCR / "home_macrolab"
OUT = SCR / "telas"
shutil.rmtree(HOME, ignore_errors=True)
shutil.copytree(Path.home() / ".macrolab", HOME)
OUT.mkdir(exist_ok=True)
os.environ["MACROLAB_HOME"] = str(HOME)
os.environ["MOETTA_SEM_SESSAO"] = "1"
sys.path.insert(0, str(APP / "motor"))
sys.path.insert(0, str(APP))
os.chdir(APP)

from PySide6.QtWidgets import QApplication, QTabWidget
qapp = QApplication(sys.argv)
from interface import tema
tema.aplicar(qapp, "r_claro")      # o site é claro: sempre o tema "R claro" do app
import idioma
idioma.definir("pt")
from interface.janela import App
warnings.filterwarnings("ignore")
jan = App(sincrono=True)
jan.retomar_sessao(forcar=True)
# sem sessão com dados, abre a base de demonstração pela mesma rotina do Acervo
BASE_DEMO = APP.parent / "Projetos" / "Análise Austríaca" / "Bases Intermediárias 1 (Op.)" / "base_op2.xlsx"
if not jan.estado.tem_acervo():
    _ac = jan.telas["acervo"]
    _ac._adotar(_ac.carregar_arquivo(str(BASE_DEMO), BASE_DEMO.name, BASE_DEMO.name))
    jan.estado.cortar_periodo("1996-01-01")          # depois do Real, como na análise original
print("acervo:", jan.estado.acervo().shape, flush=True)
from interface import componentes as _C
_C.TITULOS.clear()          # títulos personalizados da sessão não valem para as demonstrações
jan.resize(1520, 912)
jan.move(-4000, 40)
jan.show()


def pump(n=8):
    for _ in range(n):
        qapp.processEvents()


def aba(widget, texto):
    """Escolhe, em qualquer QTabWidget dentro de widget, a aba com esse texto."""
    for tw in [widget] + widget.findChildren(QTabWidget):
        if isinstance(tw, QTabWidget):
            for i in range(tw.count()):
                if tw.tabText(i).strip() == texto:
                    tw.setCurrentIndex(i)
                    pump()
                    return True
    return False


def grava(nome):
    jan.avisar("")
    pump()
    jan.grab().save(str(OUT / f"{nome}.png"))
    print("ok", nome, flush=True)


def passo(nome, f):
    try:
        f()
        grava(nome)
    except Exception:
        print("FALHOU", nome)
        traceback.print_exc()


T = jan.telas
vis, est, pred = T["visualizacao"], T["estimacao"], T["predicao"]


# ---------- Extração e acervo ----------
def extracao():
    jan.mostrar("extracao")
passo("extracao", extracao)


def acervo_cobertura():
    jan.mostrar("acervo")
    aba(T["acervo"], "Cobertura")
passo("acervo_cobertura", acervo_cobertura)


def acervo_transf():
    jan.mostrar("acervo")
    aba(T["acervo"], "Transformações")
passo("acervo_transformacoes", acervo_transf)


# ---------- Visualização ----------
def series():
    jan.mostrar("visualizacao")
    aba(vis, "Séries")
    vis.ck_eixo2.setChecked(True)
    vis.l_series.selecionar(["selic_meta_aa", "ipca_livres_var_mensal_ac12"])
    vis.desenhar()
passo("vis_series", series)


def series_focus():
    jan.mostrar("visualizacao")
    aba(vis, "Séries")
    vis.ck_eixo2.setChecked(False)
    vis.l_series.selecionar(["ipca_t1", "ipca_t2", "ipca_t3", "ipca_t4", "focus_ipca_12m"])
    vis.desenhar()
passo("vis_expectativas", series_focus)


def correl():
    jan.mostrar("visualizacao")
    aba(vis, "Correlação")
    vis.l_corr.selecionar(["ibc_br_dln", "concessoes_total_rs_milhoes_dln", "m2_brasil_rs_mil_dln",
                           "selic_meta_aa_dln", "cambio_venda_fim_dln", "ibovespa_dln"])
    vis.correlacao()
passo("vis_correlacao", correl)


def tecnica():
    jan.mostrar("visualizacao")
    aba(vis, "Análise técnica")
    t = vis.tecnica
    t.cb_serie.setCurrentText("ibovespa")
    t.desenhar()
passo("vis_tecnica", tecnica)


def triangulo():
    jan.mostrar("visualizacao")
    aba(vis, "Triângulo de Hayek")
    t = vis.triangulo
    t.recarregar()
    t.l_est.selecionar(["prod_bens_capital", "prod_bens_intermediarios",
                        "prod_bens_consumo_duraveis", "prod_bens_consumo_nao_duraveis"])
    t.ed_a.setText("31/01/2012")
    t.ed_b.setText("31/12/2019")
    t.desenhar()
passo("vis_triangulo", triangulo)


# ---------- Estimação ----------
def regressao():
    jan.mostrar("estimacao")
    aba(est, "Regressão")
    est.o_y.setCurrentText("ibc_br_dln")
    est._opcoes_x()
    est.o_x.selecionar(["concessoes_total_rs_milhoes_dln", "m2_brasil_rs_mil_dln",
                        "selic_meta_aa_dln", "cambio_venda_fim_dln"])
    est.regressao()
    aba(est.o_abas, "Coeficientes")
passo("est_regressao", regressao)


def regressao_leitura():
    aba(est.o_abas, "Leitura")
passo("est_regressao_leitura", regressao_leitura)


def regressao_ajuste():
    aba(est.o_abas, "Ajuste e resíduos")
passo("est_regressao_ajuste", regressao_ajuste)


def pca():
    jan.mostrar("estimacao")
    aba(est, "Componentes principais")
    est.pc_lista.selecionar(["ipca_var_mensal_pct", "igpm_var_mensal", "inpc_var_mensal", "igpdi_var_mensal",
                             "selic_meta_aa", "prazo_12m", "prazo_60m", "ibc_br_dln",
                             "concessoes_total_rs_milhoes_dln", "cambio_venda_fim_dln",
                             "taxa_desocupacao_pct", "spread_credito_total_pp"])
    est.estimar_pca()
passo("est_pca", pca)


def markov():
    jan.mostrar("estimacao")
    aba(est, "Regimes (Markov)")
    mk = est.markov
    mk.recarregar()
    mk.cb.setCurrentText("credito_saldo_total_dln")
    mk.estimar()
passo("est_markov", markov)


def markov_ipca():
    mk = est.markov
    mk.cb.setCurrentText("ipca_var_mensal_pct")
    mk.estimar()
passo("est_markov_ipca", markov_ipca)


def proprio():
    jan.mostrar("estimacao")
    aba(est, "Modelo próprio")
    p = est.proprio
    p.recarregar()
    p.ed_y.setText("ipca_var_mensal_pct")
    p.ed_t.setPlainText("lag(ipca_var_mensal_pct, 1)\nlag(selic_acum_mes, 1)\n"
                        "lag(cambio_venda_fim_dln, 1)\nlag(focus_ipca_12m, 1)")
    p.estimar()
    aba(p, "Ajuste e previsão")
passo("est_proprio", proprio)


def proprio_coef():
    aba(est.proprio, "Coeficientes")
passo("est_proprio_coef", proprio_coef)


def ardl():
    jan.mostrar("estimacao")
    aba(est, "ARDL")
    a = est.ardl
    a.recarregar()
    a.cb_y.setCurrentText("ipca_var_mensal_pct")
    a._opcoes()
    a.l_x.selecionar(["selic_acum_mes", "cambio_venda_fim_dln"])
    a.estimar()
passo("est_ardl", ardl)


def granger():
    jan.mostrar("estimacao")
    aba(est, "Granger")
    g = est.granger_par
    g.recarregar()
    g.cb_a.setCurrentText("selic_acum_mes")
    g.cb_b.setCurrentText("ipca_var_mensal_pct")
    g.testar()
passo("est_granger", granger)


def diagnostico():
    jan.mostrar("estimacao")
    aba(est, "Diagnóstico")
    aba(est, "Autocorrelação (ACF e PACF)")
    est.ac_serie.setCurrentText("ipca_var_mensal_pct")
    est.autocorrelacao()
passo("est_acf", diagnostico)


# ---------- Predição ----------
def univariada():
    from interface.telas.estimacao import aplicar_ordem
    jan.mostrar("predicao")
    aba(pred, "AR / ARIMA / SARIMA")
    pred.un_serie.setCurrentText("ipca_var_mensal_pct")
    aplicar_ordem(pred.un_w, (1, 0, 1), (1, 0, 1, 12))
    pred.un_h.setValue(12)
    pred.un_teste.setValue(24)
    pred.prever_univariada()
passo("pred_univariada", univariada)


def manual():
    jan.mostrar("manual")
    aba(T["manual"], "Guia dos modelos")
passo("manual", manual)


def ia():
    jan.mostrar("estimacao")
    aba(est, "Regressão")
    jan.alternar_ia("chat")
    pump(20)
passo("ia_painel", ia)
