const data = JSON.parse(document.getElementById("breakpoints").textContent)
window.addEventListener('load', function () {
  if (data.breakpoints.length > 0) {
    let width = 0
    for(const w of data.breakpoints){
      if (window.outerWidth >= w){width=w}
    }
    let mq = document.getElementById("media_query")
    if (mq === null){
      mq=document.createElement("div");
      mq.setAttribute("id", "media_query")
      document.body.appendChild(mq)
    }
    htmx.ajax('GET', '', {'source': '#media_query', 'values': {_width: width}})
  } else {
    tablesPro.init()
  }
})

