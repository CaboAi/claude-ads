#!/usr/bin/env python3
"""
Capture screenshots of ad landing pages for creative audit.

Usage:
    python capture_screenshot.py https://example.com/landing
    python capture_screenshot.py https://example.com/landing --mobile
    python capture_screenshot.py https://example.com/landing --all
"""

import argparse
import sys
from urllib.parse import urlparse

from url_utils import (
    create_guarded_browser_context,
    resolve_output_path,
    sanitize_error,
    sanitize_url,
    validate_url,
)

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright required. Install with: pip install -r requirements.txt && playwright install chromium")
    sys.exit(1)


VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
}


def capture_screenshot(
    url: str,
    output_path: str,
    viewport: str = "desktop",
    full_page: bool = False,
    timeout: int = 30000,
) -> dict:
    """
    Capture a screenshot of an ad landing page.

    Returns:
        Dictionary with url, output, viewport, success, error
    """
    result = {
        "url": sanitize_url(url),
        "output": str(output_path),
        "viewport": viewport,
        "success": False,
        "error": None,
    }

    if viewport not in VIEWPORTS:
        result["error"] = f"Invalid viewport: {viewport}. Choose from: {list(VIEWPORTS.keys())}"
        return result

    vp = VIEWPORTS[viewport]

    try:
        url = validate_url(url)
        output_path = resolve_output_path(output_path, create_parent=True)
    except ValueError as e:
        result["error"] = sanitize_error(e)
        return result

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context, blocked_requests = create_guarded_browser_context(
                browser,
                viewport={"width": vp["width"], "height": vp["height"]},
                device_scale_factor=2 if viewport == "mobile" else 1,
            )
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout)
            # Playwright follows redirects silently. Re-validate the final URL
            # against the SSRF blocklist (initial URL was already checked).
            validate_url(page.url)
            page.wait_for_timeout(1000)
            if blocked_requests:
                blocked = blocked_requests[0]
                raise ValueError(f"Blocked browser request to {blocked['url']}: {blocked['error']}")
            page.screenshot(path=str(output_path), full_page=full_page)
            result["output"] = str(output_path)
            result["success"] = True
            browser.close()

    except PlaywrightTimeout:
        result["error"] = f"Page load timed out after {timeout}ms"
    except Exception as e:
        result["error"] = sanitize_error(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Capture ad landing page screenshots")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("--output", "-o", default="screenshots", help="Output directory")
    parser.add_argument("--viewport", "-v", default="desktop", choices=VIEWPORTS.keys())
    parser.add_argument("--all", "-a", action="store_true", help="Capture all viewports")
    parser.add_argument("--full", "-f", action="store_true", help="Capture full page")
    parser.add_argument("--timeout", "-t", type=int, default=30000, help="Timeout in ms")

    args = parser.parse_args()

    try:
        output_dir = resolve_output_path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    except ValueError as exc:
        print(f"Error: {sanitize_error(exc)}", file=sys.stderr)
        sys.exit(1)

    parsed = urlparse(args.url)
    base_name = (parsed.hostname or "landing-page").replace(".", "_")

    viewports = VIEWPORTS.keys() if args.all else [args.viewport]

    for viewport in viewports:
        filename = f"{base_name}_{viewport}.png"
        output_path = output_dir / filename

        print(f"Capturing {viewport} screenshot...")
        result = capture_screenshot(
            args.url,
            output_path,
            viewport=viewport,
            full_page=args.full,
            timeout=args.timeout,
        )

        if result["success"]:
            print(f"  Saved to {output_path}")
        else:
            print(f"  Failed: {result['error']}")


if __name__ == "__main__":
    main()
