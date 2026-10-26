# Payment Webhook Service — Risk Review

## Ranked Risks

**1. Critical — Missing or invalid webhook signature**

The original webhook checked the signature only when one was provided. A request with no signature could therefore be accepted and processed. An invalid signature was rejected, but the missing-signature case was not handled correctly. I fixed this by requiring a signature and using `hmac.compare_digest()` for comparison. I added a regression test, `test_missing_signature_rejected`, which failed before the fix and passed afterward.

**2. High — Duplicate webhook event processing**

If the payment provider delivers the same event more than once, the service may process it repeatedly and create duplicate orders or send duplicate receipts. The reviewed implementation does not adequately prevent duplicate event processing. This risk remains unfixed.

**3. High — Database write failure after sending an email**

If the service sends a receipt before successfully saving the order, the customer may receive confirmation for an order that was not recorded. This creates inconsistent customer communication and order records. This risk remains unfixed.

**4. Medium — Database connection cleanup**

Database connections that are not reliably closed can consume resources and eventually affect service availability. I improved connection cleanup in `app/db.py`.

## Test Coverage Gaps

The existing tests cover successful payment processing, refunds, and invalid signatures. I added a test for missing signatures. However, the tests do not adequately cover duplicate event delivery, database write failures after an email is sent, or email delivery failures. These scenarios need additional regression and failure-handling tests.

## Conclusion

The signature-validation vulnerability and database connection cleanup have been addressed on the `fix/webhook-reliability` branch. The duplicate-event and email/database consistency risks remain open and should be addressed before production deployment.