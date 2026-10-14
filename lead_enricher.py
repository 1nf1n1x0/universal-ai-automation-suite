"""
Lead Enricher & Verification Engine
Part of the Universal AI Agent Automation Suite.
Compliant, ethical, zero-scraping violations, high-precision validation.
"""

import re
import json
import socket
from typing import Dict, Any, List

class LeadEnricher:
    def __init__(self):
        self.disposable_domains = {
            "mailinator.com", "tempmail.com", "10minutemail.com", 
            "guerrillamail.com", "trashmail.com", "yopmail.com"
        }

    def validate_email_syntax(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))

    def is_disposable(self, domain: str) -> bool:
        return domain.lower() in self.disposable_domains

    def enrich_contact(self, raw_lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrichit et attribue un score de qualité à un lead B2B.
        """
        email = raw_lead.get("email", "").strip()
        name = raw_lead.get("name", "").strip()
        company = raw_lead.get("company", "").strip()
        website = raw_lead.get("website", "").strip()

        is_valid_syntax = self.validate_email_syntax(email)
        domain = email.split("@")[-1] if is_valid_syntax else ""
        disposable = self.is_disposable(domain) if domain else True

        # Calcul du Lead Quality Score (0 à 100)
        score = 0
        if is_valid_syntax:
            score += 30
        if not disposable:
            score += 25
        if name:
            score += 15
        if company:
            score += 15
        if website:
            score += 15

        tier = "Tier 1 (High Intent)" if score >= 80 else ("Tier 2 (Qualified)" if score >= 50 else "Tier 3 (Low/Unverified)")

        return {
            "name": name,
            "company": company,
            "email": email,
            "domain": domain,
            "syntax_valid": is_valid_syntax,
            "is_disposable": disposable,
            "quality_score": score,
            "tier": tier,
            "verified": is_valid_syntax and not disposable
        }

if __name__ == "__main__":
    enricher = LeadEnricher()
    test_leads = [
        {"name": "Karim Benzema", "company": "Tech Solutions", "email": "karim@techsolutions.com", "website": "techsolutions.com"},
        {"name": "Spam User", "company": "None", "email": "fake@mailinator.com", "website": ""},
        {"name": "Sarah Connor", "company": "Cyberdyne Systems", "email": "s.connor@cyberdyne.io", "website": "cyberdyne.io"}
    ]
    results = [enricher.enrich_contact(l) for l in test_leads]
    print(json.dumps(results, indent=2))
