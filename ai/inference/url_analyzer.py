"""
Structural URL & Phishing Link Analyzer for AI ScamShield.
Evaluates URL structure, domain entropy, look-alike typosquatting,
punycode/homographs, and suspicious TLDs completely offline.
"""

import re
import math
from urllib.parse import urlparse
from typing import Dict, Any, List

# Legitimate Brand Names to protect against typosquatting
PROTECTED_BRANDS = [
    "sbi", "hdfc", "hdfcbank", "icici", "icicibank", "axisbank", "kotak", "pnb",
    "paypal", "amazon", "netflix", "google", "apple", "microsoft", "flipkart",
    "paytm", "phonepe", "swiggy", "zomato", "fedex", "bluedart", "dhl", "indiapost"
]

SUSPICIOUS_TLDS = {
    "xyz", "top", "click", "site", "cc", "pw", "me", "info", "online", "icu",
    "buzz", "club", "app", "work", "loan", "vip", "cfd", "rest", "fit"
}

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "cutt.ly", "is.gd", "rb.gy", "ow.ly", "goo.gl"
}

SENSITIVE_KEYWORDS = [
    "login", "signin", "verify", "verification", "kyc", "secure", "update",
    "banking", "account", "wallet", "recover", "password", "otp", "claim",
    "reward", "refund", "suspend", "unfreeze", "disconnection"
]

def calculate_entropy(text: str) -> float:
    """Calculates Shannon Entropy of a string to detect random generated domains."""
    if not text:
        return 0.0
    entropy = 0.0
    for x in set(text):
        p_x = float(text.count(x)) / len(text)
        entropy += - p_x * math.log(p_x, 2)
    return entropy

