const fs = require('fs');
const html = fs.readFileSync('VoltRoof_Combined.html', 'utf8');

// Find where cfgPanel is populated
const optIdx = html.indexOf('populateModuleRatingSelects');
if (optIdx !== -1) {
  console.log('populateModuleRatingSelects found:');
  console.log(html.substring(optIdx, optIdx + 800));
} else {
  // search cfgPanel in html
  const selIdx = html.indexOf('id="cfgPanel"');
  console.log('cfgPanel html:');
  console.log(html.substring(selIdx - 200, selIdx + 400));
}
