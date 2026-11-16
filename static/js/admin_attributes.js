/* Admin, craft type page (US-13): move attribute fields up and down.
   The buttons reorder the rows and renumber their Order boxes (10, 20, 30, …);
   saving the page stores the new order. Without JavaScript, edit the Order numbers. */
(function () {
  "use strict";

  function init() {
    var group = document.getElementById("attributes-group");
    var tbody = group && group.querySelector("tbody");
    if (!tbody) return;

    function isRow(el) {
      return el && el.matches && el.matches("tr.form-row") && !el.classList.contains("empty-form");
    }
    function filled(row) {
      // Existing rows, or new rows with a key typed; untouched blank rows stay blank.
      var id = row.querySelector("input[name$='-id']");
      var key = row.querySelector("input[name$='-key']");
      return (id && id.value) || (key && key.value.trim());
    }
    function renumber() {
      var n = 0;
      tbody.querySelectorAll("tr.form-row").forEach(function (row) {
        if (!isRow(row) || !filled(row)) return;
        var order = row.querySelector("input[name$='-order']");
        n += 10;
        if (order) order.value = n;
      });
    }
    function sibling(row, forward) {
      var el = forward ? row.nextElementSibling : row.previousElementSibling;
      while (el && !isRow(el)) el = forward ? el.nextElementSibling : el.previousElementSibling;
      return el;
    }
    function addButtons(row) {
      var cell = row.querySelector("td.field-order");
      if (!cell || cell.querySelector(".move-field")) return;
      [["up", "↑", "Move this field up"], ["down", "↓", "Move this field down"]].forEach(function (b) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "move-field";
        button.setAttribute("data-dir", b[0]);
        button.setAttribute("aria-label", b[2]);
        button.title = b[2];
        button.textContent = b[1];
        cell.appendChild(button);
      });
    }

    tbody.querySelectorAll("tr.form-row").forEach(function (row) { if (isRow(row)) addButtons(row); });
    tbody.addEventListener("click", function (e) {
      var button = e.target.closest(".move-field");
      if (!button) return;
      e.preventDefault();
      var row = button.closest("tr");
      var up = button.getAttribute("data-dir") === "up";
      var other = sibling(row, !up);
      if (!other) return;
      if (up) tbody.insertBefore(row, other);
      else tbody.insertBefore(other, row);
      renumber();
      button.focus();
    });
    document.addEventListener("formset:added", function (e) {
      if (isRow(e.target)) addButtons(e.target);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
