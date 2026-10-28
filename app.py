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
    "Analyze a job or internship advertisement for potential "
    "scam indicators using AI."
)

st.info(
    "This tool provides an indicative risk assessment. "
    "It does not prove that an advertisement is definitely fake or genuine."
)


# ==========================================
# GROQ API KEY
# ==========================================

api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")


# ==========================================
# INPUT
# ==========================================

job_ad = st.text_area(
    "📋 Paste Job / Internship Advertisement",
    height=300,
    placeholder="Paste the complete advertisement here..."
)


# ==========================================
# ANALYZE
# ==========================================

if st.button("🔍 Analyze Advertisement", use_container_width=True):

    if not job_ad.strip():

        st.warning(
            "Please paste a job or internship advertisement first."
        )

    elif len(job_ad.strip()) < 50:

        st.warning(
            "Please provide more information about the advertisement."
        )

    elif not api_key:

        st.error(
            "Groq API key is not configured. "
            "Please add GROQ_API_KEY in Streamlit Secrets."
        )

    else:

        with st.spinner("🔎 Analyzing advertisement..."):

            try:

                client = Groq(api_key=api_key)

                prompt = f"""
Analyze this job or internship advertisement for potential scam indicators.

Do not say it is definitely fake or genuine.
Give an indicative assessment based only on the supplied text.

Return ONLY valid JSON using this exact structure:

{{
  "risk_level": "HIGH",
  "risk_score": 85,
  "summary": "Short explanation.",
  "red_flags": [
    "Short red flag",
    "Short red flag",
    "Short red flag"
  ],
  "positive_signs": [
    "Short positive sign"
  ],
  "recommendations": [
    "Short safety recommendation",
    "Short safety recommendation"
  ]
}}

Rules:
- risk_level must be LOW, MEDIUM, or HIGH.
- risk_score must be an integer from 0 to 100.
- Keep summary under 40 words.
- Give at most 3 red flags.
- Give at most 2 positive signs.
- Give at most 3 recommendations.
- Keep every item short.
- Return JSON only.

Advertisement:
{job_ad}
"""

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a cybersecurity assistant "
                                "that analyzes job scam indicators. "
                                "Return only valid JSON."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                    max_tokens=2000,
                    response_format={
                        "type": "json_object"
                    }
                )

                result_text = response.choices[0].message.content

                result = json.loads(result_text)

                # ==========================================
                # RESULTS
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
                # RISK ASSESSMENT
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
                # RISK MESSAGE
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
                        st.warning(f"• {flag}")

                else:

                    st.write(
                        "No major red flags identified."
                    )

                # ==========================================
                # POSITIVE SIGNS
                # ==========================================

                st.subheader("✅ Positive Signs")

                if positive_signs:

                    for sign in positive_signs:
                        st.success(f"• {sign}")

                else:

                    st.write(
                        "No strong positive signs identified."
                    )

                # ==========================================
                # RECOMMENDATIONS
                # ==========================================

                st.subheader("🛡️ Safety Recommendations")

                if recommendations:

                    for recommendation in recommendations:
                        st.write(f"• {recommendation}")

                else:

                    st.write(
                        "No recommendations generated."
                    )

                # ==========================================
                # DISCLAIMER
                # ==========================================

                st.divider()

                st.caption(
                    "Disclaimer: This application provides an "
                    "indicative risk assessment based on the "
                    "advertisement text. It does not independently "
                    "verify the employer or guarantee that an "
                    "advertisement is genuine or fraudulent."
                )

            except json.JSONDecodeError:

                st.error(
                    "The AI returned an invalid JSON response. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"An error occurred while analyzing the advertisement: {e}"
                )
