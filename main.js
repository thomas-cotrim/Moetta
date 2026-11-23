// Moettá — interações do site
(() => {
  const nav = document.querySelector(".nav");
  const toggle = document.querySelector(".nav__toggle");
  const drawer = document.querySelector(".drawer");

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

  // entrada suave de cartões e blocos
  const alvos = document.querySelectorAll(".story, .card, .mod, .plan, .spec__row, .principles article");
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
    new Image().src = `assets/img/${tab.dataset.img}.webp`;   // pré-carrega
    tab.addEventListener("click", () => {
      if (tab.getAttribute("aria-selected") === "true") return;
      tabs.forEach(t => t.setAttribute("aria-selected", String(t === tab)));
      img.classList.add("is-swapping");
      setTimeout(() => {
        img.src = `assets/img/${tab.dataset.img}.webp`;
        img.alt = `Tela do Moettá: ${tab.textContent.trim()}`;
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
      boxImg.src = el.dataset.src || inner.src;
      boxImg.alt = inner.alt;
      box.hidden = false;
      document.body.style.overflow = "hidden";
    })
  );
  box.addEventListener("click", close);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !box.hidden) close(); });

  // planos: mensal / anual
  const billBtns = document.querySelectorAll("[data-billing]");
  billBtns.forEach(b =>
    b.addEventListener("click", () => {
      billBtns.forEach(x => x.classList.toggle("is-on", x === b));
      const key = b.dataset.billing === "anual" ? "a" : "m";
      document.querySelectorAll(".js-price").forEach(p => (p.textContent = p.dataset[key]));
    })
  );
})();
