"""Shared URL validation utilities with SSRF protection.

Used by fetch_page.py, analyze_landing.py, capture_screenshot.py, and
generate_image.py to validate user-supplied URLs before making HTTP requests
or launching browsers, and to sanitize exception messages before surfacing
them to the user.
"""

import ipaddress
import os
import re
import socket
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# Sensitive substrings to redact from any error message before logging or
# returning to the caller. Catches common credential parameter names (api_key,
# apikey, access_token, refresh_token, auth, key, token, secret, password,
# OAuth `code=`, AWS `signature=`) and bare `Bearer <token>` headers
# regardless of case.
_SENSITIVE_PATTERN = re.compile(
    r'\b(api[_-]?key|access[_-]?token|refresh[_-]?token|authorization|auth|key|token|secret|password|code|signature)'
    r'\s*[=:]\s*[\"\']?(?:Bearer\s+)?[^\s&,;\"\']+|\bBearer\s+[^\s,;]+',
    re.IGNORECASE,
)

_TOKEN_PATTERN = re.compile(
    r"\b(?:sk[_-](?:live[_-])?|gh[pousr]_|AIza)[A-Za-z0-9._-]{8,}\b",
    re.IGNORECASE,
)

_PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.DOTALL,
)

_SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "proxy-authorization",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
}


def _redact_sensitive(text: str) -> str:
    """Run the credential-redaction regex over arbitrary text."""
    text = _PRIVATE_KEY_PATTERN.sub("[REDACTED PRIVATE KEY]", text)
    text = _SENSITIVE_PATTERN.sub(
        lambda m: (
            "authorization=Bearer ***"
            if m.group(1) and m.group(1).lower() == "authorization" and "bearer" in m.group(0).lower()
            else (m.group(1).lower().replace('-', '_') + '=***')
            if m.group(1)
            else 'Bearer ***'
        ),
        text,
    )
    return _TOKEN_PATTERN.sub("***", text)


def redact_sensitive_text(value: Any) -> str:
    """Return a log-safe string with common credentials removed."""
    return _redact_sensitive(str(value))


def sanitize_error(err: Exception) -> str:
    """Strip potential API keys / tokens / passwords from an exception message.

    Use whenever an exception's str() reaches stdout, JSON output, or a user-
    facing error field. The redaction is irreversible — the goal is to make
    the message safe to log, not to preserve the original details.

    Args:
        err: The exception to format.

    Returns:
        The exception string with sensitive substrings replaced.
    """
    return redact_sensitive_text(err)


def sanitize_headers(headers: Any) -> dict[str, str]:
    """Return response/request headers with credential-bearing values removed."""
    sanitized: dict[str, str] = {}
    for name, value in dict(headers or {}).items():
        key = str(name)
        if key.lower() in _SENSITIVE_HEADERS:
            sanitized[key] = "***"
        else:
            sanitized[key] = redact_sensitive_text(value)
    return sanitized


def sanitize_url(url: str) -> str:
    """Strip credentials from a URL string before logging it to stderr or stdout.

    Covers tokens embedded in query parameters (`?access_token=...&code=...`)
    and userinfo (`https://user:password@host/`). The output is meant to be
    safe to surface in CLI output, logs, or transcripts — not round-trippable.

    Args:
        url: The URL to sanitize.

    Returns:
        URL with credential-bearing values replaced by `***`.
    """
    # Drop userinfo segment if present (https://user:pass@host -> https://host)
    parsed = urlparse(url)
    if parsed.username or parsed.password:
        netloc = parsed.hostname or ''
        try:
            if parsed.port:
                netloc = f"{netloc}:{parsed.port}"
        except ValueError:
            # The URL will be rejected by validate_url; redaction must still
            # be fail-safe and never expose userinfo while formatting errors.
            pass
        url = parsed._replace(netloc=netloc).geturl()
    # Redact sensitive query/fragment parameters and token-looking values.
    return _redact_sensitive(url)

_MAX_URL_LENGTH = 8192
_LOCAL_HOSTNAMES = {"localhost", "localhost.localdomain", "metadata", "metadata.google.internal"}


