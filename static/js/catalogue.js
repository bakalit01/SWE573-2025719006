/* Catalogue: search by location (place lookup or "use my location") and the results map. */
(function () {
  "use strict";
  var near = document.querySelector("[data-near]");
  if (!near) return;
  var form = near.closest("form");
  var place = near.querySelector("[data-near-place]");
  var lat = near.querySelector("[data-near-lat]");
  var lng = near.querySelector("[data-near-lng]");
  var status = near.querySelector("[data-near-status]");
  function say(text) { if (status) status.textContent = text; }

  /* Typing a place: look it up (OpenStreetMap Nominatim) before submitting. If the lookup
     fails, the form is sent without coordinates and the server matches place names. */
  var submitting = false;
  form.addEventListener("submit", function (e) {
    if (submitting) return;
    var text = place.value.trim();
    if (!text) {
      if (!near.hasAttribute("data-my-location")) { lat.value = ""; lng.value = ""; }
      return;
    }
    if (lat.value && place.getAttribute("data-geocoded-for") === text) return;
    e.preventDefault();
    say("Looking up " + text + "…");
    fetch("https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&q=" + encodeURIComponent(text),
      { headers: { "Accept-Language": document.documentElement.lang || "en" } })
      .then(function (r) { return r.json(); })
      .then(function (results) {
        if (results.length) { lat.value = results[0].lat; lng.value = results[0].lon; }
        else { lat.value = ""; lng.value = ""; }
      })
      .catch(function () { lat.value = ""; lng.value = ""; })
      .finally(function () { submitting = true; form.submit(); });
  });
  place.addEventListener("input", function () {
    if (place.value.trim() !== place.getAttribute("data-geocoded-for")) { lat.value = ""; lng.value = ""; }
  });

  var clear = near.querySelector("[data-near-clear]");
  if (clear) clear.addEventListener("click", function () {
    place.value = ""; lat.value = ""; lng.value = ""; near.removeAttribute("data-my-location");
    submitting = true; form.submit();
  });

  var me = near.querySelector("[data-near-me]");
  if (me) {
    if (!("geolocation" in navigator)) me.hidden = true;
    me.addEventListener("click", function () {
      say("Finding your location…");
      navigator.geolocation.getCurrentPosition(function (pos) {
        lat.value = pos.coords.latitude.toFixed(4); lng.value = pos.coords.longitude.toFixed(4);
        place.value = ""; submitting = true; form.submit();
      }, function () { say("Your browser didn't share your location. Type a place instead."); },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 600000 });
    });
  }

  /* Results map */
  var mapEl = document.querySelector("[data-results-map]");
  var dataEl = document.getElementById("map-points");
  function drawMap() {
    if (!mapEl || typeof L === "undefined") {
      if (mapEl) mapEl.innerHTML = '<p class="map-fallback">The map could not load.</p>';
      return;
    }
    var centre = [parseFloat(mapEl.dataset.lat), parseFloat(mapEl.dataset.lng)];
    var map = L.map(mapEl, { scrollWheelZoom: false });
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    var circle = L.circle(centre, { radius: parseInt(mapEl.dataset.km, 10) * 1000, color: "#1e4a8b", weight: 1, fillColor: "#8cc8ea", fillOpacity: 0.12 }).addTo(map);
    map.fitBounds(circle.getBounds());
    var points = dataEl ? JSON.parse(dataEl.textContent) : [];
    points.forEach(function (p) {
      var link = document.createElement("a");
      link.href = p.url; link.textContent = p.title;
      var marker = p.approximate
        ? L.circle([p.lat, p.lng], { radius: 8000, color: "#1e4a8b", fillColor: "#8cc8ea", fillOpacity: 0.5 })
        : L.marker([p.lat, p.lng]);
      marker.addTo(map).bindPopup(link);
    });
  }
  if (mapEl) {
    if (typeof L !== "undefined") drawMap();
    else {
      window.addEventListener("leaflet:ready", drawMap, { once: true });
      window.addEventListener("leaflet:failed", drawMap, { once: true });
    }
  }
})();
