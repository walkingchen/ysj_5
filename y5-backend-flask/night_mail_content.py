from html import escape
from urllib.parse import urlencode


DAILY_SURVEY_LINKS = {
    1: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_9TRP5mPfk7oac6O",
    2: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_8cTbJ0UWbgnSJLg",
    3: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_bykweL3JOk9ayKW",
    4: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_erDHeg4NlmMBU3Q",
    5: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_1GkkxaJOYMTpaR0",
    6: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_38VfuwQEo1qTNtk",
    7: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_1SUWdDVDs6g3sTY",
    8: "https://uwmadison.co1.qualtrics.com/jfe/form/SV_6PAszQdAP1RJxn8",
}


def build_night_mail_subject(day):
    return f"Chattera Night Mail and Daily Survey - DAY {day}"


def build_night_mail_content(day, payment, rid=None):
    survey_link = DAILY_SURVEY_LINKS[day]
    if rid is not None and str(rid).strip():
        separator = "&" if "?" in survey_link else "?"
        survey_link = f"{survey_link}{separator}{urlencode({'rid': str(rid).strip()})}"

    survey_link_html = escape(survey_link, quote=True)
    payment_text = escape(str(payment))

    return f"""
<p>Good evening! Thank you for staying with us on Chattera. So far, you have earned ${payment_text}.</p>
<p>Before today ends, don’t forget to complete your daily survey to earn an additional $0.25. The survey only takes about 1 minute to complete.</p>
<p>Daily Survey Link:<br>
<a href="{survey_link_html}">{survey_link_html}</a></p>
""".strip()
