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

  /* Photo credits for Wikimedia Commons files: author and license from the Commons API. */
  var creditEls = Array.prototype.slice.call(document.querySelectorAll("[data-commons-credit]"));
  if (creditEls.length) {
    var titles = creditEls.map(function (el) { return "File:" + el.getAttribute("data-commons-credit"); });
    var url = "https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*" +
      "&prop=imageinfo&iiprop=extmetadata&iiextmetadatafilter=Artist|LicenseShortName|Credit" +
      "&titles=" + encodeURIComponent(titles.join("|"));
    var plain = function (html) {
      return (new DOMParser().parseFromString(html || "", "text/html").body.textContent || "")
        .replace(/\s+/g, " ").trim();
    };
    fetch(url)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var q = data.query || {}, alias = {};
        (q.normalized || []).forEach(function (n) { alias[n.from] = n.to; });
        var byTitle = {};
        Object.keys(q.pages || {}).forEach(function (k) { byTitle[q.pages[k].title] = q.pages[k]; });
        creditEls.forEach(function (el) {
          var title = "File:" + el.getAttribute("data-commons-credit");
          var page = byTitle[alias[title] || title] || byTitle[title.replace(/_/g, " ")];
          var meta = page && page.imageinfo && page.imageinfo[0] && page.imageinfo[0].extmetadata;
          if (!meta) return;
          var artist = plain(meta.Artist && meta.Artist.value);
          var license = plain(meta.LicenseShortName && meta.LicenseShortName.value);
          el.textContent = [artist, license, "via Wikimedia Commons"].filter(Boolean).join(" · ");
        });
      })
      .catch(function () { /* keep the plain "Wikimedia Commons" credit and file-page link */ });
  }

  function initMap() {
    var el = document.querySelector("[data-craft-map]");
    if (!el) return;
    if (typeof L === "undefined") { el.hidden = true; return; }
    var lat = parseFloat(el.getAttribute("data-lat")), lng = parseFloat(el.getAttribute("data-lng"));
    var approximate = el.getAttribute("data-approximate") === "true";
    var map = L.map(el, { scrollWheelZoom: false, attributionControl: true }).setView([lat, lng], approximate ? 7 : 9);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
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