def validate_url(url: str) -> str:
    """Validate URL scheme and block private/internal IPs (SSRF protection).

    Args:
        url: The URL to validate. If no scheme, https:// is prepended.

    Returns:
        The validated URL string (with scheme).

    Raises:
        ValueError: If URL has invalid scheme, no hostname, resolves to
                    a blocked IP, or DNS resolution fails.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")
    url = url.strip()
    if not url or len(url) > _MAX_URL_LENGTH:
        raise ValueError("URL is empty or too long.")
    if any(ord(char) < 32 for char in url) or "\\" in url:
        raise ValueError("URL contains forbidden control characters or backslashes.")

    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Only http/https allowed.")
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL has no hostname.")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("Credentials in URLs are not allowed.")
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError("URL has an invalid port.") from exc

    normalized_hostname = hostname.rstrip(".").lower()
    if normalized_hostname in _LOCAL_HOSTNAMES or normalized_hostname.endswith(".localhost"):
        raise ValueError("URL targets a local/internal hostname.")
    try:
        resolved = socket.getaddrinfo(normalized_hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        if not resolved:
            raise ValueError(f"DNS resolution returned no addresses for {normalized_hostname}")
        for _, _, _, _, addr in resolved:
            ip = ipaddress.ip_address(addr[0])
            # is_global rejects loopback, private, link-local, multicast,
            # documentation, benchmark, CGNAT, unspecified, and reserved space.
            if not ip.is_global or ip.is_multicast or ip.is_reserved:
                raise ValueError(f"URL resolves to blocked non-public IP: {ip}")
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {normalized_hostname}: {exc}") from exc
    return url


def guarded_request(session: Any, method: str, url: str, **kwargs: Any) -> Any:
    """Validate an outbound URL immediately before a Requests dispatch.

    Automatic redirects are disabled because every redirect target must return
    to this boundary for a fresh validation. Callers that support redirects
    must implement a bounded manual loop.
    """
    validated = validate_url(url)
    if kwargs.get("allow_redirects") is True:
        raise ValueError("Automatic redirects are forbidden for guarded requests.")
    kwargs["allow_redirects"] = False
    dispatcher = getattr(session, method.lower(), None)
    if dispatcher is None:
        raise ValueError(f"Unsupported HTTP method: {method}")
    return dispatcher(validated, **kwargs)


def install_playwright_ssrf_guard(context: Any) -> list[dict[str, str]]:
    """Screen every Playwright request before dispatch.

    Context-level routing covers the main frame, redirects, child frames, and
    subresources. Callers must create the context with service workers blocked,
    because service-worker initiated requests can bypass Playwright routing.
    The returned list records sanitized blocked requests for user-facing errors.
    """
    blocked: list[dict[str, str]] = []

    def guard(route: Any, request: Any = None) -> None:
        outbound = request or route.request
        try:
            validate_url(outbound.url)
        except (TypeError, ValueError) as exc:
            blocked.append({"url": sanitize_url(str(outbound.url)), "error": sanitize_error(exc)})
            route.abort("blockedbyclient")
            return
        route.continue_()

    context.route("**/*", guard)
    return blocked


def create_guarded_browser_context(browser: Any, **kwargs: Any) -> tuple[Any, list[dict[str, str]]]:
    """Create a Playwright context with service workers and downloads disabled."""
    kwargs.setdefault("service_workers", "block")
    kwargs.setdefault("accept_downloads", False)
    context = browser.new_context(**kwargs)
    return context, install_playwright_ssrf_guard(context)


def output_root(root: str | os.PathLike[str] | None = None) -> Path:
    """Resolve the only directory in which generated artifacts may be written."""
    configured = root or os.environ.get("CLAUDE_ADS_OUTPUT_ROOT") or os.getcwd()
    return Path(configured).expanduser().resolve()


def resolve_output_path(
    path: str | os.PathLike[str],
    *,
    root: str | os.PathLike[str] | None = None,
    create_parent: bool = False,
) -> Path:
    """Resolve an output path and reject traversal or symlink escapes.

    Relative paths are anchored to ``CLAUDE_ADS_OUTPUT_ROOT`` (or the current
    directory). Absolute paths are accepted only when they remain inside that
    root. Existing symlinks are resolved before the containment check.
    """
    base = output_root(root)
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = base / candidate
    candidate = candidate.resolve(strict=False)
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"Output path escapes configured root: {candidate}") from exc
    if create_parent:
        candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate
