// Resolve a bare import the way this study's build does: an installed package first (registry dependency),
// then an in-repo lib (libs/<name>/index.js, found by walking up). Same file in both topologies.
const fs = require('fs'), path = require('path');
function up(dir, rel) {
  for (let d = dir; ; d = path.dirname(d)) {
    const p = path.join(d, rel);
    if (fs.existsSync(p)) return p;
    if (d === path.dirname(d)) return null;
  }
}
function resolve(pkg, fromDir) {
  const nm = up(fromDir, path.join('node_modules', pkg, 'index.js'));
  if (nm) return nm;
  const lib = up(fromDir, path.join('libs', pkg.split('/').pop(), 'index.js'));
  if (lib) return lib;
  throw new Error(`cannot resolve ${pkg} from ${fromDir}`);
}
function parseImports(src) {
  const out = []; const re = /import\s*\{([^}]*)\}\s*from\s*['"]([^'"]+)['"];?/g; let m;
  while ((m = re.exec(src))) out.push({ stmt: m[0], pkg: m[2], names: m[1].split(',').map(s => s.trim().split(/\s+as\s+/)[0]).filter(Boolean) });
  return out;
}
module.exports = { resolve, parseImports };
