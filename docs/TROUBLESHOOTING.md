# Troubleshooting — how to find the cause without thrashing

Two rules before anything else:

1. **Reproduce, or it is not a bug.** Capture five identifiers: request id, merchant id, invoice/payment id,
   session id, commit sha. Without them you are guessing, and an AI agent guessing is expensive.
2. **Two strikes.** If the same error survives two fix attempts, stop. Write down the exact command, the exact
   output, and what you tried — then ask. Thrashing is the single largest time sink in this repository.

Then use the ladder. Every entry is a **symptom family**, and the checks are ordered cheapest-first — the
first three catch most cases.

## 1. "It returns nothing / an empty list"

| # | Check | Where |
|---|---|---|
| 1 | Is the query running as `authenticated` and not the table owner? RLS is bypassed for owners | `select current_user, session_user` in the failing path |
| 2 | Is `merchant_id` actually in the session/JWT and equal to the row's? | `active_merchant_id` on the session row |
| 3 | Does the policy have `USING` but no `WITH CHECK` (or the reverse) for this operation? | the table's policies |
| 4 | Is the table `force row level security`? Without it, owners bypass | `pg_class.relforcerowsecurity` |
| 5 | Did a recent migration add the table but skip the exposure block (§7.9)? | `information_schema.table_privileges` |

**Known trap:** a SECURITY DEFINER function owned by a non-bypass role plus forced RLS returns zero rows
(pitfall 4). Own ledger/RPC functions as `postgres` and test them *as* `authenticated`.

## 2. "The money is wrong"

Order matters here — check in this sequence, because each one invalidates the next.

| # | Question | If yes |
|---|---|---|
| 1 | Did a JS `number` ever touch it? | pitfall 2 — `numeric` arrives as a string; assert `typeof === 'string'` and add the OID 1700 parser |
| 2 | Is the number **computed** or **derived from the ledger**? | statements must derive from `ledger_entries` only (pitfall 17) |
| 3 | Is the currency's exponent assumed to be 2? | JPY 0, KWD 3 — exponent is data (`CHANGE-PLAYBOOK.md` R2) |
| 4 | Is it a rounding-each-line vs sum-then-round difference? | the allocation rule is per-currency and must be an explicit test |
| 5 | Is the query cutting on a date in a different timezone? | all date maths in UTC, display in the merchant's zone |
| 6 | Does a balance differ from the sum of its postings? | ledger imbalance → runbook `ledger-imbalance.md`; **do not** edit rows |

A wrong number is never fixed by changing the display layer. Find the posting.

## 3. "A payment is stuck in pending / processing"

1. **Compare states**: what does the processor say (`PaymentProvider.retrieve`) versus our state machine?
2. **Did the webhook arrive?** Look for the `(processor, event_id)` row. If absent, the gateway rejected the
   signature, timed out, or retried — check the processor's delivery log.
3. **Did it arrive but do nothing?** The event was deduped or the worker never picked it up: inspect
   `private.outbox`, the worker lease, and the dead-letter count.
4. **Did the worker run but the commit failed?** Look for a ledger error — a failed `ledger_balance_guard`
   rolls the whole transaction back, which is correct but looks like "nothing happened".
5. **Idempotency collision?** A reused `Idempotency-Key` returns the first result by design; confirm the key
   was not generated per-attempt instead of per-payment.

## 4. "Two charges / a double post"

| # | Check |
|---|---|
| 1 | Was the client retry keyed? `(merchant_id, key, scope)` must be a primary key (pitfall 15) |
| 2 | Is there a partial unique index preventing a second payment on one invoice? |
| 3 | Was the lock taken in the **same** transaction as the insert (`for update` on the merchant/invoice)? |
| 4 | Did the processor send two different `event_id`s for one payment? Dedupe on the payment ref too, not only the event id |
| 5 | Did a refund/reversal get posted as a new payment instead of a reversing entry? |

If money already moved twice: freeze payouts (`payouts_enabled=false`), snapshot, post a **reversing**
transaction, then investigate. Never delete or edit a posting.

## 5. "Merchant webhooks are not arriving"

1. Is there a row in the delivery table at all? No row → the event was never emitted (check the emitting
   transaction committed).
2. Row present but failed → look at the last response status. 2xx means delivered; 4xx means the merchant's
   endpoint rejected us (do not retry a 4xx forever); 5xx/timeout means retry per the backoff schedule.
3. Signature complaints → `t=<unix>,v1=<hex hmac>` over the **raw** body; a re-serialised JSON body breaks it.
4. SSRF guard rejected the URL → private-range resolution, non-HTTPS, or a redirect. Correct behaviour;
   tell the merchant.
5. Backlog rising → `webhook-backlog.md` runbook.

## 6. "A scheduled job never ran"

Check in this order: is the cron actually configured (plan limits! pitfall 9) → is the job paused/flagged off
→ did the previous run hold a lease that never released → is the job in the dead-letter queue → did it run but
log into a different environment's table.

## 7. "The PDF or email is wrong"

Template version (in-flight sends keep their original) → locale and font (Bangla shaping needs the embedded
font) → was it generated inline where it should be a worker job (pitfall 10) → is the watermark carrying the
right merchant/version → for email, SPF/DKIM/DMARC and the sending subdomain (pitfall 19).

## 8. "Users get signed out randomly"

1. Is `supabase-js` writing its own auth cookies next to our `__Host-` ones? (pitfall 25 — the most common)
2. `__Host-` requires `Secure` + `Path=/` + **no** `Domain`; one wrong attribute and the cookie silently
   vanishes in production only (pitfall 12).
3. Session rotation on privilege change — expected; check the audit log for the rotation event.
4. Device/fingerprint change triggering step-up — expected; check the replay guard, not the session code.
5. Two tabs racing a refresh — the token is single-use; the loser should refresh, not sign out.

## 9. "Works locally, breaks on Vercel"

Edge-runtime import of `postgres` (pitfall 6) → `prepare: false` missing under transaction pooling (pitfall 1)
→ `max` too high for the pooler → hardcoded URLs instead of env (pitfall 24) → server action body limit
(pitfall 8) → CSP blocking a third-party frame/script in production only (pitfall 13).

## 10. "The test passes locally, fails in CI"

Injected clock (`now()`) vs `Date.now()` → seeded factories vs `Math.random()` → ordering assumptions without
`order by` → shared database state between tests → timezone of the CI runner → a snapshot rendered with a
system font.

## Escalation

| Situation | Do |
|---|---|
| Symptom matches a row above | Follow it to the end before inventing a theory |
| Two fix attempts failed | Stop; write the two-strike report (command, output, attempts) |
| Symptom is new | Fix it, then **add a row here** and a pitfall to §11 if it is a class of bug, not a one-off |
| Money already moved wrongly | Freeze payouts first (`payouts_enabled=false`); correctness before diagnosis |
| Suspected breach or data leak | Runbook `suspected-breach.md`; do not "investigate quietly" |

## Keeping this file useful

`docs/TROUBLESHOOTING.md` is written to be appended to, not read once. Every non-trivial bug adds one row:
symptom → ordered checks → the fix that worked. An AI agent with a symptom and this ladder spends its tokens
on the fix instead of on rediscovering the architecture. A symptom that needed a whole afternoon belongs here
the same day.
