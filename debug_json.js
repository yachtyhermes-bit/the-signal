const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, 'articles', 'posts');
const fileName = 'pltr-enterprise-ai-bootcamps-2026.json';

try {
  const article = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, fileName), 'utf8'));
  console.log('Parsed Article:');
  console.log('  slug:', article.slug, typeof article.slug);
  console.log('  title:', article.title, typeof article.title);
  console.log('  bodyHtml:', article.bodyHtml.substring(0, 100) + '...', typeof article.bodyHtml);
  if (article.slug && article.title && article.bodyHtml) {
    console.log('  All required fields are present.');
  } else {
    console.log('  ERROR: One or more required fields are missing/falsy.');
  }
} catch (e) {
  console.error('Error parsing JSON:', e.message);
}
