(function () {
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
