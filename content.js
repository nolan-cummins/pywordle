chrome.runtime.onMessage.addListener((msg) => {
  if (msg.action !== 'showGuess') return;

  const g = msg.guess;

  // remove any old overlay
  let overlay = document.getElementById('pywordle-guess');
  if (overlay) {
    overlay.remove();
  }

  // create & style a new overlay
  overlay = document.createElement('div');
  overlay.id = 'pywordle-guess';
  Object.assign(overlay.style, {
    position:     'fixed',
    top:          '10px',
    right:        '10px',
    background:   'rgba(0, 0, 0, 0.78)',
    color:        '#fff',
    padding:      '4px 8px',       // reduced padding
    borderRadius: '4px',
    fontFamily:   'sans-serif',
    fontSize:     '13px',          // slightly smaller font
    lineHeight:   '1.4',
    maxWidth:     '180px',
    zIndex:       '2147483647',
    boxShadow:    '0 2px 6px rgba(0,0,0,0.5)'
  });

  // fill it with either a list or single string
  if (Array.isArray(g) && g.length) {
    const ol = document.createElement('ol');
    ol.style.margin = '0';
    ol.style.paddingLeft = '20px';  // for list indent
    g.forEach(word => {
      const li = document.createElement('li');
      li.textContent = word;
      li.style.margin = '2px 0';    // small space between items
      ol.appendChild(li);
    });
    overlay.appendChild(ol);
  } else if (typeof g === 'string' && g.length) {
    overlay.textContent = g;
  } else {
    overlay.textContent = 'Wordle not found!';
  }

  // 4) Add it to the page
  document.documentElement.appendChild(overlay);
});