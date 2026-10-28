import os
import json
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Fake Job & Internship Ad Detector",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Fake Job & Internship Ad Detector")

st.write(
    "Analyze a job or internship advertisement for potential "
    "scam indicators using AI."
)

st.info(
    "This tool provides a risk assessment based on the text you provide. "
    "It does not prove that an advertisement is definitely fake."
)

# Get Groq API Key
api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

# Job Advertisement Input
job_ad = st.text_area(
    "Paste Job / Internship Advertisement",
    height=300,
    placeholder="Paste the complete job or internship advertisement here..."
)

# Analyze Button
if st.button("🔍 Analyze Advertisement", use_container_width=True):

    if not job_ad.strip():
        st.warning("Please paste a job or internship advertisement first.")

    elif len(job_ad.strip()) < 50:
        st.warning(
            "Please provide more information about the advertisement "
            "for a better analysis."
        )

    elif not api_key:
        st.error(
            "Groq API key is not configured. "
            "Add GROQ_API_KEY in Streamlit Secrets."
        )

    else:

        with st.spinner("Analyzing advertisement..."):

            try:
                client = Groq(api_key=api_key)

                prompt = f"""
You are a cybersecurity assistant specializing in job and internship scam detection.

Analyze the following job/internship advertisement for potential scam indicators.

IMPORTANT:
- Do not claim that an advertisement is definitely fraudulent.
- Provide a risk assessment based only on the supplied text.
- Identify suspicious indicators and explain them clearly.
- If there is insufficient evidence, say so.
- Do not invent facts about the company or employer.

Return ONLY valid JSON in this exact structure:

{{
    "risk_level": "LOW, MEDIUM, or HIGH",
    "risk_score": 0,
    "summary": "Short explanation",
    "red_flags": [
        "Red flag 1",
        "Red flag 2"
    ],
    "positive_signs": [
        "Positive sign 1"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}}

Risk score should be an integer from 0 to 100.

Advertisement:

{job_ad}
"""

                response = client.chat.completions.create(
                    model="model="openai/gpt-oss-20b",",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a cybersecurity assistant. "
                                "Analyze job advertisements carefully "
                                "and return the requested JSON only."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=1200
                )

                result_text = response.choices[0].message.content

                result_text = result_text.replace("```json", "")
                result_text = result_text.replace("```", "")
                result_text = result_text.strip()

                result = json.loads(result_text)

                st.divider()

                st.subheader("📊 Risk Assessment")

                risk_level = result.get("risk_level", "UNKNOWN")
                risk_score = result.get("risk_score", 0)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Risk Score", f"{risk_score}/100")

                with col2:
                    st.metric("Risk Level", risk_level)

                if risk_level.upper() == "HIGH":
                    st.error(
                        "🔴 HIGH RISK — Several potential scam indicators "
                        "were identified."
                    )

                elif risk_level.upper() == "MEDIUM":
                    st.warning(
                        "🟡 MEDIUM RISK — Some suspicious indicators "
                        "were identified."
                    )

                elif risk_level.upper() == "LOW":
                    st.success(
                        "🟢 LOW RISK — No major warning signs were "
                        "identified from the supplied text."
                    )

                else:
                    st.info(
                        "The AI could not determine a clear risk level."
                    )

                st.subheader("📝 Analysis Summary")
                st.write(result.get("summary", "No summary available."))

                st.subheader("🚩 Potential Red Flags")

                red_flags = result.get("red_flags", [])

                if red_flags:
                    for flag in red_flags:
                        st.warning(f"• {flag}")
                else:
                    st.write("No major red flags identified.")

                st.subheader("✅ Positive Signs")

                positive_signs = result.get("positive_signs", [])

                if positive_signs:
                    for sign in positive_signs:
                        st.success(f"• {sign}")
                else:
                    st.write("No strong positive signs identified.")

                st.subheader("🛡️ Safety Recommendations")

                recommendations = result.get("recommendations", [])

                for recommendation in recommendations:
                    st.write(f"• {recommendation}")

                st.divider()

                st.caption(
                    "Disclaimer: This AI tool provides an indicative risk "
                    "assessment based on the advertisement text. It does "
                    "not verify the employer's identity and cannot guarantee "
                    "that an advertisement is genuine or fraudulent."
                )

            except json.JSONDecodeError:
                st.error(
                    "The AI returned an unexpected response format. "
                    "Please try analyzing the advertisement again."
                )

            except Exception as e:
                st.error(
                    f"An error occurred while analyzing the advertisement: {e}"
                )
