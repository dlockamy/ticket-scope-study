// Stand-in for a compiler: every named import must be exported by the module it resolves to, and every
// SHARED_CONFIG.<field> the app reads must exist in the contract. Same file in both topologies.
const fs = require('fs'), path = require('path');
const { resolve, parseImports } = require('./mfe-resolve.cjs');
(async () => {
  const src = process.argv[2]; const code = fs.readFileSync(src, 'utf8'); let bad = 0;
  for (const imp of parseImports(code)) {
    const mod = await import(resolve(imp.pkg, path.dirname(src)));
    for (const n of imp.names) if (!(n in mod)) { console.error(`CONTRACT ERROR: ${path.basename(src)} imports { ${n} } from ${imp.pkg}, which does not export it`); bad++; }
    if (mod.SHARED_CONFIG) for (const m of code.matchAll(/SHARED_CONFIG\.(\w+)/g))
      if (!(m[1] in mod.SHARED_CONFIG)) { console.error(`CONTRACT ERROR: ${path.basename(src)} reads SHARED_CONFIG.${m[1]}, not in contract`); bad++; }
  }
  if (bad) process.exit(1);
  console.log('contract check OK');
})();
