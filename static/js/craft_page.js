/* Craft page: photo gallery thumbnails and the location map. */
(function () {
  "use strict";
  var main = document.querySelector("[data-gallery-main]");
  var caption = document.querySelector("[data-gallery-caption]");
  document.querySelectorAll("[data-gallery-thumb]").forEach(function (button) {
    button.addEventListener("click", function () {
      main.src = button.getAttribute("data-src");
      main.alt = button.getAttribute("data-alt");
      if (caption) caption.textContent = button.getAttribute("data-caption");
      document.querySelectorAll("[data-gallery-thumb]").forEach(function (b) {
        b.setAttribute("aria-current", b === button ? "true" : "false");
      });
    });
  });

  function initMap() {
    var el = document.querySelector("[data-craft-map]");
    if (!el) return;
    if (typeof L === "undefined") { el.hidden = true; return; }
    var lat = parseFloat(el.getAttribute("data-lat")), lng = parseFloat(el.getAttribute("data-lng"));
    var approximate = el.getAttribute("data-approximate") === "true";
    var map = L.map(el, { scrollWheelZoom: false, attributionControl: true }).setView([lat, lng], approximate ? 7 : 9);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    if (approximate) {
      L.circle([lat, lng], { radius: 12000, color: "#a54826", fillColor: "#a54826", fillOpacity: 0.18 }).addTo(map);
    } else {
      L.marker([lat, lng]).addTo(map);
    }
  }
  if (typeof L !== "undefined") initMap();
  else {
    window.addEventListener("leaflet:ready", initMap, { once: true });
    window.addEventListener("leaflet:failed", initMap, { once: true });
  }
})();
