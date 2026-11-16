/* Craft page: photo gallery thumbnails, sensitive-photo notices and the location map. */
(function () {
  "use strict";
  var main = document.querySelector("[data-gallery-main]");
  var figure = document.querySelector("[data-gallery-figure]");
  var cover = document.querySelector("[data-sensitive-cover]");
  var caption = document.querySelector("[data-gallery-caption]");
  var revealed = {};  // photos this viewer chose to see (US-21), by address

  /* Sensitive photos stay blurred, with no alt text read out, until "Show photo". */
  function showPhoto(src, alt, sensitive) {
    var hide = sensitive && !revealed[src];
    main.src = src;
    main.setAttribute("data-alt", alt);
    main.alt = hide ? "" : alt;
    if (figure) figure.classList.toggle("is-sensitive", hide);
    if (cover) cover.hidden = !hide;
  }
  if (cover && main) {
    var reveal = cover.querySelector("[data-reveal]");
    if (reveal) reveal.addEventListener("click", function () {
      var src = main.getAttribute("src");
      revealed[src] = true;
      showPhoto(src, main.getAttribute("data-alt") || "", false);
      document.querySelectorAll("[data-gallery-thumb]").forEach(function (b) {
        if (b.getAttribute("data-src") === src) b.classList.remove("thumb-sensitive");
      });
      main.setAttribute("tabindex", "-1");  // keep keyboard focus near the photo
      main.focus();
    });
  }
  document.querySelectorAll("[data-gallery-thumb]").forEach(function (button) {
    button.addEventListener("click", function () {
      showPhoto(button.getAttribute("data-src"), button.getAttribute("data-alt"),
        button.getAttribute("data-sensitive") === "true");
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
      L.circle([lat, lng], { radius: 12000, color: "#1e4a8b", fillColor: "#8cc8ea", fillOpacity: 0.18 }).addTo(map);
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
