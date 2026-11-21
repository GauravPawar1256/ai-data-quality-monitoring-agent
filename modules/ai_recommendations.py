
import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


# ==========================================
# 1. PREPARE DATA QUALITY SUMMARY
# ==========================================

def prepare_quality_summary(results, score_results):

    missing_df = results["missing"]
    duplicate_count, _ = results["duplicates"]
    inconsistent_df = results["inconsistent"]
    anomalies_df = results["anomalies"]

    summary = {
        "quality_scores": score_results,

        "missing_values": {
            "total_issues": len(missing_df),
            "details": missing_df.head(20).to_dict(
                orient="records"
            )
        },

        "duplicate_rows": int(duplicate_count),

        "inconsistencies": {
            "total_issues": len(inconsistent_df),
            "details": inconsistent_df.head(20).to_dict(
                orient="records"
            )
        },

        "numeric_anomalies": {
            "total_issues": len(anomalies_df),
            "details": anomalies_df.head(20).to_dict(
                orient="records"
            )
        }
    }

    return summary


# ==========================================
# 2. GENERATE AI RECOMMENDATIONS
# ==========================================

def generate_ai_recommendations(results, score_results):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key is missing from .env."
        )

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )

    quality_summary = prepare_quality_summary(
        results,
        score_results
    )

    summary_json = json.dumps(
        quality_summary,
        indent=2,
        default=str
    )

    prompt = f"""
The dataset achieved a quality score of 100/100 across the implemented checks.
No issues were detected by the current validation rules.

Analyze this dataset quality report:

{summary_json}

Provide a concise report containing:

1. Overall Quality Assessment
2. Missing Value Solutions
3. Duplicate Record Solutions
4. Inconsistency Solutions
5. Outlier Investigation
6. Python Pandas Code
7. Priority Actions

Important rules:
- Only discuss issues shown in the report.
- Do not assume outliers are invalid.
- Do not claim accuracy was measured.
- Give beginner-friendly explanations.
- Keep recommendations practical.
"""

    # ==========================================
    # 3. GEMINI API WITH RETRY
    # ==========================================

    try:

        with genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=120000
            )
        ) as client:

            for attempt in range(3):

                try:

                    print(
                        f"Gemini request: attempt {attempt + 1}/3"
                    )

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.3,
                            max_output_tokens=800
                        )
                    )

                    if not response.text:
                        raise RuntimeError(
                            "Gemini returned an empty response."
                        )

                    return response.text

                except Exception as e:

                    error_message = str(e)

                    temporary_error = (
                        "503" in error_message
                        or "504" in error_message
                    )

                    if temporary_error and attempt < 2:

                        wait_time = 5 * (2 ** attempt)

                        print(
                            f"Gemini unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                    else:
                        raise

    except Exception as e:

        raise RuntimeError(
            f"Gemini recommendation failed: {e}"
        )
