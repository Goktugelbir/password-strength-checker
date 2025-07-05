import re

class PasswordChecker:
    def __init__(self, common_passwords=None):
        self.common_passwords = common_passwords or []

    def analyze_password(self, password):
        score = 0
        criteria_met = {
            "length": len(password) >= 8,
            "uppercase": bool(re.search(r"[A-Z]", password)),
            "lowercase": bool(re.search(r"[a-z]", password)),
            "numbers": bool(re.search(r"\d", password)),
            "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
            "no_common": password.lower() not in self.common_passwords,
            "no_patterns": not re.search(r"(1234|abcd|qwerty|1111)", password.lower())
        }

        score += sum(criteria_met.values()) * 10
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10

        if not criteria_met["no_common"]:
            score -= 20
        if not criteria_met["no_patterns"]:
            score -= 10

        strength = "Very Weak"
        if score >= 80:
            strength = "Very Strong"
        elif score >= 65:
            strength = "Strong"
        elif score >= 50:
            strength = "Medium"
        elif score >= 35:
            strength = "Weak"

        suggestions = []
        if not criteria_met["length"]:
            suggestions.append("Use at least 8 characters.")
        if not criteria_met["uppercase"]:
            suggestions.append("Add uppercase letters.")
        if not criteria_met["lowercase"]:
            suggestions.append("Add lowercase letters.")
        if not criteria_met["numbers"]:
            suggestions.append("Include numbers.")
        if not criteria_met["special"]:
            suggestions.append("Include special characters.")
        if not criteria_met["no_common"]:
            suggestions.append("Avoid common passwords.")
        if not criteria_met["no_patterns"]:
            suggestions.append("Avoid obvious patterns.")

        warnings = []
        if password.lower() in self.common_passwords:
            warnings.append("Your password is too common!")
        if re.match(r".{1,6}$", password):
            warnings.append("Your password is very short.")

        return {
            "score": min(max(score, 0), 100),
            "strength": strength,
            "criteria_met": criteria_met,
            "suggestions": suggestions,
            "warnings": warnings
        }
