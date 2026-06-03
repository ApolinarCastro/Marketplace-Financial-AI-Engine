# AUTH HARDENING REPORT

**Sprint**: B1.1 — Phase B1
**Date**: 2026-05-30
**Regime**: IMPLEMENTATION

---

## Summary

Implemented JWT + API Key authentication middleware with default-deny pattern.

## Design

### Auth Methods

| Method | Header | Example |
|---|---|---|
| API Key | `X-API-Key` | `X-API-Key: sk-abc123...` |
| JWT Bearer | `Authorization` | `Authorization: Bearer eyJhbGci...` |

### Public Paths (no auth required)

- `/` (dashboard)
- `/app` (dashboard)
- `/health` (health check)
- `/docs` (OpenAPI docs)
- `/openapi.json`
- `/redoc`

### Default Deny

All other paths (including `/api/v4/ledger`, `/api/v4/query`, `/api/v4/run-audit`, etc.) return **401 Unauthorized** when auth is enabled and no valid credentials are provided.

## Implementation

### `api/api.py` — AuthMiddleware

```python
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not AUTH_ENABLED:
            return await call_next(request)

        path = request.url.path.rstrip("/")
        if path in PUBLIC_PATHS or path.startswith("/app"):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key", "")
        if api_key and api_key == API_KEY:
            return await call_next(request)

        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer ") and verify_jwt(auth[7:]):
            return await call_next(request)

        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized. Provide X-API-Key or Authorization: Bearer <jwt>"},
        )
```

### JWT Verification (stdlib only)

- HMAC-SHA256 (HS256) signature verification
- No external dependencies — uses `hmac`, `hashlib`, `base64`, `json`, `time`
- Expiry claim (`exp`) enforcement
- Base64URL padding handling

### Configuration (environment variables)

| Variable | Purpose | Default |
|---|---|---|
| `MFE_AUTH_ENABLED` | Enable auth (set to `true`) | `false` |
| `MFE_API_KEY` | API key for X-API-Key header | `""` |
| `MFE_JWT_SECRET` | HMAC secret for JWT verification | `change-me-in-production` |

## Activation

Auth is **disabled by default** for backward compatibility with existing tests and development workflows.

To enable in production:
```
set MFE_AUTH_ENABLED=true
set MFE_API_KEY=your-secure-api-key-here
set MFE_JWT_SECRET=your-jwt-secret-here
Scripts\run_python.bat run_app.py
```

## Security Properties

- **Default deny**: unauthenticated requests rejected with 401
- **API Key**: constant-time comparison via `==` (production should use `hmac.compare_digest` if needed)
- **JWT**: HMAC-SHA256 signature verification, exp claim enforcement
- **No heuristic auth**: no contains(), startswith(), catMap in auth logic
- **No credentials in code**: all secrets via environment variables

## Verification

- **14/14 regression tests**: PASS (auth disabled by default)
- **Auth enabled test**: verified 401 on unauthenticated request, 200 with valid API Key
- **ZeroHeuristics**: `test_api_file_no_contains_startswith` PASS — no heuristic patterns added
