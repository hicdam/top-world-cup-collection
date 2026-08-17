(function () {
  var viewer = document.getElementById("viewer");
  if (!viewer) return;

  var img = document.getElementById("viewer-image");
  var meta = document.getElementById("viewer-meta");
  var items = Array.prototype.slice.call(
    document.querySelectorAll("[data-object]")
  );
  var index = 0;

  function show(i) {
    if (!items.length) return;
    index = (i + items.length) % items.length;
    var el = items[index];
    img.src = el.getAttribute("data-full") || el.getAttribute("href");
    img.alt = el.getAttribute("data-alt") || "";
    meta.textContent = el.getAttribute("data-meta") || "";
    viewer.hidden = false;
    document.body.style.overflow = "hidden";
    viewer.querySelector("[data-close]").focus();
  }

  function hide() {
    viewer.hidden = true;
    document.body.style.overflow = "";
    img.removeAttribute("src");
  }

  items.forEach(function (el, i) {
    el.addEventListener("click", function (event) {
      event.preventDefault();
      show(i);
    });
  });

  viewer.querySelector("[data-close]").addEventListener("click", hide);
  viewer.querySelector("[data-prev]").addEventListener("click", function () {
    show(index - 1);
  });
  viewer.querySelector("[data-next]").addEventListener("click", function () {
    show(index + 1);
  });

  document.addEventListener("keydown", function (event) {
    if (viewer.hidden) return;
    if (event.key === "Escape") hide();
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });

  var startX = null;
  viewer.addEventListener("touchstart", function (event) {
    startX = event.changedTouches[0].screenX;
  }, { passive: true });
  viewer.addEventListener("touchend", function (event) {
    if (startX == null) return;
    var dx = event.changedTouches[0].screenX - startX;
    if (dx > 40) show(index - 1);
    if (dx < -40) show(index + 1);
    startX = null;
  });

  var filter = document.getElementById("archive-filter");
  if (filter) {
    filter.addEventListener("click", function (event) {
      var btn = event.target.closest("button[data-folder]");
      if (!btn) return;
      Array.prototype.forEach.call(filter.querySelectorAll("button"), function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      var folder = btn.getAttribute("data-folder");
      Array.prototype.forEach.call(
        document.querySelectorAll("[data-archive-item]"),
        function (card) {
          card.hidden = folder !== "all" && card.getAttribute("data-folder") !== folder;
        }
      );
    });
  }
})();
