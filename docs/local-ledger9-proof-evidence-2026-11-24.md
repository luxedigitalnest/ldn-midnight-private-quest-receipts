# Local Ledger 9 proof-backed redemption evidence — 24 November 2026

## Scope

This is an isolated local `undeployed` development chain on Windows, not Preprod, Preview, or Mainnet. Only the official example's prefunded local fixture and a randomly generated synthetic receipt witness were used. No personal wallet, public-chain transaction, real funds, award, or public explorer proof is claimed.

## Verified environment

- Compact compiler 0.36.1, runtime 0.21.0; generated artifact from [Actions run 45408673443](https://github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/45408673443), SHA-256 `b1bf39c44559c4b9d0aa7b015e824cb0e01f96d13fa006f9e4647d9032099208`.
- Node 22.22.3, Midnight.js/testkit 5.0.1, wallet SDK 2.0.1, node 2.1.101, indexer 4.4.101, proof server 9.0.2.
- Local-only services: 127.0.0.1:9944 (node), :8088 (indexer), :6300 (proof server).
- The official current [private-party example](https://github.com/midnightntwrk/midnight-examples/tree/main/examples/private-party) supplies the Apache-2.0 provider/wallet helpers and Docker Compose configuration. The receipt-specific integration script is separate, not a copy of the party contract. The official source at the time was retrieved from main; that external branch may change.
- The first install was interrupted and contained missing transitive dependencies. A clean isolated reinstall returned 407 packages installed and zero missing required package manifests.

## Independent chain evidence

Indexer scan found four successful deployment/redemption pairs. Connector timeout/replay appears to have run the local test more than once. These are separate synthetic contracts, not four user quest rewards. No further transaction retry is necessary.

| Deploy block | Deploy transaction hash | Contract address | Redeem block | Redeem transaction hash |
|---|---|---|---|---|
|73|ababc205ef7cde00c02b32c942c34f87dfb2f6d8b6e4812b6adc16057d308c28|5269632e2f4f4225ce7289fc9795b09355c568b6cde3bd1a81288cc20ea440d6|77|29d6cddc9a23f08e4926173c69becea5a33dce3e23e9daca71c74660c06416ed|
|85|148901c479f65194f8d3d5782253fa5acfedb4a6d6cd18f46766e0a1f900ca4a|26b07ff88e34d4d797bdafc03dc75a950b22a69e2be3af6d2eede3dfac7f6893|89|a5fd989f614d20b8db2496178b43ba04d19745f6f6d8cc75de4b1927e1fe9f5b|
|95|1edefbcec64f2e73b65fec6eda3263a6eda6ec00cbc050b08656a4004c3e9372|f582765359d5698d8273cd3572fafb701cc857d4b0f5fe8e498e6abb2fe90402|99|d05c4ff81ed7919c4dc8d58e71e575b268fa2d3674c67eb4060206b3ad8a2ffd|
|105|1b54731bfec59875804da73c809d35f5ce14d9bff8ce2a89f454e49ed6d2ef56|5038870ffd41874fa2887ede9b63f064f420b52a058de1570560386ab94f03d7|109|b2a7badfd79c4b8c08908c01f4ec963eb34b689362c277e1c80b97ea99a848fb|

All eight transactions had indexer status SUCCESS. Proof-server logs included POST /check and /prove requests during the run. Independent decoder readback for the fourth address:

```json
{"address":"5038870ffd41874fa2887ede9b63f064f420b52a058de1570560386ab94f03d7","era":"v9","redeemedNullifiers":"1","publicFields":["approvedCommitment","redeemedNullifiers"]}
```

Query while this local chain remains running (PowerShell):

```powershell
$q='{contractAction(address:"5038870ffd41874fa2887ede9b63f064f420b52a058de1570560386ab94f03d7"){__typename address ... on ContractCall{entryPoint} transaction{hash block{height} ... on RegularTransaction{transactionResult{status}}}}}'
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8088/api/v4/graphql' -ContentType 'application/json' -Body (@{query=$q}|ConvertTo-Json -Compress)
```

The full integration process stdout/exit code was not captured because the connector timed out. A second redemption rejection was included in the script, but its assertion output was not captured; do not label that separate negative integration test passed. The six prior in-memory tests including replay rejection remain independently verified. The latest local ledger contained exactly one redeemed nullifier. Local chain evidence is not externally accessible, and this document is a recorded observation, not a public explorer attestation.

## Next gate

Deploy only to an explicitly approved public test network using the current Ledger 9 SDK and a funded test wallet with spendable test DUST. Obtain public explorer transaction hashes and independently check the contract state. No production readiness, genuine off-chain issuer identity verification, mainnet transaction, or payout is established.
