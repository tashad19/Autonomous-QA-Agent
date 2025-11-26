import os
import json
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

class LLMClient:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def _clean_json_text(self, text: str):
        text = text.strip()
        if text.startswith("```"):
            parts = text.split("```")
            if len(parts) >= 2:
                candidate = parts[1]
                if candidate.lower().startswith("json"):
                    candidate = candidate[4:]
                return candidate.strip()
        return text

    def generate_test_cases(self, user_query: str, hits: list):
        context_blocks = []
        for h in hits:
            src = h["metadata"].get("source", "unknown")
            txt = h.get("text", "")
            if len(txt) > 2000:
                txt = txt[:2000]
            block = f"Source: {src}\nContent:\n{txt}"
            context_blocks.append(block)
        context_text = "\n\n".join(context_blocks)

        prompt = f"""
You are a senior QA engineer. You design detailed positive and negative test cases grounded only in the given documentation and HTML.

Project documentation and HTML snippets:
{context_text}

User request:
{user_query}

Instructions:
1. Use only the information from the documentation and HTML above.
2. Do not invent fields or features that are not present there.
3. Produce test cases that cover both positive and negative scenarios, as relevant to the user query.
4. Respond with a JSON array only, no extra text.
5. Each test case object must have exactly these fields:
   - "test_id": string, like "TC-001", "TC-002", etc.
   - "feature": short feature name.
   - "scenario": clear description of the test scenario.
   - "expected": expected result of the test.
   - "grounded_in": array of document filenames that support this test, for example ["assets/product_specs.md"].

Output format example:
[
  {{
    "test_id": "TC-001",
    "feature": "Discount Code",
    "scenario": "Apply valid discount code SAVE15",
    "expected": "Total price is reduced by 15 percent",
    "grounded_in": ["assets/product_specs.md"]
  }}
]
"""

        response = self.model.generate_content(prompt)
        text = response.text or ""
        cleaned = self._clean_json_text(text)
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                data = [data]
            return data
        except Exception:
            return [
                {
                    "test_id": "TC-001",
                    "feature": "Fallback",
                    "scenario": user_query,
                    "expected": "LLM response could not be parsed as JSON",
                    "grounded_in": []
                }
            ]

    def generate_selenium_script(self, test_case: dict, checkout_html: str, hits: list):
        context_blocks = []
        for h in hits:
            src = h["metadata"].get("source", "unknown")
            txt = h.get("text", "")
            if len(txt) > 1500:
                txt = txt[:1500]
            block = f"Source: {src}\nContent:\n{txt}"
            context_blocks.append(block)
        docs_context = "\n\n".join(context_blocks)

        test_case_json = json.dumps(test_case, indent=2)

        prompt = f"""
You are a Selenium (Python) expert QA automation engineer.

You are testing a single page checkout application.

Here is the complete checkout.html source:
<checkout_html>
{checkout_html}
</checkout_html>

Here are relevant documentation snippets:
{docs_context}

Here is the selected test case:
{test_case_json}

Instructions:
1. Write a complete Python Selenium script that executes this test case end to end.
2. Use appropriate locators based on the actual HTML: ids, names, CSS selectors.
3. Assume Chrome WebDriver is used.
4. Assume the file is opened using a local file URL; the caller will replace the path. You should keep a placeholder FILE_URL.
5. Include basic assertions using the DOM where appropriate, for example verifying success messages or error texts.
6. Output Python code only, no explanations, no markdown fences.

Remember:
- Do not invent elements that are not present in the given HTML.
- Ground the script strictly on the provided HTML structure.
"""

        response = self.model.generate_content(prompt)
        text = response.text or ""
        if text.startswith("```"):
            parts = text.split("```")
            if len(parts) >= 2:
                candidate = parts[1]
                if candidate.lower().startswith("python"):
                    candidate = candidate[6:]
                text = candidate.strip()
        return text.strip()
