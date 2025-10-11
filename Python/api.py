# insecure_test_canary.py
# SAFETY NOTICE:
# - This file contains ONLY DUMMY / PLACEHOLDER secrets and insecure patterns for LOCAL TESTING.
# - DO NOT use any of these patterns in production code.
# - DO NOT push to public repositories. Use a private test repo or run locally.

# 1) Hardcoded API key (placeholder)
# Intentionally obvious pattern: api_key, token, secret assigned directly.
API_KEY = "DUMMY_API_KEY_abcdefghijklmnopqrstuvwxyz123456"  # fake key for scanner testing

# 2) AWS-like fake key (pattern scanners often look for this form)
AWS_ACCESS_KEY_ID = "AKIAAAAAAAAAAAAAAAAAA"  # NOT real — for detection only
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # fake

# 3) PEM-like private key block (fake placeholder)
FAKE_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQEA7dUm8EXAMPLEfA1kYQq7L0w5uN+fakeplaceholderdataQ==
-----END RSA PRIVATE KEY-----"""

# 4) Insecure HTTP usage example (plaintext transport)
import requests  # included to illustrate insecure pattern; no external request is made
INSECURE_URL = "http://example-insecure.test/api"  # scanner pattern: http URI

def fetch_insecure():
    # This is intentionally not executed by default; it's a demonstration pattern only.
    # DO NOT use this in production — use HTTPS and verify SSL/TLS.
    try:
        # Note: we do not actually call requests.get here to avoid network behavior in tests.
        return f"Would fetch from {INSECURE_URL} with API_KEY={API_KEY[:8]}..."
    except Exception:
        return "fetch failed (demo)"

# 5) SQL construction via string interpolation (SQL injection pattern)
def build_query(user_input: str) -> str:
    # BAD practice: direct string formatting of user input into SQL
    # This is here to trigger static analysis rules looking for SQL injection patterns.
    query = "SELECT * FROM users WHERE username = '%s';" % user_input
    return query

# 6) eval usage demonstration (dangerous if used with untrusted input)
def dangerous_eval(expr: str):
    # WARNING: DO NOT use eval on untrusted input in real code.
    # This function exists to demonstrate scanning rules that detect eval/exec usage.
    try:
        # We intentionally avoid actually executing eval on arbitrary input during tests.
        return f"Would eval: {expr}"
    except Exception:
        return "eval failed (demo)"

# 7) Credentials in a simulated .env style string
DOTENV_SIM = """
# .env style - placeholder secrets below
SECRET_KEY="super-secret-placeholder-1234567890"
DATABASE_URL="postgres://user:password@localhost:5432/dbname"
"""

# Quick self-test printing (keeps output safe and non-sensitive)
if __name__ == "__main__":
    print("INSECURE TEST CANARY: This file contains ONLY FAKE placeholders for testing.")
    print("Examples present:")
    print("- hardcoded API_KEY (placeholder):", API_KEY[:12] + "...")
    print("- AWS-like placeholders (do not use):", AWS_ACCESS_KEY_ID)
    print("- PEM-like block length:", len(FAKE_PRIVATE_KEY))
    print("- Insecure URL example:", INSECURE_URL)
    print("- Example unsafe SQL query:", build_query("alice OR 1=1"))
    print("Remove this file from repos when you're done testing.")

