# Security notes

## Enforced boundaries

- Exact HTTPS hostname membership; no suffix matching, userinfo, nonstandard ports or fragment URLs. Lookalike domains are rejected before nondeterminism.
- HTML script/style removal, decoded entities, stripped tags and collapsed whitespace. JSON is parsed and serialized with sorted keys. Digest canonical extracted text, never raw bytes.
- One immediate retry on HTTP 429 or 5xx; subsequently unavailable. A source outage can yield a valid UNSUPPORTED judgment, never a fabricated quote.
- The post and page text are untrusted data. Prompt instructions say to ignore embedded instructions, while deterministic code validates labels, URL membership, quote membership and person restrictions.
- Each non-UNSUPPORTED result requires at least one exact quoted supplied source. Validators independently classify and validate leader quotes against their own reads. Comparison excludes free-form text.
- Person allegations allow only SUPPORTED/UNSUPPORTED. SUPPORTED additionally requires the validator's explicit-public-report field. Names, handles and post text are never saved. Allegation quotes are stored only as fingerprints. This is source reporting, not a guilt/innocence finding.
- All label changes and monetary settlement effects wait for protected finalized self-callbacks. Only Recheck/Appeals update Notes. Only Bonds marks deposit settlement and closes open-note quota.
- One appeal per version, immutable 72-hour original deadline, per-address open/post quotas, and pre-fetch UNCERTAIN limits. There is no small shared global quota.
- Pull withdrawals reserve attempts; paid requires finalized positive native-credit evidence with exact parent and child binding. A failed transfer alone does not enable retries before verification finalizes.

## Remaining limitations and threat model

The allegation detector and assessment of reputable explicit reporting still require honest validator consensus. Code constrains the consequences of a positive allegation flag; it cannot determine every allegation without semantic interpretation. The fixed allowlist permits particular hosts, not every factual claim hosted there. A government site or reputable outlet can be mistaken. A quote occurring on a page is not proof that its claim is accurate.

The runtime web transport may follow redirects; the contract validates the submitted host but does not claim an independently audited redirect chain. Fixed trusted-domain policy reduces exposure, and deployers must avoid open-redirect source endpoints. Full-page content can include changing navigation; canonical extraction stabilizes markup changes, not substantive text changes. Validators compare semantic decisions and citation sets rather than digests, so digest metadata describes the leader's observation and does not claim byte equality across validators.

The spam requirement and automatic detection of a same-URL edit conflict after two inconclusive attempts: a new allowlisted correction URL is necessary to open another probe without fetching first. False/nonrelevant new URLs can still consume bounded consensus. A recheck/appeal race is fail-closed by version checks, but a stale paid appeal does not yet have an automated cancel/refund branch; avoid racing these operations in the public simulator demonstration. History grows over time. The current index shows the first twelve records, not a complete production indexing service.

A wire operation is deployer-only and one-time. Its addresses are not changeable afterward, so a flawed deployed contract requires replacement and explicit migration of the app configuration. There is no administrative label, payout-recipient or balance override.

For the live proof, same-wallet writer/appellant demonstrates contract routing but does not prove independent participants. Direct tests use distinct fixture wallets and a controlled native ledger; they do not prove StudioNet consensus. Native transfer credit requires explicit protocol evidence, and unknown receipt schemas fail closed. Sources and network reads may throttle, and the API's short cache can delay presentation of a freshly finalized version.

StudioNet GEN and chain state are simulated. This release has not undergone an external security audit. The documented tests and proof manifest define the actual verified scope; no broader guarantee is implied.

## Dependency audit

The runtime-only npm audit reports zero vulnerabilities. The full audit reports five high-severity development-tool entries, all arising from the same braces <=3.0.3 stack-exhaustion advisory through the Next ESLint plugin, fast-glob and micromatch. These tools consume the fixed repository lint patterns and are not shipped as application request handlers. npm proposes downgrading eslint-config-next to Next 14; that incompatible downgrade was not applied. The raw full/runtime audit reports are committed in docs/proofs. Revisit the upstream tooling patch before accepting arbitrary glob input in a build service.
