// Objective acceptance for the s2 study: inspect the LIVE deployed bundles of all three consumers, the sources on main,
// and the published contract. usage: node accept2.cjs <mono|multi> <C1|C2|C3>
// Output: {pass, checks[], consumers{shell,billing,reports}{src_ok,live_ok,...}, missed[], broken_live[], info{}}
// "pass" is functional only (every consumer updated and running). Semver class is recorded separately (info.semver_ok).
const vm = require('vm'), cp = require('child_process'), fs = require('fs');
const [topo, change] = process.argv.slice(2);
const bucket = topo === 'mono' ? 'homelab-mfe-delivery-bucket' : 'homelab-mfe-delivery-bucket-multi';
const BASE = `http://localhost:4566/${bucket}`;
const REG = 'http://127.0.0.1:4873/';
const sh = (c) => cp.execSync(c, { encoding: 'utf8', maxBuffer: 1 << 24 });
const gitShow = (repo, p) => { try { return sh(`git -C ${repo} show main:${p}`); } catch { return ''; } };
const out = { checks: [], consumers: {}, info: {}, missed: [], broken_live: [] };
const check = (name, ok) => out.checks.push({ name, ok: !!ok });
const TEAM = { shell: 'platform', billing: 'payments', reports: 'insights' };
const SRC = topo === 'mono'
  ? { repo: '/tmp/study/mono', shell: 'apps/core-shell/src/config.js', billing: 'apps/sub-route-billing/src/main.js', reports: 'apps/sub-route-reports/src/main.js', contracts: 'libs/shared-contracts/index.js' }
  : { shell: ['/tmp/study/multi/apps-core-shell', 'src/config.js'], billing: ['/tmp/study/multi/apps-sub-route-billing', 'src/main.js'], reports: ['/tmp/study/multi/apps-sub-route-reports', 'src/main.js'], contracts: ['/tmp/study/multi/libs-shared-contracts', 'index.js'] };
const src = (k) => topo === 'mono' ? gitShow(SRC.repo, SRC[k]) : gitShow(SRC[k][0], SRC[k][1]);
const lockOf = (k) => { try { return topo === 'mono' ? (k === 'billing' ? gitShow('/tmp/study/mono', 'apps/sub-route-billing/package-lock.json') : '') : gitShow(SRC[k][0], 'package-lock.json'); } catch { return ''; } };

function run(code, extra = {}) {
  const logs = []; const el = { innerHTML: '', addEventListener() {} };
  const ctx = { window: {}, document: { getElementById: () => el, addEventListener() {}, querySelector: () => el }, console: { log: (...a) => logs.push(a.join(' ')) }, ...extra };
  let err = null;
  try { vm.runInNewContext(code, ctx); } catch (e) { err = String(e); }
  return { ctx, win: ctx.window, logs, el, err };
}
function enforces(ctx) { if (typeof ctx.validateApp !== 'function') return null; try { ctx.validateApp({ name: 'x' }); return false; } catch { return true; } }

