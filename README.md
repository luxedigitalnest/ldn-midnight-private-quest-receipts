# LDN Private Quest Receipts

**Project stage: COMPILER + IN-MEMORY TESTED SOURCE PROTOTYPE (21 November 2026). Original Compact 0.36.1 compilation and six genuine generated-runtime tests passed (0 failed). No generated zero-knowledge proof, testnet deployment, signed credential issuer, or judged submission is claimed.**

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
- [Compiler AND behavior test run — PASSED 6/6](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/44900372695): official Compact toolchain 0.36.1, `Compiling 1 circuits`, then `npm test` 6 passed / 0 failed. Genuine generated-contract in-memory calls, not mocks or an on-chain proof.\n- [`tests/receipt.test.mjs`](tests/receipt.test.mjs): deterministic hashes, distinct commitment/nullifier, constructor/public state, valid redemption, invalid witness rejection, repeat rejection and no raw secret in the public ledger.

## Planned components

- **Contract extension:** authenticated issuer permissions, multiple authorized commitments, thorough proof-system integration and deployment acceptance tests.
- **Proof client:** locally generates witnesses and submits verifier transactions through Midnight supported tooling.
- **Operator/issuer test flow:** authorize sample task commitments on a local test deployment.
- **Proof and demo:** proof server v9 end-to-end verification, original narrated evidence video, testnet transaction receipts if deployment becomes possible.
- **Mainnet plan:** signed issuer credentials, permissioned administration, accessibility QA, review of metadata leaks, security audit, and explicit operational costs.

## Evidence gates

- [x] Official Compact compiler 0.36.1 pinned in GitHub Actions
- [x] One original contract circuit builds successfully from source (job 44898737533)
- [x] AKINDO concept product registered: https://app.akindo.io/communities/JBRMPW64ecW9lKda1/products/zK3AJ8lmLC7XnXQk
- [x] Six positive/negative in-memory generated-contract tests pass (run 44900372695)
- [ ] Local proof generated and contract call verified
- [ ] Optional testnet deployment with explorer hash and cost evidence
- [ ] Original 3-minute-or-less playable demonstration
- [ ] AKINDO final judged Wave 3 submission (product listing alone is NOT a submission)

Compilation + real in-memory runtime tests are genuine milestones, but do not establish cryptographic proof or public deployment. The project is not production-safe or fully eligible for a judged entry until organizer requirements are met. No reward, payout, or accepted submission is claimed.

## Reproduce the verified tests\n\nThe GitHub Actions workflow checks out the exact public source and performs:\n\n```bash\ncompact update 0.36.1\ncompact compile contract/private-quest-receipt.compact contract/managed/private-quest-receipt\nnpm install --no-audit --no-fund\nnpm test\n```\n\nThe official workflow is [compact-compile.yml](.github/workflows/compact-compile.yml). Required versions: Node.js 22+, Compact toolchain 0.36.1, Compact runtime 0.21.0. **Do not treat an in-memory test as a ZK proof, deployment, or chain receipt.**\n\n## References

- [Midnight docs: toolchain installation](https://docs.midnight.network/getting-started/installation)
- [Midnight docs: private smart contracts](https://docs.midnight.network/guides/build-a-private-smart-contract)
- [Midnight buildathon](https://app.akindo.io/wave-hacks/jaMZjqPOBsLXvjdG)

## License

Apache License 2.0. See [LICENSE](LICENSE).
