# CropPulse Commerce Mobile Authentication

The commerce service uses persistent, provider-backed Indian mobile OTP authentication. It does not contain a universal OTP, return verification codes in API responses, or fall back to an in-memory production flow.

## API entrypoint

Run the isolated commerce API from the repository root:

```bash
uvicorn phase2_backend.commerce.api:app --reload
```

Versioned authentication routes:

```text
GET  /api/commerce/v1/auth/readiness
POST /api/commerce/v1/auth/otp/request
POST /api/commerce/v1/auth/otp/verify
POST /api/commerce/v1/auth/refresh
POST /api/commerce/v1/auth/logout
GET  /api/commerce/v1/auth/me
```

Interactive documentation is available at `/api/commerce/v1/docs` in an explicitly permitted development environment.

## Required secrets

Configure these values in the deployment provider's secret store:

```text
COMMERCE_JWT_SECRET=<unique random value of at least 32 characters>
COMMERCE_OTP_HASH_SECRET=<different random value of at least 32 characters>
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_VERIFY_SERVICE_SID=VA...
```

The service rejects missing, short, placeholder, reused, or unsupported JWT configuration. No secret belongs in source control, mobile builds, logs, screenshots, or support messages.

Optional controls are documented in the repository `.env.example`, including access/refresh lifetimes, OTP expiry, resend cooldown, request-rate windows, and verification-attempt limits.

## Security behavior

- Indian mobile numbers are normalized to E.164 before use.
- Request-rate identifiers are stored as HMAC-SHA256 values rather than plaintext IP addresses or duplicate plaintext phone fields.
- The Twilio Verify service generates, sends, and checks OTP codes.
- Challenges expire, enforce attempt limits, and can be consumed only once.
- Request responses are account-enumeration safe and never contain the OTP.
- Access tokens are short-lived signed JWTs with user, session, type, expiry, issued-at, and unique-token claims.
- Refresh tokens are opaque random values; only SHA-256 hashes are stored.
- Refreshing rotates the refresh token, and a rotated token cannot be reused.
- Logout revokes the server session, immediately invalidating related access tokens.
- A blocked/deleted customer cannot create or continue a session.
- Missing provider or secret configuration returns a fail-closed readiness or `503` response.

## Example flow

Request a code:

```json
POST /api/commerce/v1/auth/otp/request
{"phone":"9876543210"}
```

The response returns a masked phone number and a `challenge_id`. Submit that identifier with the code received by SMS:

```json
POST /api/commerce/v1/auth/otp/verify
{
  "challenge_id":"<uuid>",
  "phone":"9876543210",
  "code":"<received code>"
}
```

Successful verification returns a short-lived access token and a rotating refresh token. The mobile app must store them in Android secure storage; it must not use plain shared preferences.

## Migration

Migration `20260813_0002` adds `commerce_otp_challenges`. Hosted PostgreSQL application is intentionally deferred, so this code is locally complete but not externally activated.

```bash
alembic -c phase2_backend/alembic.ini upgrade head
```

## Verification

```bash
python -m pytest phase2_backend/test_commerce_auth.py phase2_backend/test_commerce_database.py -q
```

The tests use an injected recording provider and isolated SQLite database. The recording provider exists only in test code and is never selectable by runtime environment variables.

## External activation still required

- Create/review a Twilio Verify service and approved Indian SMS sender configuration.
- Store real secrets in the chosen deployment provider.
- Apply migrations to the chosen hosted PostgreSQL database.
- Restrict allowed origins and network access for the production API.
- Verify SMS delivery, throttling, expiry, retry, provider outage, and abuse behavior in a non-production account.
- Complete privacy/retention review for phone and authentication records.
- Integrate the Flutter app with secure token storage and the new API contract.
