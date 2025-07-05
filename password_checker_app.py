import streamlit as st
import re
from password_checker import PasswordChecker
from common_passwords import COMMON_PASSWORDS

def main():
    st.set_page_config(
        page_title="Password Strength Checker",
        page_icon="🔒",
        layout="wide"
    )

    st.title("🔒 Password Strength Checker")
    st.markdown("**Check your password strength and get personalized improvement suggestions**")

    checker = PasswordChecker(COMMON_PASSWORDS)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Enter Your Password")
        password = st.text_input("Password:", type="password")

        show_password = st.checkbox("Show password")
        if show_password and password:
            st.text(f"Your password: {password}")

        if password:
            result = checker.analyze_password(password)
            st.subheader("Password Strength")

            strength_colors = {
                "Very Weak": "🔴",
                "Weak": "🟠", 
                "Medium": "🟡",
                "Strong": "🟢",
                "Very Strong": "🟢"
            }

            strength_text = f"{strength_colors[result['strength']]} **{result['strength']}**"
            st.markdown(strength_text)

            strength_values = {
                "Very Weak": 0.2,
                "Weak": 0.4,
                "Medium": 0.6,
                "Strong": 0.8,
                "Very Strong": 1.0
            }
            st.progress(strength_values[result['strength']])
            st.metric("Security Score", f"{result['score']}/100")

            st.subheader("Detailed Analysis")
            criteria_met = result['criteria_met']
            st.markdown("**Requirements Met:**")

            criteria_display = [
                ("✅" if criteria_met['length'] else "❌", "At least 8 characters"),
                ("✅" if criteria_met['uppercase'] else "❌", "Contains uppercase letters"),
                ("✅" if criteria_met['lowercase'] else "❌", "Contains lowercase letters"),
                ("✅" if criteria_met['numbers'] else "❌", "Contains numbers"),
                ("✅" if criteria_met['special'] else "❌", "Contains special characters"),
                ("✅" if criteria_met['no_common'] else "❌", "Not a common password"),
                ("✅" if criteria_met['no_patterns'] else "❌", "No obvious patterns")
            ]
            for icon, description in criteria_display:
                st.markdown(f"{icon} {description}")

            if result['suggestions']:
                st.subheader("💡 Improvement Suggestions")
                for suggestion in result['suggestions']:
                    st.markdown(f"• {suggestion}")

            if result['warnings']:
                st.subheader("⚠️ Security Warnings")
                for warning in result['warnings']:
                    st.warning(warning)

    with col2:
        st.subheader("🛡️ Password Security Tips")
        tips = [
            "Length Matters: Longer passwords are harder to crack.",
            "Mix Characters: Use uppercase, lowercase, numbers, and symbols.",
            "Avoid Personal Info: No names or birthdays.",
            "Use Unique Passwords: Don't reuse across accounts.",
            "Avoid Common Patterns: Like '123456' or 'qwerty'.",
            "Use Passphrases: Memorable and complex phrases.",
            "Enable Two-Factor Authentication (2FA)."
        ]
        for tip in tips:
            st.markdown(f"- {tip}")

if __name__ == "__main__":
    main()
