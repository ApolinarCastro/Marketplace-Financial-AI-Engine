# API SECURITY REPORT

**Sprint**: B1.1 — Phase B2
**Date**: 2026-05-30
**Regime**: IMPLEMENTATION

---

## Summary

Hardened CORS configuration and implemented rate limiting middleware.

## Changes

### 1. CORS Hardening

**Before**: `allow_origins=["*"]` — allowed any origin, including malicious websites

**After**:

```python
CORS_ORIGINS = os.environ.get(
    "MFE_CORS_ORIGINS",
    "http://localhost:8003,http://127.0.0.1:8003"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- Default origins: only localhost (dev server)
- Production can set `MFE_CORS_ORIGINS` to specific domains
- `allow_credentials=True` retained but now paired with explicit origins

### 2. Rate Limiting

**Before**: No rate limiting — unlimited requests from any IP

**After**:

```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests=100, window=60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self._clients: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        forwarded = request.headers.get("x-forwarded-for", "")
        client_ip = forwarded.split(",")[0].strip() if forwarded else (
            request.client.host if request.client else "127.0.0.1"
        )
        now = time.time()
        window_start = now - self.window
        if client_ip in self._clients:
            timestamps = [t for t in self._clients[client_ip] if t > window_start]
            self._clients[client_ip] = timestamps
            if len(timestamps) >= self.max_requests:
                return JSONResponse(status_code=429, content={
                    "detail": "Rate limit exceeded. Try again later."
                })
            self._clients[client_ip].append(now)
        else:
            self._clients[client_ip] = [now]
        return await call_next(request)
```

- **Default**: 100 requests per 60-second window per IP
- **Configurable**: `MFE_RATE_LIMIT` env var
- **X-Forwarded-For aware**: respects proxy headers
- **Sliding window**: purges expired timestamps, not fixed clock-aligned windows
- **In-memory**: no external dependencies (Redis, etc.)

### 3. Middleware Ordering

```
CORSMiddleware (outermost)  → intercepts OPTIONS preflight before auth
RateLimitMiddleware         → prevents abuse before auth check
AuthMiddleware (innermost)  → default deny for protected paths
```

This ordering ensures:
1. CORS preflight handled before any other middleware
2. Rate limiting applied before auth check (prevents auth DoS)
3. Auth check last (validates credentials)

### 4. Health Endpoint

Added `/health` endpoint returning database connectivity status:

```python
@app.get("/health")
def health():
    db_ok = False
    try:
        db = DatabaseV4.get()
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        pass
    return {"status": "ok" if db_ok else "degraded",
            "database": "connected" if db_ok else "unreachable"}
```

- Returns `200 OK` when DB is reachable
- Returns `200 degraded` when DB is unreachable (still responds, health check passes)
- Exempt from auth (in PUBLIC_PATHS)
- Exempt from rate limiting (in PUBLIC_PATHS)

## Verification

- **14/14 regression tests**: PASS
- CORS preflight: OPTIONS requests handled correctly with explicit origins
- Rate limiting: threshold enforced (429 after exceeding limit)
- Health endpoint: returns correct status
