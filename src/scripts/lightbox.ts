function setupLightbox() {
  const article = document.querySelector("#article");
  if (!article) return;

  const images = article.querySelectorAll("img");
  if (!images.length) return;

  // Create overlay
  const overlay = document.createElement("div");
  overlay.id = "lightbox-overlay";
  overlay.style.cssText =
    "position:fixed;inset:0;z-index:100;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.85);cursor:zoom-out;backdrop-filter:blur(4px)";

  const img = document.createElement("img");
  img.style.cssText =
    "max-width:90vw;max-height:90vh;object-fit:contain;border-radius:4px";
  overlay.appendChild(img);

  document.body.appendChild(overlay);

  function close() {
    overlay.style.display = "none";
    document.documentElement.style.overflow = "";
  }

  overlay.addEventListener("click", close);
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") close();
  });

  images.forEach(image => {
    image.style.cursor = "zoom-in";
    image.addEventListener("click", () => {
      img.src = image.src;
      img.alt = image.alt;
      overlay.style.display = "flex";
      document.documentElement.style.overflow = "hidden";
    });
  });
}

setupLightbox();
document.addEventListener("astro:page-load", setupLightbox);
