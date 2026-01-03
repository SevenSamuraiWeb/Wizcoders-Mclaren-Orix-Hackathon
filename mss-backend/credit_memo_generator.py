import json
from retriever import ContextRetriever

class CreditMemoGenerator:
    """
    Generates a structured banking credit memo using a ContextRetriever and an LLM.
    Enforces the refined 5Cs schema with strict JSON output and source citations.
    """
    def __init__(self, retriever: ContextRetriever, llm_client, model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct"):
        self.retriever = retriever
        self.client = llm_client
        self.model_name = model_name

    def generate_credit_memo(self) -> dict:
        """
        Generates the full credit memo by processing each section.
        """
        # Execute sections in parallel could be an optimization, but sequential is safer for now
        summary = self._generate_executive_summary()
        financials = self._generate_financial_metrics()
        five_cs = self._generate_5cs()
        risks = self._generate_risks()
        
        # Construct Metadata (Simplified for prototype)
        metadata = {
            "document_id": "auto-generated-id",
            "document_name": "Financial_Statement.pdf",
            "pages_analyzed": 0, # Placeholder, needing integration with vector store meta
            "overall_confidence": 0.85,
            "processing_time_ms": 1200,
            "model_info": self.model_name
        }

        return {
            "summary": summary,
            "financial_metrics": financials,
            "credit_analysis_5cs": five_cs,
            "risk_assessment": risks,
            "metadata": metadata
        }

    def _call_llm(self, original_prompt: str, json_schema: str = None) -> dict:
        system_msg = (
            "You are a senior banking credit analyst. "
            "You must output valid JSON only. "
            "Do not output markdown code blocks. "
            "Do not include any conversational text. "
            "Every fact must be cited if possible."
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
        
        Output JSON:
        {{
            "executive_summary": "Detailed narrative summary of the credit profile (markdown enabled).",
            "recommendation": "Approve | Decline | Conditional Approval",
            "key_takeaways": ["str1", "str2", "str3", "str4"]
        }}
        """
        return self._call_llm(prompt)

    def _generate_financial_metrics(self) -> list:
        context = self.retriever.retrieve_context("financial_metrics")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Extract Key Financial Metrics.
        Rules:
        - Include Current Ratio, EBITDA Margin, Debt-to-Equity, Net Profit Margin.
        - "is_calculated": true if you derived it, false if extracted directly.
        - "source": {{ "page_number": int, "snippet": "exact text string" }} (Use 0 if unknown)
        
        Output JSON format (List of objects):
        [
            {{
                "category": "Liquidity | Profitability | Leverage",
                "label": "string",
                "value": number or string,
                "unit": "ratio | % | USD",
                "status": "healthy | warning | critical",
                "is_calculated": boolean,
                "source": {{ "page_number": int, "snippet": "string" }}
            }}
        ]
        
        Wrap the list in a key called "metrics" for valid JSON object.
        """
        response = self._call_llm(prompt)
        return response.get("metrics", [])

    def _generate_5cs(self) -> dict:
        context = self.retriever.retrieve_context("credit_analysis_5cs")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Analyze the 5Cs of Credit.
        
        JSON Structure:
        {{
          "character": {{
            "assessment": "string",
            "confidence": float (0-1),
            "source_citations": [{{ "page": int, "snippet": "string" }}]
          }},
          "capacity": {{
            "repayment_source": "string",
            "ratios": {{ "dscr": number, "interest_coverage": number }},
            "confidence": float,
            "source_citations": [{{ "page": int, "snippet": "string" }}]
          }},
          "capital": {{
            "equity_position": "string",
            "leverage_ratio": number,
            "net_worth": number,
            "confidence": float,
            "source_citations": [{{ "page": int, "snippet": "string" }}]
          }},
          "collateral": {{
            "pledged_assets": ["string"],
            "ltv_ratio": number,
            "valuation": number,
            "confidence": float,
            "source_citations": [{{ "page": int, "snippet": "string" }}]
          }},
          "conditions": {{
            "loan_purpose": "string",
            "market_outlook": "string",
            "covenants": ["string"],
            "confidence": float,
            "source_citations": [{{ "page": int, "snippet": "string" }}]
          }}
        }}
        """
        return self._call_llm(prompt)

    def _generate_risks(self) -> dict:
        context = self.retriever.retrieve_context("risks")
        prompt = f"""
        Context:
        {context['context_text']}

        Task: Risk Assessment.
        
        JSON Structure:
        {{
            "red_flags": [
                {{
                    "issue": "string",
                    "severity": "High | Med | Low",
                    "confidence": float,
                    "mitigant": "string",
                    "source": {{ "page": int, "snippet": "string" }}
                }}
            ],
            "strengths": [
               {{ "text": "string", "source": {{ "page": int, "snippet": "string" }} }}
            ],
            "weaknesses": [
               {{ "text": "string", "source": {{ "page": int, "snippet": "string" }} }}
            ]
        }}
        """
        return self._call_llm(prompt)
