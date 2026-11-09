// Core-shell "bundler": compile check, then inline src/config.js (and what it imports) into dist/index.html.
// Same file in both topologies.
const fs = require('fs'), path = require('path'), cp = require('child_process');
const helper = [path.join(__dirname, 'scripts', 'mfe-resolve.cjs'), path.join(__dirname, '..', '..', 'scripts', 'mfe-resolve.cjs')].find(fs.existsSync);
const { resolve, parseImports } = require(helper);
const srcHtml = path.join(__dirname, 'src', 'index.html'), cfgFile = path.join(__dirname, 'src', 'config.js'), distDir = path.join(__dirname, 'dist');
cp.execFileSync('node', [path.join(path.dirname(helper), 'check-contract.cjs'), cfgFile], { stdio: 'inherit' });
let cfg = fs.readFileSync(cfgFile, 'utf8');
for (const imp of parseImports(cfg)) {
  const body = fs.readFileSync(resolve(imp.pkg, __dirname), 'utf8').replace(/^export /gm, '');
  cfg = cfg.replace(imp.stmt, `// --- inlined module ---\n${body}\n// --- end inlined module ---`);
}
cfg = cfg.replace(/^export /gm, '');
let html = fs.readFileSync(srcHtml, 'utf8');
if (!html.includes('</body>')) throw new Error('index.html has no </body>');
html = html.replace('</body>', `<script>\n${cfg}\nwindow.MFE_SHELL_CONFIG = shellConfig;\n</script>\n</body>`);
fs.mkdirSync(distDir, { recursive: true });
fs.writeFileSync(path.join(distDir, 'index.html'), html);
console.log('Core shell app compiled successfully to dist/index.html');
