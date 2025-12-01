Security Measures Documentation for LibraryProject

1. Django Settings Security

- DEBUG = False: Ensures detailed error messages are not shown in production.
- ALLOWED_HOSTS: Restricts which domains can serve the app.
- SECURE_BROWSER_XSS_FILTER: Enables browser XSS filter.
- SECURE_CONTENT_TYPE_NOSNIFF: Prevents browser from MIME-sniffing.
- X_FRAME_OPTIONS = 'DENY': Prevents clickjacking by denying iframe embedding.
- CSRF_COOKIE_SECURE & SESSION_COOKIE_SECURE: Ensures cookies are sent over HTTPS only.

