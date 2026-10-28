import os
import json
import streamlit as st
from groq import Groq


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Fake Job & Internship Ad Detector",
    page_icon="🔍",
    layout="centered"
)


# ==========================================
# HEADER
# ==========================================

st.title("🔍 Fake Job & Internship Ad Detector")

st.write(
    "Analyze a job or internship advertisement for "
    "potential scam indicators using Artificial Intelligence."
)

st.info(
    "This tool provides an indicative risk assessment. "
    "It does not prove that an advertisement is definitely fake or genuine."
)


# ==========================================
# GET GROQ API KEY
# ==========================================

api_key = None

# First try Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# If Secrets are not available, try environment variable
if not api_key:
    api_key = os.getenv("GROQ_API_KEY")


# ==========================================
# USER INPUT
# ==========================================

job_ad = st.text_area(
    "📋 Paste Job / Internship Advertisement",
    height=300,
    placeholder=(
        "Paste the complete job or internship advertisement here..."
    )
)


# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("🔍 Analyze Advertisement", use_container_width=True):

    # Empty input check
    if not job_ad.strip():

        st.warning(
            "Please paste a job or internship advertisement first."
        )

    # Short input check
    elif len(job_ad.strip()) < 50:

        st.warning(
            "Please provide more information about the advertisement "
            "for a better analysis."
        )

    # API key check
    elif not api_key:

        st.error(
            "Groq API key is not configured. "
            "Please add GROQ_API_KEY in Streamlit Secrets."
        )

    else:

        # ==========================================
        # AI ANALYSIS
        # ==========================================

        with st.spinner("🔎 Analyzing advertisement..."):

            try:

                client = Groq(api_key=api_key)

                prompt = f"""
You are a cybersecurity assistant specializing in
job and internship scam detection.

Analyze the following job or internship advertisement
for potential scam indicators.

Your job is to identify warning signs based ONLY
on the advertisement text provided by the user.

IMPORTANT RULES:

1. Do NOT claim that the advertisement is definitely fake.
2. Do NOT claim that the advertisement is definitely genuine.
3. Give an indicative risk assessment.
4. Explain the reasons for the risk assessment.
5. Do not invent information about the company.
6. Identify suspicious indicators when present.
7. Mention positive signs when present.
8. Give practical safety recommendations.
9. Risk score must be an integer between 0 and 100.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "risk_level": "LOW",
    "risk_score": 0,
    "summary": "Short explanation of the analysis.",
    "red_flags": [
        "Potential red flag 1",
        "Potential red flag 2"
    ],
    "positive_signs": [
        "Positive sign 1",
        "Positive sign 2"
    ],
    "recommendations": [
        "Safety recommendation 1",
        "Safety recommendation 2"
    ]
}}

Risk levels:

LOW:
Few or no significant warning signs are visible
in the supplied advertisement.

MEDIUM:
Some warning signs are present and additional
verification is recommended.

HIGH:
Several strong warning signs are present and
the user should exercise significant caution.

Advertisement to analyze:

{job_ad}
"""

                # ==========================================
                # GROQ REQUEST
                # ==========================================

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a cybersecurity assistant "
                                "specializing in job scam analysis. "
                                "Return only valid JSON."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=1200,
                    response_format={
                        "type": "json_object"
                    }
                )

                # ==========================================
                # PROCESS AI RESPONSE
                # ==========================================

                result_text = response.choices[0].message.content

                result = json.loads(result_text)

                # ==========================================
                # GET RESULTS
                # ==========================================

                risk_level = str(
                    result.get("risk_level", "UNKNOWN")
                ).upper()

                risk_score = result.get("risk_score", 0)

                summary = result.get(
                    "summary",
                    "No summary available."
                )

                red_flags = result.get(
                    "red_flags",
                    []
                )

                positive_signs = result.get(
                    "positive_signs",
                    []
                )

                recommendations = result.get(
                    "recommendations",
                    []
                )


                # ==========================================
                # DISPLAY RESULTS
                # ==========================================

                st.divider()

                st.subheader("📊 Risk Assessment")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Risk Score",
                        f"{risk_score}/100"
                    )

                with col2:
                    st.metric(
                        "Risk Level",
                        risk_level
                    )


                # ==========================================
                # RISK LEVEL MESSAGE
                # ==========================================

                if risk_level == "HIGH":

                    st.error(
                        "🔴 HIGH RISK — Several potential "
                        "scam indicators were identified."
                    )

                elif risk_level == "MEDIUM":

                    st.warning(
                        "🟡 MEDIUM RISK — Some potential "
                        "warning signs were identified."
                    )

                elif risk_level == "LOW":

                    st.success(
                        "🟢 LOW RISK — No major warning signs "
                        "were identified from the supplied text."
                    )

                else:

                    st.info(
                        "The AI could not determine a clear risk level."
                    )


                # ==========================================
                # SUMMARY
                # ==========================================

                st.subheader("📝 Analysis Summary")

                st.write(summary)


                # ==========================================
                # RED FLAGS
                # ==========================================

                st.subheader("🚩 Potential Red Flags")

                if red_flags:

                    for flag in red_flags:

                        st.warning(
                            f"• {flag}"
                        )

                else:

                    st.write(
                        "No major red flags were identified."
                    )


                # ==========================================
                # POSITIVE SIGNS
                # ==========================================

                st.subheader("✅ Positive Signs")

                if positive_signs:

                    for sign in positive_signs:

                        st.success(
                            f"• {sign}"
                        )

                else:

                    st.write(
                        "No strong positive signs were identified."
                    )


                # ==========================================
                # RECOMMENDATIONS
                # ==========================================

                st.subheader("🛡️ Safety Recommendations")

                if recommendations:

                    for recommendation in recommendations:

                        st.write(
                            f"• {recommendation}"
                        )

                else:

                    st.write(
                        "No recommendations were generated."
                    )


                # ==========================================
                # DISCLAIMER
                # ==========================================

                st.divider()

                st.caption(
                    "Disclaimer: This application provides an "
                    "indicative risk assessment based on the "
                    "advertisement text provided by the user. "
                    "It does not independently verify the employer "
                    "or guarantee that an advertisement is genuine "
                    "or fraudulent."
                )


            # ==========================================
            # ERROR HANDLING
            # ==========================================

            except json.JSONDecodeError:

                st.error(
                    "The AI returned an unexpected response format. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"An error occurred while analyzing the advertisement: {e}"
                )
