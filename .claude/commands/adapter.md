---
description: Add or change a payment processor adapter against the frozen contract and its test matrix
argument-hint: airwallex | stripe | sandbox
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

Add or update the **$ARGUMENTS** processor. The contract is frozen (`src/lib/processors/types.ts`, master spec
§4.1) — you are implementing it, not designing it.

## Rules that are not negotiable

1. **Implement the interface as it exists.** If a method does not fit, stop and write an ADR — do not add an
   optional method, a cast, or a second interface.
2. **Vendor SDK imports live only in `src/lib/processors/<name>.ts`.** Nothing else imports the SDK.
3. **Sandbox first.** Implement against the processor's test mode with recorded fixtures; live keys are a
   deployment concern, never a test dependency.
4. **A decline is data, not an exception.** Return `{ ok: false, code, declineClass, retryable }`.
5. **Unknown status or decline code → `requires_review`.** Never map an unknown to success.
6. **Every call carries an idempotency key** derived from the payment, not from the attempt.
7. **Webhooks:** verify on the **raw** body before parsing, at the edge of the request. Normalise into
   `NormalizedEvent`; do not invent event names.
8. **Capabilities are data** (`ProcessorCapabilities`). If the processor cannot do something, the UI hides it.
9. **Raw payloads are stored encrypted** (`payment_attempts.raw_response_ciphertext`).

## Do this

1. Read `src/lib/processors/types.ts`, `normalize.ts`, and the existing `sandbox.ts`. List the methods and which
   ones this adapter will implement now (the rest throw `NotImplemented` with a linked step).
2. Write the **contract test first**: run the shared matrix against this adapter
   (`pnpm test:contract -- processor`), watch it fail, then implement until it passes.
3. Add the decline-code mappings to `normalize.ts` — table-driven, with a test that fails on any unmapped code.
4. Record fixtures for: success, decline (insufficient funds, do-not-honor, expired card), 3DS challenge,
   timeout followed by a status fetch, refund full and partial, and a replayed webhook.
5. Register the processor in `registry.ts` and the capability flags.
6. Prove it: paste the contract-test output, plus one sandbox payment end to end with the webhook replayed
   twice and posted once in the ledger.

Finally, answer: **what did you have to work around, and does the interface need an ADR?**
