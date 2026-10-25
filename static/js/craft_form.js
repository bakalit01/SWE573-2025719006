/* Add / edit craft form: map pin + place search, repeatable rows, craft-type fields, draft. */
(function () {
  "use strict";
  var form = document.querySelector("[data-craft-form]");
  if (!form) return;

  /* ---------- Repeatable rows (materials, techniques, photos) ---------- */
  function totalInput(prefix) {
    return form.querySelector("#id_" + prefix + "-TOTAL_FORMS");
  }
  function addRow(prefix) {
    var tpl = form.querySelector('[data-row-template="' + prefix + '"]');
    var box = form.querySelector('[data-rows="' + prefix + '"]');
    var total = totalInput(prefix);
    if (!tpl || !box || !total) return null;
    var index = parseInt(total.value, 10);
    var html = tpl.innerHTML.replace(/__prefix__/g, String(index));
    var wrap = document.createElement("div");
    wrap.innerHTML = html.trim();
    var row = wrap.firstElementChild;
    box.appendChild(row);
    total.value = index + 1;
    var first = row.querySelector("input, select, textarea");
    if (first) first.focus();
    return row;
  }
  form.addEventListener("click", function (e) {
    var add = e.target.closest("[data-add-row]");
    if (add) { e.preventDefault(); addRow(add.getAttribute("data-add-row")); return; }
    var remove = e.target.closest("[data-remove-row]");
    if (remove) {
      e.preventDefault();
      var row = remove.closest("[data-row]");
      // Clearing (not deleting) keeps formset indexes valid; empty rows are ignored on save.
      row.querySelectorAll("input, textarea, select").forEach(function (el) {
        if (el.type === "file") el.value = ""; else if (el.type !== "checkbox") el.value = "";
      });
      row.hidden = true;
      saveDraft();
    }
  });

  /* Photo previews */
  form.addEventListener("change", function (e) {
    if (e.target.type !== "file" || !e.target.files || !e.target.files[0]) return;
    var row = e.target.closest("[data-row]");
    var img = row && row.querySelector("[data-preview]");
    if (!img) return;
    img.src = URL.createObjectURL(e.target.files[0]);
    img.hidden = false;
  });

  /* ---------- Craft-type-specific fields ---------- */
  var typeSelect = form.querySelector("[data-craft-type]");
  var attrBox = form.querySelector("[data-attribute-fields]");
  if (typeSelect && attrBox) {
    typeSelect.addEventListener("change", function () {
      var url = form.getAttribute("data-fields-url") + "?craft_type=" + encodeURIComponent(typeSelect.value) +
        "&craft=" + encodeURIComponent(form.getAttribute("data-craft-slug") || "");
      attrBox.setAttribute("aria-busy", "true");
      fetch(url, { credentials: "same-origin" })
        .then(function (r) { return r.text(); })
        .then(function (html) { attrBox.innerHTML = html; restoreDraft(attrBox); })
        .finally(function () { attrBox.removeAttribute("aria-busy"); });
    });
  }

  // A type chosen before this script ran (slow network): load its fields now.
  if (typeSelect && attrBox && typeSelect.value && !attrBox.querySelector('[name^="attr-"]')) {
    typeSelect.dispatchEvent(new Event("change"));
  }

  /* ---------- Map: search, click to pin, reverse lookup ---------- */
  var latInput = form.querySelector("[data-map-lat]");
  var lngInput = form.querySelector("[data-map-lng]");
  var placeInput = form.querySelector("[data-map-place]");
  var countryInput = form.querySelector("[data-map-country]");
  var status = form.querySelector("[data-map-status]");
  var mapEl = form.querySelector("[data-map-picker]");
  var map = null, marker = null;
  var NOMINATIM = "https://nominatim.openstreetmap.org";

  function say(text) { if (status) status.textContent = text; }
  function setPin(lat, lng, zoom) {
    lat = Math.round(lat * 1e6) / 1e6; lng = Math.round(lng * 1e6) / 1e6;
    latInput.value = lat; lngInput.value = lng;
    if (!map) return;
    if (marker) marker.setLatLng([lat, lng]); else marker = L.marker([lat, lng], { draggable: true }).addTo(map);
    marker.off("dragend").on("dragend", function () {
      var p = marker.getLatLng(); setPin(p.lat, p.lng); lookUp(p.lat, p.lng);
    });
    if (zoom) map.setView([lat, lng], zoom);
    saveDraft();
  }
  function placeFrom(address) {
    address = address || {};
    return address.city || address.town || address.village || address.municipality ||
      address.county || address.state || address.region || "";
  }
  function lookUp(lat, lng) {
    say("Looking up the place…");
    fetch(NOMINATIM + "/reverse?format=jsonv2&zoom=10&addressdetails=1&lat=" + lat + "&lon=" + lng,
      { headers: { "Accept-Language": document.documentElement.lang || "en" } })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var place = placeFrom(d.address);
        if (place) placeInput.value = place;
        if (d.address && d.address.country) countryInput.value = d.address.country;
        say(place ? "Pinned near " + place + ". You can edit the place name." : "Pin placed.");
        saveDraft();
      })
      .catch(function () { say("Pin placed. Type the place name yourself (lookup unavailable)."); });
  }
  function search() {
    var q = form.querySelector("[data-map-search]").value.trim();
    if (!q) { say("Type a place to search for."); return; }
    say("Searching…");
    fetch(NOMINATIM + "/search?format=jsonv2&limit=1&addressdetails=1&q=" + encodeURIComponent(q),
      { headers: { "Accept-Language": document.documentElement.lang || "en" } })
      .then(function (r) { return r.json(); })
      .then(function (results) {
        if (!results.length) { say("No match. Try a nearby town, or click the map."); return; }
        var r = results[0];
        setPin(parseFloat(r.lat), parseFloat(r.lon), 9);
        placeInput.value = placeFrom(r.address) || r.name || q;
        if (r.address && r.address.country) countryInput.value = r.address.country;
        say("Found " + r.display_name + ".");
        saveDraft();
      })
      .catch(function () { say("Search is unavailable right now. Click the map or enter coordinates."); });
  }
  var searchButton = form.querySelector("[data-map-search-button]");
  if (searchButton) searchButton.addEventListener("click", search);
  var searchInput = form.querySelector("[data-map-search]");
  if (searchInput) searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") { e.preventDefault(); search(); }
  });
  var clear = form.querySelector("[data-map-clear]");
  if (clear) clear.addEventListener("click", function () {
    latInput.value = ""; lngInput.value = "";
    if (marker && map) { map.removeLayer(marker); marker = null; }
    say("Pin removed."); saveDraft();
  });

  function initMap() {
    if (map) return;
    if (!mapEl || typeof L === "undefined") {
      if (mapEl) mapEl.innerHTML = '<p class="map-fallback">The map could not load. Enter the coordinates under “Coordinates”.</p>';
      return;
    }
    var hasPin = latInput.value && lngInput.value;
    map = L.map(mapEl, { scrollWheelZoom: false }).setView(
      hasPin ? [parseFloat(latInput.value), parseFloat(lngInput.value)] : [20, 10], hasPin ? 8 : 2);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    if (hasPin) setPin(parseFloat(latInput.value), parseFloat(lngInput.value));
    map.on("click", function (e) { setPin(e.latlng.lat, e.latlng.lng); lookUp(e.latlng.lat, e.latlng.lng); });
    [latInput, lngInput].forEach(function (el) {
      el.addEventListener("change", function () {
        var lat = parseFloat(latInput.value), lng = parseFloat(lngInput.value);
        if (!isNaN(lat) && !isNaN(lng)) setPin(lat, lng, 8);
      });
    });
  }

  /* ---------- Unsaved draft in this browser (add form only) ---------- */
  var draftKey = form.getAttribute("data-draft-key");
  var notice = document.querySelector("[data-draft-notice]");
  var restoring = false;
  function fields() {
    return Array.prototype.filter.call(form.elements, function (el) {
      return el.name && el.type !== "file" && el.type !== "hidden" && el.type !== "submit" && el.type !== "button";
    });
  }
  function saveDraft() {
    if (!draftKey || restoring) return;
    var data = { totals: {} , values: {} };
    ["mat", "tec"].forEach(function (p) { var t = totalInput(p); if (t) data.totals[p] = t.value; });
    fields().forEach(function (el) {
      if (el.type === "checkbox" || el.type === "radio") {
        if (el.checked) (data.values[el.name] = data.values[el.name] || []).push(el.value);
      } else if (el.value) { data.values[el.name] = el.value; }
    });
    try { localStorage.setItem(draftKey, JSON.stringify(data)); } catch (e) { /* storage unavailable */ }
  }
  function readDraft() {
    try { return JSON.parse(localStorage.getItem(draftKey) || "null"); } catch (e) { return null; }
  }
  function restoreDraft(scope) {
    var data = draftKey && readDraft();
    if (!data) return false;
    restoring = true;
    var any = false;
    (scope || form).querySelectorAll("input, select, textarea").forEach(function (el) {
      if (!el.name || el.type === "file" || el.type === "hidden") return;
      var v = data.values[el.name];
      if (v === undefined) return;
      if (el.type === "checkbox" || el.type === "radio") el.checked = v.indexOf(el.value) !== -1;
      else if (!el.value || el.tagName === "SELECT") el.value = v;
      any = true;
    });
    restoring = false;
    return any;
  }
  if (draftKey) {
    var formIsEmpty = !form.querySelector("#id_title").value && !form.querySelector(".error");
    var saved = readDraft();
    if (formIsEmpty && saved) {
      ["mat", "tec"].forEach(function (p) {
        var want = parseInt(saved.totals[p] || "0", 10), have = parseInt(totalInput(p).value, 10);
        for (var i = have; i < want; i++) addRow(p);
      });
      if (restoreDraft()) {
        if (notice) notice.hidden = false;
        if (typeSelect && typeSelect.value) typeSelect.dispatchEvent(new Event("change"));
      }
    }
    form.addEventListener("input", saveDraft);
    form.addEventListener("change", saveDraft);
    form.addEventListener("submit", function () { try { localStorage.removeItem(draftKey); } catch (e) {} });
    var clearDraft = document.querySelector("[data-draft-clear]");
    if (clearDraft) clearDraft.addEventListener("click", function () {
      try { localStorage.removeItem(draftKey); } catch (e) {}
      window.location.reload();
    });
  }

  form.setAttribute("data-ready", "true");

  /* Leaflet loads asynchronously; the form works without it (coordinates can be typed). */
  if (typeof L !== "undefined") initMap();
  else {
    window.addEventListener("leaflet:ready", initMap, { once: true });
    window.addEventListener("leaflet:failed", initMap, { once: true });
  }
})();
