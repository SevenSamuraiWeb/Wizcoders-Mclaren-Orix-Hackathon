import json
from retriever import ContextRetriever

class CreditMemoGenerator:
    """
    Generates a structured banking credit memo using a ContextRetriever and an LLM.
    """
    def __init__(self, retriever: ContextRetriever, llm_client, model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct"):
        """
        Args:
            retriever (ContextRetriever): Retrieval engine for context.
            llm_client: Initialized OpenAI-compatible client (e.g., Groq).
            model_name (str): Name of the model to use.
        """
        self.retriever = retriever
        self.client = llm_client
        self.model_name = model_name

    def generate_credit_memo(self) -> dict:
        """
        Generates the full credit memo by processing each section.
        
        Returns:
            dict: Structured JSON of the credit memo.
        """
        return {
            "document_type": "Banking Credit Memo (Auto-generated)",
            "confidence_level": "Draft – Analyst Review Required",
            "sections": {
                "executive_summary": self._generate_executive_summary(),
                "financial_metrics": self._generate_financial_metrics(),
                "risks": self._generate_risks(),
                "recommendation": self._generate_recommendation()
            }
        }

    def _call_llm(self, original_prompt: str, json_schema: str = None) -> dict:
        """
        Helper to call the LLM with a system prompt enforcing JSON output.
        """
        system_msg = (
            "You are a senior banking credit analyst. "
            "You must output valid JSON only. "
            "Do not output markdown code blocks. "
            "Do not include any conversational text."
        )
        if json_schema:
            system_msg += f"\nFollow this JSON schema strictly:\n{json_schema}"

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": original_prompt}
            ],
            model=self.model_name,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print(f"Error parsing JSON from LLM: {content}")
            return {}

    def _generate_executive_summary(self) -> dict:
        context = self.retriever.retrieve_context("executive_summary")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Generate an Executive Summary.
        Rules:
        - Exactly 5 bullets.
        - Each bullet maps to ONE attribute: Growth, Profitability, Cash Flow, Leverage, Credit View.
        - Cite page numbers like [Page X] using the context headers.
        
        Output JSON format:
        {{
            "highlights": [
                {{
                    "point": "string",
                    "attribute": "Growth | Profitability | Cash Flow | Leverage | Credit View",
                    "sources": [1, 2]
                }}
            ]
        }}
        """
        return self._call_llm(prompt)

    def _generate_financial_metrics(self) -> dict:
        context = self.retriever.retrieve_context("financial_metrics")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Extract Key Financial Metrics.
        Rules:
        - Extract keys: Revenue, EBITDA, Net Profit, Debt, Cash Flow.
        - Use "Information not available" if missing.
        - Cite page numbers.
        
        Output JSON format:
        {{
            "metrics": [
                {{
                    "name": "Revenue | EBITDA | Net Profit | Debt | Cash Flow",
                    "value": "string or number",
                    "period": "FY24",
                    "confidence": "Strong | Estimated | Not Available",
                    "sources": [1]
                }}
            ]
        }}
        """
        return self._call_llm(prompt)

    def _generate_risks(self) -> dict:
        context = self.retriever.retrieve_context("risks")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Identify Key Risks.
        Rules:
        - Max 3 risks.
        - Must be grounded in context.
        - No generic risks.
        
        Output JSON format:
        {{
            "items": [
                {{
                    "risk_title": "string",
                    "description": "short factual description",
                    "risk_type": "Financial | Liquidity | Business | Operational",
                    "severity": "Low | Medium | High",
                    "sources": [1]
                }}
            ]
        }}
        """
        return self._call_llm(prompt)

    def _generate_recommendation(self) -> dict:
        context = self.retriever.retrieve_context("recommendation")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Generate Credit Recommendation.
        Rules:
        - Stance must be Positive, Neutral, Cautious, or Negative.
        - Summary max 2-3 lines.
        
        Output JSON format:
        {{
            "stance": "Positive | Neutral | Cautious | Negative",
            "summary": "2–3 lines max",
            "justification": [
                {{
                    "point": "string",
                    "sources": [1]
                }}
            ]
        }}
        """
        return self._call_llm(prompt)
