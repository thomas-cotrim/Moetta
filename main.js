// Moettá — interações do site
(() => {
  const nav = document.querySelector(".nav");
  const toggle = document.querySelector(".nav__toggle");
  const drawer = document.querySelector(".drawer");

  // textos da interface em cada idioma (o conteúdo fica no HTML de cada idioma)
  const lang = (document.documentElement.lang || "pt").slice(0, 2);
  const T = {
    pt: { prev: "Página anterior", next: "Próxima página", pages: "Páginas", tela: "Tela do Moettá" },
    en: { prev: "Previous page", next: "Next page", pages: "Pages", tela: "Moettá screen" },
    es: { prev: "Página anterior", next: "Página siguiente", pages: "Páginas", tela: "Pantalla de Moettá" },
  }[lang] || {};

  // raiz do site (onde está o main.js), para as imagens funcionarem em /en/ e /es/
  const base = new URL(".", document.querySelector('script[src*="main.js"]').src).href;

  // navegação: filete ao rolar e menu móvel
  const onScroll = () => nav.classList.toggle("is-scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const setDrawer = open => {
    drawer.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  };
  toggle.addEventListener("click", () => setDrawer(drawer.hidden));
  drawer.querySelectorAll("a").forEach(a => a.addEventListener("click", () => setDrawer(false)));
  window.addEventListener("resize", () => { if (window.innerWidth > 860) setDrawer(false); });

  // ---------- páginas ----------
  // Cada <div class="page"> é uma página. O endereço (#pesquisa, #software…) escolhe qual aparece;
  // autor, contato e rodapé ficam sempre embaixo.
  const pages = [...document.querySelectorAll(".page")];
  const siteTitle = document.title;

  // rodapé de cada página: anterior / próxima
  pages.forEach((p, i) => {
    const prev = pages[i - 1], next = pages[i + 1];
    const el = document.createElement("nav");
    el.className = "pager wrap";
    el.setAttribute("aria-label", T.pages);
    el.innerHTML =
      (prev ? `<a class="pager__prev" href="#${prev.id}"><small>← ${T.prev}</small>${prev.dataset.title}</a>` : "<span></span>") +
      (next ? `<a class="pager__next" href="#${next.id}"><small>${T.next} →</small>${next.dataset.title}</a>` : "<span></span>");
    p.appendChild(el);
  });

  const pageLinks = document.querySelectorAll(".nav__left a, .drawer a");
  const langLinks = document.querySelectorAll(".lang a");
  let current = null;

  const show = (page, target) => {
    const changed = page !== current;
    if (changed) {
      pages.forEach(p => p.classList.toggle("is-active", p === page));
      current = page;
      document.title = page === pages[0] ? siteTitle : `${page.dataset.title} — Moettá`;
      pageLinks.forEach(a => {
        if (a.getAttribute("href") === `#${page.id}`) a.setAttribute("aria-current", "page");
        else a.removeAttribute("aria-current");
      });
    }
    const behavior = changed ? "instant" : "smooth";
    if (target && target !== page) target.scrollIntoView({ behavior });
    else window.scrollTo({ top: 0, behavior });
  };

  const route = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const el = id && document.getElementById(id);
    // o idioma mantém a mesma página
    langLinks.forEach(a => { a.href = a.href.split("#")[0] + location.hash; });
    if (!el || id === "topo") return show(pages[0]);
    const page = el.closest(".page");
    if (page) return show(page, el);
    el.scrollIntoView({ behavior: "smooth" });   // autor, contato: comuns a todas
  };
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  window.addEventListener("hashchange", route);
  route();

  // clique na página já aberta (ou no mesmo #) volta ao topo dela
  document.addEventListener("click", e => {
    const a = e.target.closest('a[href^="#"]');
    if (a && a.getAttribute("href") === location.hash) { e.preventDefault(); route(); }
  });

  // entrada suave de cartões e blocos
  const alvos = document.querySelectorAll(".story, .card, .mod, .spec__row, .principles article, .research article");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -40px 0px" });
    alvos.forEach(el => { el.classList.add("reveal"); io.observe(el); });
  }

  // vitrine de funcionalidades
  const tabs = document.querySelectorAll(".tabs [role=tab]");
  const img = document.querySelector(".js-stage-img");
  const title = document.querySelector(".js-stage-title");
  const cap = document.querySelector(".js-stage-cap");
  tabs.forEach(tab => {
    new Image().src = `${base}assets/img/${tab.dataset.img}.webp`;   // pré-carrega
    tab.addEventListener("click", () => {
      if (tab.getAttribute("aria-selected") === "true") return;
      tabs.forEach(t => t.setAttribute("aria-selected", String(t === tab)));
      img.classList.add("is-swapping");
      setTimeout(() => {
        img.src = `${base}assets/img/${tab.dataset.img}.webp`;
        img.alt = `${T.tela}: ${tab.textContent.trim()}`;
        title.textContent = tab.textContent.trim();
        cap.textContent = tab.dataset.cap;
        img.classList.remove("is-swapping");
      }, 180);
    });
  });

  // ampliação de imagens
  const box = document.querySelector(".lightbox");
  const boxImg = box.querySelector("img");
  const close = () => { box.hidden = true; document.body.style.overflow = ""; };
  document.querySelectorAll("[data-lightbox]").forEach(el =>
    el.addEventListener("click", () => {
      const inner = el.querySelector("img");
      boxImg.src = el.dataset.src ? new URL(el.dataset.src, location.href).href : inner.src;
      boxImg.alt = inner.alt;
      box.hidden = false;
      document.body.style.overflow = "hidden";
    })
  );
  box.addEventListener("click", close);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !box.hidden) close(); });
})();
