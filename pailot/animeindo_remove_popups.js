// ==UserScript==
// @name     Unnamed Script 784834
// @version  1
// @grant    none
// ==/UserScript==

function removeElement(selector) {
  let bangsat = document.querySelectorAll(selector);
  for(let i = 0; i < bangsat.length; i++) {
    bangsat[i].remove();
  }
}

let elementsToDelete = [
  'article>span', 
  'body>script', 
  '.site-content > script:nth-child(2)', 
  '#M637953ScriptRootC1007572', 
  'div.widget_senction:nth-child(2) > div:nth-child(1) > script:nth-child(2)', 
  'div.widget_text:nth-child(3) > div:nth-child(1)',
  '#cid0020000260737301838_',
  '.container > a:nth-child(6) > script:nth-child(10)',
  '.container > a:nth-child(6) > script:nth-child(9)',
  'div.widget_senction:nth-child(2) > div:nth-child(1) > script:nth-child(1)',
  '#post-118264 > script:nth-child(7)',
  '#main > script:nth-child(3)',
  '#post-100736 > script:nth-child(7)',
  'script[src*=adskeeper]',
];

for(let i = 0; i < elementsToDelete.length; i++) {
 removeElement(elementsToDelete[i]);
}
