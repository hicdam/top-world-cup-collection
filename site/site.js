(function () {
  var contents = document.getElementById("contents");
  var openers = document.querySelectorAll("[data-contents-open]");
  var closers = document.querySelectorAll("[data-contents-close]");

  function openContents(event) {
    if (!contents) return;
    if (event) event.preventDefault();
    contents.hidden = false;
    document.body.classList.add("contents-open");
    var closeBtn = contents.querySelector("[data-contents-close]");
    if (closeBtn) closeBtn.focus();
  }

  function closeContents() {
    if (!contents) return;
    contents.hidden = true;
    document.body.classList.remove("contents-open");
  }

  openers.forEach(function (el) {
    el.addEventListener("click", openContents);
  });
  closers.forEach(function (el) {
    el.addEventListener("click", closeContents);
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeContents();
  });

  var beats = document.querySelectorAll(".beat");
  var time = document.getElementById("time");
  if (beats.length && "IntersectionObserver" in window) {
    var current = null;
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          current = entry.target;
          var paper = current.getAttribute("data-paper");
          var rule = current.getAttribute("data-rule");
          var ink = current.getAttribute("data-ink");
          var year = current.getAttribute("data-year");
          if (paper) document.body.style.setProperty("--paper", paper);
          if (rule) document.body.style.setProperty("--rule", rule);
          if (ink) document.body.style.setProperty("--ink", ink);
          if (time) {
            if (year) {
              time.hidden = false;
              time.textContent = year;
            } else {
              time.hidden = true;
            }
          }
        });
      },
      { rootMargin: "-35% 0px -45% 0px", threshold: 0.01 }
    );
    beats.forEach(function (beat) {
      observer.observe(beat);
    });
  }

  var form = document.getElementById("enquire");
  if (!form) return;

  var error = form.querySelector(".form-error");
  var ok = document.getElementById("enquire-ok");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var name = form.elements.namedItem("name");
    var email = form.elements.namedItem("email");
    var message = form.elements.namedItem("message");
    var missing =
      !String(name && name.value).trim() ||
      !String(email && email.value).trim() ||
      !String(message && message.value).trim();

    if (missing) {
      if (error) {
        error.hidden = false;
        error.textContent = error.getAttribute("data-required") || "";
      }
      return;
    }

    if (error) error.hidden = true;
    form.hidden = true;
    if (ok) ok.hidden = false;
  });
})();
