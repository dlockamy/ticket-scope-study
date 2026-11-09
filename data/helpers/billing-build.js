// Billing "bundler": compile check, then inline every imported module into dist/main.js
// (README: "shared config, inlined into the bundle at build time"). Same file in both topologies.
const fs = require('fs'), path = require('path'), cp = require('child_process');
const helper = [path.join(__dirname, 'scripts', 'mfe-resolve.cjs'), path.join(__dirname, '..', '..', 'scripts', 'mfe-resolve.cjs')].find(fs.existsSync);
const { resolve, parseImports } = require(helper);
const srcFile = path.join(__dirname, 'src', 'main.js');
const distDir = path.join(__dirname, 'dist');
cp.execFileSync('node', [path.join(path.dirname(helper), 'check-contract.cjs'), srcFile], { stdio: 'inherit' });
let code = fs.readFileSync(srcFile, 'utf8');
for (const imp of parseImports(code)) {
  const body = fs.readFileSync(resolve(imp.pkg, __dirname), 'utf8').replace(/^export /gm, '');
  code = code.replace(imp.stmt, `// --- inlined module ---\n${body}\n// --- end inlined module ---`);
}
fs.mkdirSync(distDir, { recursive: true });
fs.writeFileSync(path.join(distDir, 'main.js'), code);
console.log('Billing micro-frontend compiled successfully to dist/main.js');
