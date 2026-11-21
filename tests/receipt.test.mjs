import test from 'node:test';
import assert from 'node:assert/strict';
import * as RT from '@midnight-ntwrk/compact-runtime';
import { Contract, ledger, pureCircuits } from '../contract/managed/private-quest-receipt/contract/index.js';

// Genuine generated Compact 0.36.1 contract execution. No mocks, wallet or on-chain claims.
// The in-memory runtime checks contract state and asserts; it does NOT create a ZK proof.
const COIN = '0'.repeat(64);
const bytes = (n) => new Uint8Array(32).fill(n);
const hex = (b) => Buffer.from(b).toString('hex');

async function makeSimulator(secret = bytes(7)) {
  const contract = new Contract({});
  const commitment = pureCircuits.receiptCommitment(secret);
  const initial = await contract.initialState(
    RT.createConstructorContext({}, COIN),
    commitment,
  );
  const context = RT.createCircuitContext({
    circuitId: 'redeem',
    contractAddress: RT.sampleContractAddress(),
    coinPublicKeyOrZswapState: COIN,
    contractState: initial.currentContractState,
    privateState: initial.currentPrivateState,
  });
  return { contract, commitment, context, secret };
}
function readLedger(context) {
  const state = context.callContext?.currentQueryContext?.state ??
    context.currentQueryContext?.state;
  assert.ok(state, 'Circuit result must contain verifiable ledger state');
  return ledger(state);
}
async function redeem(sim, secret) {
  const call = await sim.contract.impureCircuits.redeem(sim.context, secret);
  sim.context = call.context;
  return readLedger(sim.context);
}

test('pure commitment and nullifier are deterministic, domain separated', () => {
  const secret = bytes(9);
  assert.deepEqual(pureCircuits.receiptCommitment(secret),
    pureCircuits.receiptCommitment(secret));
  assert.notEqual(hex(pureCircuits.receiptCommitment(secret)),
    hex(pureCircuits.receiptNullifier(secret)));
  assert.notEqual(hex(pureCircuits.receiptCommitment(secret)),
    hex(pureCircuits.receiptCommitment(bytes(8))));
});
test('constructor stores only the commitment and starts with no redeemed receipts', async () => {
  const sim = await makeSimulator();
  const state = readLedger(sim.context);
  assert.equal(hex(state.approvedCommitment), hex(sim.commitment));
  assert.equal(state.redeemedNullifiers.size(), 0n);
  assert.deepEqual(Object.keys(state).sort(), ['approvedCommitment','redeemedNullifiers']);
});
test('correct private witness redeems exactly once and records a public nullifier', async () => {
  const sim = await makeSimulator();
  const state = await redeem(sim, sim.secret);
  assert.equal(state.redeemedNullifiers.size(), 1n);
  assert.equal(state.redeemedNullifiers.member(pureCircuits.receiptNullifier(sim.secret)), true);
  assert.equal(hex(state.approvedCommitment), hex(sim.commitment));
});
test('wrong receipt secret is rejected and does not alter ledger state', async () => {
  const sim = await makeSimulator();
  await assert.rejects(async () => redeem(sim, bytes(8)), /Receipt is not approved/);
  const state = readLedger(sim.context);
  assert.equal(state.redeemedNullifiers.size(), 0n);
});
test('a second redemption of the same secret is rejected', async () => {
  const sim = await makeSimulator();
  await redeem(sim, sim.secret);
  await assert.rejects(async () => redeem(sim, sim.secret), /Receipt already redeemed/);
  assert.equal(readLedger(sim.context).redeemedNullifiers.size(), 1n);
});
test('private receipt bytes are not exposed in the published ledger fields', async () => {
  const sim = await makeSimulator(bytes(77));
  const state = await redeem(sim, sim.secret);
  const publicValues = [state.approvedCommitment, ...state.redeemedNullifiers];
  assert.equal(publicValues.length, 2);
  for (const value of publicValues) {
    assert.notEqual(hex(value), hex(sim.secret));
  }
  assert.ok(publicValues.some(v => hex(v) === hex(pureCircuits.receiptNullifier(sim.secret))),
    'positive control: privacy inspection must observe the public nullifier');
});
