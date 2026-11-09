# Contributing

- Work on a branch and open a PR against `main`. CI must be green to merge. Merging to `main` triggers CD automatically.
- Build locally: `export MFE_REGISTRY=http://127.0.0.1:4873/` and run `npm run build` (dependencies come from our private npm registry). Do not run `make build-*` targets: they publish to the shared environment.
- Shared libraries are published to the private registry by CD when merged to `main`. The release is the `version` in `package.json`: CD publishes only if that version is not already in the registry, so bump it (semver: breaking = major, additive = minor, fix = patch). An unchanged version publishes nothing.
- Applications depend on libraries through version ranges in `package.json` with a committed `package-lock.json`. A newly published library version changes no application until that application updates its dependency (`npm install <package>@<range>`, commit `package.json` and `package-lock.json`) and ships again.
- Applications ship by merging to `main`: CD builds and uploads to the CDN bucket.
- Prefer one PR per ticket unless changes must land in a particular order.
