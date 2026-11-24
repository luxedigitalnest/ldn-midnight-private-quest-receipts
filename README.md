# LDN Private Quest Receipts

**Project stage (24 November 2026): Original Compact 0.36.1 compiler and six generated-runtime tests passed (0 failed) in [GitHub Actions](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/44900372695). A second [CI run](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/45408673443) produced a downloadable generated contract artifact, whose SHA-256 was verified before extraction on Windows; all six local runtime tests passed there as well. An original [video demonstration](https://www.youtube.com/watch?v=VxWXyj1s_vQ) is published. The [AKINDO product page](https://app.akindo.io/communities/JBRMPW64ecW9lKda1/products/zK3AJ8lmLC7XnXQk) explicitly lists the product as **Submitted to** Midnight Buildathon Wave 3. Local Ledger 9 deployment and proof-backed redemption succeeded on an isolated Windows development chain; [local evidence and limitations](docs/local-ledger9-proof-evidence-2026-11-24.md). No organizer award, prize, public testnet transaction, or production readiness is claimed.**

This is an original, Apache-2.0-licensed experimental Midnight project from [LuxeDigitalNest Privacy Builders](https://app.akindo.io/communities/JBRMPW64ecW9lKda1), prepared for the privacy-first Midnight buildathon.

## Problem

Users who complete optional quests, training challenges, or accessibility-related tasks often must reveal an address, full task history, or personal identifiers just to prove one requirement was satisfied. A conventional public ledger can permanently expose too much information.

## Intended MVP

A privacy-conscious receipt checker that:

1. Lets an **authorized issuer** approve a task-completion commitment without storing the user's name or the underlying activity description on-chain.
2. Lets a participant demonstrate possession of a matching secret locally, using a Midnight Compact circuit and a publicly visible *single-use nullifier*, while keeping the full receipt and salt private.
3. Rejects a nullifier that has already been redeemed and exposes only whether a specific verification is valid.
4. Produces a reproducible local demonstration, contract tests, and a public repository with a release-compatible compiler manifest.

**Limits:** Merely knowing a secret is not evidence of authentic off-chain completion; issuer authentication and a trustworthy issuer-to-user credential process are required. A public nullifier and transaction timing can still reveal metadata. This design is not an anonymity guarantee or a production security audit.

## Implemented source prototype

- [`contract/private-quest-receipt.compact`](contract/private-quest-receipt.compact): one issuer-supplied *constructor* commitment per deployment, one private witness input, a domain-separated public nullifier, and a `Set` intended to reject replay. This is **not** multi-issuer authorization or production credential verification.
- [Compiler AND behavior test run — PASSED 6/6](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/44900372695): official Compact toolchain 0.36.1, `Compiling 1 circuits`, then `npm test` 6 passed / 0 failed. Genuine generated-contract in-memory calls, not mocks or an on-chain proof.
- [`tests/receipt.test.mjs`](tests/receipt.test.mjs): deterministic hashes, distinct commitment/nullifier, constructor/public state, valid redemption, invalid witness rejection, repeat rejection and no raw secret in the public ledger.

## Planned components

- **Contract extension:** authenticated issuer permissions, multiple authorized commitments, thorough proof-system integration and deployment acceptance tests.
- **Proof client:** locally generates witnesses and submits verifier transactions through Midnight supported tooling.
- **Operator/issuer test flow:** authorize sample task commitments on a local test deployment.
- **Proof and demo:** local proof server v9 redemption verified; publish a revised original narrated walkthrough and obtain public testnet transaction receipts only when authorized.
- **Mainnet plan:** signed issuer credentials, permissioned administration, accessibility QA, review of metadata leaks, security audit, and explicit operational costs.

## Original hackathon presentation

- [2:19 YouTube technical walkthrough (unlisted, playable)](https://youtu.be/VxWXyj1s_vQ) — original project-specific narration and 7 visual slides, verified contract CI results, truthful remaining limitations.
- [MP4 in repository](media/LDN_Private_Quest_Receipts_Genuine_Technical_Walkthrough.mp4) — original H.264/AAC 1280×720 source artifact.
- [Seven-slide pitch PDF](media/LDN_Private_Quest_Receipts_Pitch_Deck.pdf) — judges can inspect without video.
- [Editable 7-slide PPTX](media/LDN_Private_Quest_Receipts_Pitch_Deck.pptx).
- [Reproducible original video + deck generator](scripts/make_midnight_demo.py).

## Evidence gates

- [x] Official Compact compiler 0.36.1 pinned in GitHub Actions
- [x] One original contract circuit builds successfully from source (job 44898737533)
- [x] AKINDO concept product registered: https://app.akindo.io/communities/JBRMPW64ecW9lKda1/products/zK3AJ8lmLC7XnXQk
- [x] Six positive/negative in-memory generated-contract tests pass (run 44900372695)
- [x] Local Ledger 9 proof-backed contract redemption and ledger readback verified (see [local chain evidence](docs/local-ledger9-proof-evidence-2026-11-24.md)); full negative integration test stdout unavailable
- [ ] Optional testnet deployment with explorer hash and cost evidence
- [x] Original 2:19 narrated, playable demonstration (https://youtu.be/VxWXyj1s_vQ) and 7-slide deck; original video predates local-chain verification
- [x] Product submitted to the AKINDO Midnight Buildathon Wave 3 (the [official product page](https://app.akindo.io/communities/JBRMPW64ecW9lKda1/products/zK3AJ8lmLC7XnXQk) labels the Wave under **Submitted to**); judging outcome and prize unconfirmed

Compilation and in-memory runtime tests alone do not establish a cryptographic proof. The later isolated Ledger 9 proof-backed redemption is a separate verified milestone, not a public deployment. The existing AKINDO Wave 3 product submission is not a judging decision: review, eligibility acceptance, awards and payouts remain unconfirmed. This code is not production-safe.

## Reproduce the verified tests

The GitHub Actions workflow checks out the exact public source and performs:

```bash
compact update 0.36.1
compact compile contract/private-quest-receipt.compact contract/managed/private-quest-receipt
npm install --no-audit --no-fund
npm test
```

The official workflow is [compact-compile.yml](.github/workflows/compact-compile.yml). Required versions: Node.js 22+, Compact toolchain 0.36.1, Compact runtime 0.21.0. **Do not treat an in-memory test as a ZK proof, deployment, or chain receipt.**

### Reproduce with the published compiler output (Windows)

The [successful run 45408673443](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/45408673443) produced `compact-0.36.1-private-quest-receipt.zip` (artifact 14926583270, seven-day retention). Its SHA-256 is `b1bf39c44559c4b9d0aa7b015e824cb0e01f96d13fa006f9e4647d9032099208`. Download from the authenticated GitHub Actions page, verify the digest, and extract into the previously absent `contract/managed/private-quest-receipt/` directory. With the pinned runtime installed, run `node --test tests/receipt.test.mjs` from the repository root. On 24 November 2026 this exact procedure returned 6 passed, 0 failed, exit code 0 on Windows. The generated files are not committed; if the artifact expires, rerun the compiler workflow or compile with the pinned toolchain.

This particular offline procedure is still only in-memory execution. The later local-network evidence is recorded separately; no public-chain deployment is established.

## References

- [Midnight docs: toolchain installation](https://docs.midnight.network/getting-started/installation)
- [Midnight docs: private smart contracts](https://docs.midnight.network/guides/build-a-private-smart-contract)
- [Midnight buildathon](https://app.akindo.io/wave-hacks/jaMZjqPOBsLXvjdG)

## License

Apache License 2.0. See [LICENSE](LICENSE).