def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes minimum edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def analyze_url(url: str) -> Dict[str, Any]:
    """
    Performs comprehensive structural and heuristic risk analysis on a URL.
    Returns risk score (0-100), risk level, detected signals, attribution, and recommendation.
    """
    if not url or not url.strip():
        return {
            "risk_score": 0,
            "risk_level": "LOW",
            "status": "NO URL PROVIDED",
            "confidence": 1.0,
            "signals": [],
            "attribution": [],
            "recommendation": "Please enter a valid URL to analyze.",
            "is_offline": True,
            "url": ""
        }

    raw_url = url.strip()
    if not re.match(r"^https?://", raw_url, re.IGNORECASE):
        test_url = "http://" + raw_url
    else:
        test_url = raw_url

    parsed = urlparse(test_url)
    hostname = (parsed.hostname or "").lower()
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()

    signals = []
    factor_weights = {}
    base_risk = 5

    # 1. Check Protocol (HTTPS vs HTTP)
    is_https = raw_url.lower().startswith("https://")
    if not is_https:
        base_risk += 15
        signals.append("Insecure HTTP Protocol (Lacks SSL/TLS Encryption)")
        factor_weights["Protocol Security"] = 15

    # 2. Check for IP Address in Hostname (e.g. http://192.168.1.1/login)
    is_ip = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname))
    if is_ip:
        base_risk += 50
        signals.append("Direct IP Address Hostname (Bypasses Domain DNS Verification)")
        factor_weights["Domain Structure"] = factor_weights.get("Domain Structure", 0) + 40

    # 3. Check for Known URL Shortener
    if hostname in URL_SHORTENERS:
        base_risk += 25
        signals.append("URL Shortener Detected (Obfuscates Final Destination)")
        factor_weights["Obfuscation Tactics"] = factor_weights.get("Obfuscation Tactics", 0) + 25

    # 4. Check for Punycode / Homograph Attack
    if "xn--" in hostname:
        base_risk += 45
        signals.append("Punycode Internationalized Domain (Possible Homograph Impersonation)")
        factor_weights["Domain Impersonation"] = factor_weights.get("Domain Impersonation", 0) + 45

    # 5. Check Top-Level Domain (TLD)
    parts = hostname.split(".")
    tld = parts[-1] if len(parts) > 1 else ""
    if tld in SUSPICIOUS_TLDS:
        base_risk += 35
        signals.append(f"High-Risk Phishing TLD (.{tld})")
        factor_weights["Domain Structure"] = factor_weights.get("Domain Structure", 0) + 30

    # 6. Check Subdomain Stacking (e.g. sbi.co.in.verification-portal.xyz)
    if len(parts) > 3:
        base_risk += 20
        signals.append(f"Excessive Subdomain Stacking ({len(parts)-2} subdomains)")
        factor_weights["Domain Structure"] = factor_weights.get("Domain Structure", 0) + 20

    # 7. Check Domain Shannon Entropy
    domain_name = parts[-2] if len(parts) >= 2 else hostname
    entropy = calculate_entropy(domain_name)
    if len(domain_name) > 8 and entropy > 3.4:
        base_risk += 25
        signals.append(f"High Random Character Entropy in Domain ({entropy:.2f})")
        factor_weights["Algorithmic Generation"] = factor_weights.get("Algorithmic Generation", 0) + 25

    # 8. Check Look-alike Typosquatting against Protected Brands
    detected_brand_target = None
    for brand in PROTECTED_BRANDS:
        # Check if brand is in domain or subdomains
        if brand in hostname:
            # If hostname is not the exact official domain (e.g. sbi-kyc-update.xyz vs onlinesbi.sbi)
            official_allowed = [f"{brand}.com", f"{brand}.co.in", f"{brand}.org", f"{brand}.net", f"onlinesbi.sbi"]
            if not any(hostname == off or hostname.endswith("." + off) for off in official_allowed):
                base_risk += 45
                detected_brand_target = brand.upper()
                signals.append(f"Potential Brand Impersonation Targeting {brand.upper()}")
                factor_weights["Brand Impersonation"] = factor_weights.get("Brand Impersonation", 0) + 45
                break
        else:
            # Levenshtein distance check (e.g. paypa1 vs paypal)
            dist = levenshtein_distance(domain_name, brand)
            if dist == 1 and len(brand) >= 4:
                base_risk += 50
                detected_brand_target = brand.upper()
                signals.append(f"Typosquatting Look-Alike Domain (Targeting {brand.upper()})")
                factor_weights["Brand Impersonation"] = factor_weights.get("Brand Impersonation", 0) + 50
                break

    # 9. Sensitive Phishing Keywords in Path or Query
    matched_keywords = [kw for kw in SENSITIVE_KEYWORDS if kw in path or kw in query]
    if matched_keywords:
        weight = min(30, len(matched_keywords) * 12)
        base_risk += weight
        signals.append(f"Deceptive Security Keywords in URL Path: {', '.join(matched_keywords[:3])}")
        factor_weights["Credential Solicitation"] = factor_weights.get("Credential Solicitation", 0) + weight

    # 10. Direct Executable Download (.apk, .exe, .scr)
    if re.search(r"\.(apk|exe|scr|bat|vbs|msi)$", path, re.IGNORECASE):
        base_risk += 55
        signals.append("Direct Executable / APK Package Download Detected")
        factor_weights["Malicious File Payload"] = factor_weights.get("Malicious File Payload", 0) + 55

    # Final Risk Score Normalization (0-100)
    final_score = int(round(min(100, max(5, base_risk))))

    # Map to Risk Level
    if final_score <= 25:
        risk_level = "LOW"
        status = "LOW OBSERVED RISK"
        recommendation = "Low structural risk observed. Standard browsing caution still applies."
    elif final_score <= 50:
        risk_level = "MODERATE"
        status = "CAUTION ADVISED"
        recommendation = "Verify the domain carefully. Do not enter credentials on unfamiliar websites."
    elif final_score <= 75:
        risk_level = "HIGH"
        status = "POTENTIALLY SUSPICIOUS"
        recommendation = "High risk indicators found. Do not enter passwords, OTPs, or make payments."
    else:
        risk_level = "CRITICAL"
        status = "CRITICAL PHISHING RISK"
        recommendation = "Severe phishing / fake domain indicators detected! Do not open this link or install downloads."

    # Build Attribution Breakdown summing to 100%
    attributions = []
    if final_score <= 25:
        attributions = [
            {"factor": "Standard Domain Architecture", "percentage": 80, "description": "Conventional domain structure with legitimate characteristics."},
            {"factor": "Absence of Obfuscation", "percentage": 20, "description": "No hidden redirects, punycode, or look-alike spelling."}
        ]
    else:
        total_w = sum(factor_weights.values()) or 1
        accum = 0
        items = sorted(factor_weights.items(), key=lambda x: x[1], reverse=True)
        for i, (k, v) in enumerate(items):
            if i == len(items) - 1:
                pct = max(1, 100 - accum)
            else:
                pct = int(round((v / total_w) * 100))
                accum += pct
            attributions.append({
                "factor": k,
                "percentage": pct,
                "description": f"Contributes {pct}% to the overall URL risk calculation."
            })

    return {
        "url": raw_url,
        "hostname": hostname,
        "risk_score": final_score,
        "risk_level": risk_level,
        "status": status,
        "confidence": 0.94 if signals else 0.85,
        "signals": signals,
        "attribution": attributions,
        "recommendation": recommendation,
        "is_offline": True,
        "is_https": is_https,
        "impersonated_brand": detected_brand_target
    }
