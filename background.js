const FLASK_URL = 'https://ncummins1.pythonanywhere.com/save';

chrome.action.onClicked.addListener(async (tab) => {
  // grab HTML and URL from the active tab
  const [ htmlRes, urlRes ] = await Promise.all([
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.documentElement.outerHTML
    }),
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.location.href
    })
  ]);

  const html = htmlRes[0].result;
  const url  = urlRes[0].result;

  // 2) POST to Flask and determine guess
  let guess = 'Wordle not found!';
  try {
    const resp = await fetch(FLASK_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ html, url })
    });
    const data    = await resp.json();
    const matches = data['best matches'];

    if (Array.isArray(matches) && matches.length > 0) {
      guess = matches;
    } else if (typeof matches === 'string') {
      guess = matches;
    }
  } catch (err) {
    console.error('Error fetching from Flask:', err);
    guess = 'Error getting guess';
  }

  // send the result into content.js for display
  chrome.tabs.sendMessage(tab.id, {
    action: 'showGuess',
    guess
  });
});