# Site do Moettá

Protótipo do site institucional, em HTML, CSS e JavaScript puros: sem build, sem dependências. O Vercel publica a pasta como está.

Visual claro e editorial: fundo off-white, navegação em pílulas com a marca ao centro, grade de destaques com filetes finos. As imagens são capturas reais da versão atual (Moettá Dev, tema "R claro"), com a última sessão salva no app.

## Estrutura

    index.html          página única: destaques, software, funcionalidades, em detalhe,
                        módulos, métodos, assistente, planos, contato
    styles.css          identidade visual
    main.js             menu, vitrine de telas, ampliação de imagens, mensal/anual
    vercel.json         URLs limpas e cache dos arquivos estáticos
    .vercelignore       deixa _captura e este README fora da publicação
    assets/marca/       símbolo, logo e ícone do app
    assets/img/         telas inteiras (nome.webp) e recortes dos gráficos (c-nome.webp)
    _captura/           scripts que regeram as imagens a partir do app

## Ver localmente

    python -m http.server 8080 --directory Site

e abrir http://localhost:8080.

## Publicar no Vercel

Pelo site: *Add New › Project*, importe o repositório e defina **Root Directory = `Site`**, *Framework Preset = Other*, sem comando de build.

Pela linha de comando (precisa do Node): `npm i -g vercel`, depois `vercel` dentro desta pasta.

## Marca

`assets/marca/` vem do próprio app: as logos de cada edição (`moetta`, `moetta-ia`, `moetta-dev`, de `interface/marca/logo.png` de cada pasta) e o logotipo "Moettá" (`moetta-nome.svg`, desenho monolinear de `interface/logotipo.py`, com os dois "t" unidos e o acento em verde-água). O sufixo da edição ("IA", "DEV") segue o app: fonte de largura fixa, negrito, em maiúsculas espaçadas. Para regerar depois de mudar a marca, em `Site/_captura`:

    python exportar_marca.py

## Refazer as capturas

Quando o app mudar, dentro de `Site/_captura`:

    ..\..\Instalador\_amb\Scripts\python.exe capturar_telas.py
    python exportar_imagens.py telas ..\assets\img

O primeiro abre o app fora da tela, retoma a última sessão sobre uma cópia de `~/.macrolab` (os seus dados não são tocados), roda regressão, Markov, modelo próprio, PCA, previsão etc. e grava as telas. O segundo converte para WebP e gera os recortes. As séries usadas em cada tela estão no próprio script. Depois de trocar imagens, aumente o `?v=` do CSS/JS em `index.html` se o navegador insistir na versão antiga.

## O que ainda é provisório

- **Preços** dos planos (R$ 59 / 119 / 219 por mês; anual com 20% de desconto) são ilustrativos. Ficam nos atributos `data-m` e `data-a` de cada `.js-price` em `index.html`.
- **Formulário de contato** só mostra a mensagem de agradecimento; não envia nada. Para receber os e-mails, ligue-o a um serviço (Formspree, Vercel Functions etc.).