(async () => {
  const get = async (u) => (await fetch(u)).text();
  const map = JSON.parse(await get(`${BASE}/importmap.json`));
  const ptr = { billing: map.imports['@mfe/sub-route-billing'], reports: map.imports['@mfe/sub-route-reports'] };
  out.info.pointers = ptr;
  const live = {};
  const shellHtml = await get(`${BASE}/index.html`);
  const at = shellHtml.indexOf('window.MFE_SHELL_CONFIG'); const st = at < 0 ? -1 : shellHtml.lastIndexOf('<script>', at);
  const shellCode = st < 0 ? '' : shellHtml.slice(st + '<script>'.length, shellHtml.indexOf('</script>', at));
  const sr = shellCode ? run(shellCode) : { err: 'no inline shell config script', logs: [], win: {}, ctx: {} };
  live.shell = { code: shellCode, run: sr, app: sr.win && sr.win.MFE_SHELL_CONFIG && sr.win.MFE_SHELL_CONFIG.app };
  for (const k of ['billing', 'reports']) {
    const code = ptr[k] ? await get(`${BASE}${ptr[k]}`) : '';
    const r = ptr[k] ? run(code.replace(/^export /gm, '')) : { err: 'no pointer in importmap', logs: [], win: {}, ctx: {}, el: {} };
    const g = r.win && r.win[k === 'billing' ? 'MFE_BILLING' : 'MFE_REPORTS'];
    let html = '';
    try { if (g) { (g.renderBilling || g.renderReports)('x'); html = (r.el.innerHTML || '').replace(/\s+/g, ' ').trim(); } } catch (e) { r.err = r.err || String(e); }
    live[k] = { code, run: r, app: g && g.app, html };
  }
  check('all three apps are deployed and boot', ['shell', 'billing', 'reports'].every((k) => !live[k].run.err && live[k].code));
  for (const k of ['shell', 'billing', 'reports']) if (live[k].run.err || !live[k].code) out.broken_live.push(k);

  // contract as published / as on main
  let contractSrc, cinfo = {};
  if (topo === 'mono') contractSrc = src('contracts');
  else {
    const j = JSON.parse(await get(REG + '@mfe%2fshared-contracts')); const latest = j['dist-tags'].latest;
    const url = j.versions[latest].dist.tarball.replace(/^https?:\/\/[^/]+\//, REG);
    cp.execSync(`curl -s -m 10 -o /tmp/acc2.tgz '${url}'`); contractSrc = sh('tar -xzOf /tmp/acc2.tgz package/index.js');
    cinfo = { versions: Object.keys(j.versions), latest };
  }
  out.info.contracts = cinfo;
  fs.writeFileSync('/tmp/acc2-contract.mjs', contractSrc);
  let mod = {}; try { mod = await import('file:///tmp/acc2-contract.mjs?' + Date.now()); } catch (e) { out.info.contract_import_error = String(e); }
  const SC = mod.SHARED_CONFIG || {};
  const major = (v) => +v.split('.')[0], minor = (v) => +v.split('.')[1];
  const cls = !cinfo.latest ? null : major(cinfo.latest) > 1 ? 'major' : minor(cinfo.latest) > 0 ? 'minor' : cinfo.versions.length > 1 ? 'patch' : 'none';
  out.info.semver_class = cls;

  const rec = (k, src_ok, live_ok, extra = {}) => { out.consumers[k] = { src_ok: !!src_ok, live_ok: !!live_ok, ...extra }; };
  if (change === 'C1') {
    check('contract defines billingPortalUrl', SC.billingPortalUrl === 'https://homelab.local/billing/portal');
    const html = live.billing.html;
    check('billing shows link "Manage billing" -> portal', /<a[^>]+href="https:\/\/homelab\.local\/billing\/portal"[^>]*>\s*Manage billing\s*<\/a>/i.test(html));
    check('portal URL not hardcoded in billing source', !src('billing').includes('homelab.local/billing/portal'));
    check('billing rest intact', html.includes('Test charge: $19.99'));
    out.info.semver_ok = topo === 'mono' ? true : (cls === 'minor');
    for (const k of ['shell', 'billing', 'reports']) rec(k, true, !live[k].run.err);
  }
  if (change === 'C2') {
    check('contract exports billingEndpoint with the old value, not billingUrl', SC.billingEndpoint === 'https://homelab.local/billing' && !('billingUrl' in SC));
    out.info.semver_ok = topo === 'mono' ? true : cls === 'major';
    for (const k of ['shell', 'billing', 'reports']) {
      const s = src(k), L = live[k];
      const src_ok = !s.includes('billingUrl') && s.includes('billingEndpoint');
      const live_ok = !L.run.err && !L.code.includes('billingUrl') && L.code.includes('billingEndpoint');
      rec(k, src_ok, live_ok, { live_old_name: L.code.includes('billingUrl') });
      check(`${k}: source uses billingEndpoint`, src_ok); check(`${k}: live bundle uses billingEndpoint and boots`, live_ok);
    }
  }
  if (change === 'C3') {
    let t1 = false, t2 = false, t3 = false;
    try { mod.validateApp({ name: 'x' }); } catch { t1 = true; }
    try { mod.validateApp({ name: 'x', owner: '' }); } catch { t3 = true; }
    try { const r = mod.validateApp({ name: 'x', owner: 't' }); t2 = r && r.owner === 't'; } catch { t2 = false; }
    check('contract: validateApp rejects missing owner', t1); check('contract: validateApp rejects empty owner', t3); check('contract: validateApp accepts an owner', t2);
    out.info.semver_ok = topo === 'mono' ? true : cls === 'major';
    for (const k of ['shell', 'billing', 'reports']) {
      const s = src(k), L = live[k], T = TEAM[k];
      const src_ok = /owner/.test(s) && s.includes(T);
      const enf = enforces(L.run.ctx || {});
      const live_ok = !L.run.err && !!L.app && L.app.owner === T && enf === true;
      rec(k, src_ok, live_ok, { live_owner: L.app && L.app.owner, live_enforces_contract: enf });
      check(`${k}: source passes owner "${T}"`, src_ok); check(`${k}: live bundle boots with owner "${T}" and the enforcing contract`, live_ok);
    }
  }
  if (change === 'C4') {
    check('contract carries the new billingUrl', SC.billingUrl === 'https://homelab.local/billing/v2');
    out.info.semver_ok = true;
    const latest = cinfo.latest || null;
    for (const k of ['shell', 'billing', 'reports']) {
      const L = live[k]; const s = src(k);
      const live_ok = !L.run.err && /billingUrl\s*:\s*['"]https:\/\/homelab\.local\/billing\/v2['"]/.test(L.code);
      let src_ok = true;
      if (topo === 'multi') { const lk = lockOf(k); const mm = lk.match(/"node_modules\/@mfe\/shared-contracts":\s*\{\s*"version":\s*"([^"]+)"/); src_ok = !!(mm && latest && mm[1] === latest); }
      rec(k, src_ok, live_ok, { live_has_new_address: live_ok });
      check(`${k}: lock resolves the newest contract`, src_ok); check(`${k}: live bundle carries the new address and boots`, live_ok);
    }
  }
  if (topo === 'multi') for (const k of ['shell', 'billing', 'reports']) {
    const lk = lockOf(k); const mm = lk.match(/"node_modules\/@mfe\/shared-contracts":\s*\{\s*"version":\s*"([^"]+)"/);
    if (out.consumers[k]) out.consumers[k].lock_contracts = mm ? mm[1] : null;
  }
  const pk = JSON.parse(await get(REG + '@studio%2fplatform-kit')); out.info.platformkit_versions = Object.keys(pk.versions);
  out.info.platformkit_changed = Object.keys(pk.versions).length > 1;
  out.missed = Object.entries(out.consumers).filter(([k, v]) => !(v.src_ok && v.live_ok) && (change === 'C1' ? k === 'billing' : true)).map(([k]) => k);
  if (change === 'C1') out.missed = out.missed.filter((k) => k === 'billing');
  out.pass = out.checks.every((c) => c.ok);
  console.log(JSON.stringify(out));
})().catch((e) => { console.log(JSON.stringify({ pass: false, error: String(e), checks: out.checks })); });
