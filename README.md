# LDN Private Quest Receipts

**Project stage: SOURCE PROTOTYPE / COMPILER VERIFIED (21 November 2026). The original Compact 0.36.1 circuit compiles in GitHub Actions. No behavioral tests, local proof, testnet deployment, signed issuance, playable demo or judged submission are claimed.**

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
- [GitHub Actions compiler log — passed](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/44898737533): official Compact 0.36.1, `Compiling 1 circuits`, successful job. This checks syntax/code generation only.

## Planned components

- **Contract extension:** authenticated issuer permissions, multiple authorized commitments and replay tests.
- **Proof client:** locally generates witnesses and submits verifier transactions through Midnight supported tooling.
- **Operator/issuer test flow:** authorize sample task commitments on a local test deployment.
- **Demo and tests:** one valid completion, one nonmatching receipt rejection, and one replay rejection.
- **Mainnet plan:** signed issuer credentials, permissioned administration, accessibility QA, review of metadata leaks, security audit, and explicit operational costs.

## Evidence gates

- [x] Official Compact compiler 0.36.1 pinned in GitHub Actions
- [x] One original contract circuit builds successfully from source (job 44898737533)
- [x] AKINDO concept product registered: https://app.akindo.io/communities/JBRMPW64ecW9lKda1/products/zK3AJ8lmLC7XnXQk
- [ ] Automated positive and negative circuit tests pass
- [ ] Local proof generated and contract call verified
- [ ] Optional testnet deployment with explorer hash and cost evidence
- [ ] Original 3-minute-or-less playable demonstration
- [ ] AKINDO final judged Wave 3 submission (product listing alone is NOT a submission)

Compilation is one genuine technical requirement, but by itself it does not establish a functional or eligible final entry. No reward, payout, or accepted submission is claimed.

## References

- [Midnight docs: toolchain installation](https://docs.midnight.network/getting-started/installation)
- [Midnight docs: private smart contracts](https://docs.midnight.network/guides/build-a-private-smart-contract)
- [Midnight buildathon](https://app.akindo.io/wave-hacks/jaMZjqPOBsLXvjdG)

## License

Apache License 2.0. See [LICENSE](LICENSE).
