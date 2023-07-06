// Handle checkboxes in tables, and modal forms
'use strict';
var tablesPro = (function () {
    let tb = {};
    let lastChecked = null
    let selAll = null
    let selAllPage = null
    tb.init = function () {
      let url = new URL(window.location.href)
      const w = url.searchParams.get("_width")
      if (w !== null) {
        if (parseInt(w) !== window.outerWidth) {
          window.location.href = window.location.href.replace(`_width=${w}`, `_width=${window.outerWidth}`)
        }
      }


      //window.addEventListener("load", onLoad)
      selAll = document.getElementById('select_all')
      selAllPage = document.getElementById('select_all_page')
      if (selAllPage) {
        selAllPage.addEventListener("click", selectAllPage)
        selectAllPage()
      }
      if (selAll) {
        selAll.addEventListener("click", selectAll)
        selectAll()
      }

      // document.getElementById('select_all_page').addEventListener("click", selectAllPage )
      Array.from(document.getElementsByTagName("table")).forEach(e => e.addEventListener("click", tableClick));
      Array.from(document.querySelectorAll(".auto-submit")).forEach(e => e.addEventListener("change", function () {
        document.getElementById("id_filter_form").submit()
      }));

      Array.from(document.querySelectorAll(".form-group.hx-get")).forEach(e => e.addEventListener("change", filterChanged))

      countChecked()
      document.body.addEventListener("trigger", function (evt) {
        htmx.ajax('GET', evt.detail.url, {source: '#table_data', 'target': '#table_data'});
      })
      // if (window.matchMedia("(max-width: 768px)").matches) {
      //     setMobileTable("table")
      // }
    }

    function removeURLParameter(url, parameter) {
      //prefer to use l.search if you have a location/link object
      var urlparts = url.split('?');
      if (urlparts.length >= 2) {

        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);

        //reverse iteration as may be destructive
        for (var i = pars.length; i-- > 0;) {
          //idiom for string.startsWith
          if (pars[i].lastIndexOf(prefix, 0) !== -1) {
            pars.splice(i, 1);
          }
        }

        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
      }
      return url;
    }

    // tb.onload = function() {
    // function onLoad() {
    //   init()
    //   console.log("onLoad")
    //   countChecked()
    //   if (selAll) {
    //     if (selAll.checked) {
    //       Array.from(document.getElementsByClassName("select-checkbox")).forEach(function (box) {
    //         box.checked = true;
    //         box.disabled = false;
    //         highlightRow(box);
    //       })
    //       selAll.parentElement.style.display = 'block';
    //       document.getElementById('count').innerText = 'All';
    //       document.getElementById('select_all_page').disabled = true;
    //       Array.from(document.getElementsByClassName("select-checkbox")).forEach(function (box) {
    //         box.disabled = true;
    //       })
    //     }
    //   }
    // }


    function filterChanged() {
      htmx.ajax('GET', '', {source: '#' + this.lastChild.id, target: '#table_data'});
    }

    function checkBoxes() {
      return Array.from(document.getElementsByClassName("select-checkbox"))
    }

    function selectAllPage() {
      // Click on 'Select all on page' highlights all rows
      let checked = selAllPage.checked
      if (checked) {
        selAll.parentElement.style.display = 'block';
      } else {
        selAll.parentElement.style.display = 'none';
      }
      Array.from(document.getElementsByClassName("select-checkbox")).forEach(function (box) {
        box.checked = checked;
        //box.disabled = false;
        highlightRow(box);
      })
      countChecked();
      lastChecked = null;
    }

    function selectAll() {
      // Click on Select all highlights all rows and disables checkboxes
      let checked = selAll.checked
      if (checked) {
        document.getElementById('count').innerText = 'All';
        if (selAllPage) {
          selAllPage.disabled = true
        }
        ;
      } else {
        if (selAllPage) {
          selAllPage.disabled = false
        }
        ;
        //sslAllPage.checked = false;
      }
      Array.from(document.getElementsByClassName("select-checkbox")).forEach(function (box) {
        box.disabled = checked;
      })
      countChecked();
      lastChecked = null;
    }

    function tableClick(e) {
      if (e.target.name === 'select-checkbox') {
        // Click on row's select checkbox - handle using shift to select multiple rows
        if (selAllPage) {
          selAllPage.checked = false
        }
        ;
        // selAll.parentElement.style.display = 'none';
        let chkBox = e.target;
        highlightRow(chkBox);
        if (!lastChecked) {
          lastChecked = chkBox;
        } else if (e.shiftKey) {
          let chkBoxes = checkBoxes();
          let start = chkBoxes.indexOf(chkBox);
          let end = chkBoxes.indexOf(lastChecked);
          chkBoxes.slice(Math.min(start, end), Math.max(start, end) + 1).forEach(function (box) {
            box.checked = chkBox.checked;
            // highlightRow(box)
          });
          lastChecked = chkBox;
        } else {
          lastChecked = chkBox;
        }
        countChecked();

      } else if (e.target.tagName === 'TD') {

        let editing = document.getElementsByClassName("td_editing");
        if (editing.length > 0) {
          let el = editing[0].parentNode
          htmx.ajax('PUT', "", {source: "#" + el.id, target: "#" + el.id, values: htmx.closest(el, 'tr')})
        } else {
          let row = e.target.parentNode;
          let id = row.id.slice(3);
          let table = row.parentNode.parentNode;
          let col = 0;
          let previous = e.target.previousElementSibling;
          while (previous) {
            previous = previous.previousElementSibling;
            col += 1;
          }
          let tdId = ("td" + "_" + id + "_" + col + "_" + window.outerWidth);


          if (table.dataset.url) {
            let url = table.dataset.url;
            if (table.dataset.pk) {
              url += id;
            }
            if (table.dataset.method === "get") {
              window.document.location = url;
            } else if (table.dataset.method === "hxget") {
              htmx.ajax('GET', url, {source: '#' + row.id, target: table.dataset.target});
            }
          } else if (e.target.classList.contains("td_edit")) {
            e.target.setAttribute("id", tdId);
            htmx.ajax('GET', "", {source: '#' + tdId, target: '#' + tdId});
          }
        }
      }
    }

    function highlightRow(box) {
      let row = box.parentElement.parentElement;
      let cls = (("selected" in row.dataset) ? row.dataset.selected : "table-active");
      if (box.checked) {
        row.classList.add(cls)
      } else {
        row.classList.remove(cls)
      }
    }

// Count the number of checked rows and nake sure they are highlighted
    function countChecked() {
      if (selAll.checked) {
        return
      }
      let checked = Array.from(document.querySelectorAll(".select-checkbox:checked"));
      checked.forEach(function (e) {
        let row = e.parentElement.parentElement
        row.classList.add((("selected" in row.dataset) ? row.dataset.selected : "table-active"))
      });
      let count = checked.length;
      let countField = document.getElementById('count');
      if (countField) {
        countField.innerText = count.toString();
      }
      let actionMenu = document.getElementById('selectActionMenu');
      if (actionMenu) {
        actionMenu.disabled = (count === 0);
        actionMenu.enabled = (count > 0 || selAll.checked);
      }
    }

    // function windowSize():
    // htmx

    // function setMobileTable(selector) {
    //     // if (window.innerWidth > 600) return false;
    //     const tableEl = document.querySelector(selector);
    //     const thEls = tableEl.querySelectorAll('thead th');
    //     const tdLabels = Array.from(thEls).map(el => el.innerText);
    //     tableEl.querySelectorAll('tbody tr').forEach(tr => {
    //         Array.from(tr.children).forEach(
    //             (td, ndx) => td.setAttribute('label', tdLabels[ndx])
    //         );
    //     });
    // }

    return tb
  }

)
();
// document.addEventListener("DOMContentLoaded", (event) =>{
//   alert("DOM loaded")
// })
// window.addEventListener("hashchange", hashchange)
window.addEventListener("load", tablesPro.init)
// window.addEventListener("popstate", (event) => {
//   alert(
//     `location: ${document.location}, state: ${JSON.stringify(event.state)}`
//   );
// });
//
// function test() {
//   alert("onload")
// }
// function hashchange(){
//   alert("hashchange")
// }