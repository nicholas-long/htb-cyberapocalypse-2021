async function getResults() {
  const query = document.getElementById("query").value;
  const xml = `<?xml version="1.0" encoding="ISO-8859-1"?><root><query>${query}</query></root>`;
  const response = await fetch('/search', {
    method: 'POST',
    headers: {
      'Content-Type' : 'application/xml'
    },
    body: xml
  });
  var results = "";
  const data = await response.json().then(async data => {
    for(var i = 0; i < data.length - 1; i++) {
      result = data[i];
      results += `<div class="message"><div class="message__body"><div class="content"><span class="name">${result.name}</span><div>${result.desc}</div></div><div class="image"><img src="images/${result.url}" width="100" height="100"></div></div></div>`;
    }
  })
  document.getElementById('results').innerHTML = results;
}

document.getElementById('btn').addEventListener("click", getResults);
