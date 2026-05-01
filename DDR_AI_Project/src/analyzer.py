import os
from dotenv import load_dotenv
from groq import Groq


class AIAnalyzer:
    def __init__(self):
        load_dotenv()

        # api_key = os.getenv("GROQ_API_KEY")
        api_key = ""

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)

        # Good default model
        self.model = "llama-3.3-70b-versatile"

    def build_prompt(self, merged_text):
        return f"""
You are a professional civil/building diagnostic engineer.

Analyze inspection + thermal findings.

Return clean professional DDR report with:

1. Executive Summary

2. Area Wise Findings:
- Area
- Problem
- Root Cause
- Severity (Low/Medium/High/Critical)
- Recommended Solution
- Priority

3. Overall Risks If Delayed

4. Final Recommendation

DATA:
{merged_text[:12000]}
"""

    def analyze(self, merged_text):
        prompt = self.build_prompt(merged_text)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )

        return response.choices[0].message.content

    def run(self, merged_result):
        print("Running AI diagnostic analysis via Groq...")

        combined_text = merged_result["combined_text"]

        ai_report = self.analyze(combined_text)

        return {"ai_report": ai_report}


if __name__ == "__main__":
    sample = {
        "combined_text": "Wall dampness, thermal moisture near corner, terrace cracks."
    }

    analyzer = AIAnalyzer()
    result = analyzer.run(sample)
    print(result["ai_report"])