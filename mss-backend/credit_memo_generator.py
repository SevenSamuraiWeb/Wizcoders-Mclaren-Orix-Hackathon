import json
from retriever import ContextRetriever
from typing import Optional

class CreditMemoGenerator:
    """
    Generates a structured banking credit memo using a ContextRetriever and an LLM.
    Enforces the refined 5Cs schema with strict JSON output and source citations.
    """
    def __init__(self, retriever: ContextRetriever, llm_client, model_name: str = "meta-llama/llama-4-scout-17b-16e-instruct", settings=None):
        self.retriever = retriever
        self.client = llm_client
        self.model_name = model_name
        self.settings = settings

    def generate_credit_memo(self) -> dict:
        """
        Generates the full credit memo by processing each section.
        Respects user settings for which sections to include.
        """
        result = {}
        
        # Get preferences
        prefs = self.settings.reportPreferences if self.settings else None
        include_summary = prefs.includeExecutiveSummary if prefs else True
        include_5cs = prefs.include5Cs if prefs else True
        include_risks = prefs.includeRiskAssessment if prefs else True
        
        # Execute sections based on preferences
        if include_summary:
            result["summary"] = self._generate_executive_summary()
        
        # Financial metrics are always included
        result["financial_metrics"] = self._generate_financial_metrics()
        
        if include_5cs:
            result["credit_analysis_5cs"] = self._generate_5cs()
        
        if include_risks:
            result["risk_assessment"] = self._generate_risks()
        
        # Construct Metadata (Simplified for prototype)
        metadata = {
            "document_id": "auto-generated-id",
            "document_name": "Financial_Statement.pdf",
            "pages_analyzed": 0, # Placeholder, needing integration with vector store meta
            "overall_confidence": 0.85,
            "processing_time_ms": 1200,
            "model_info": self.model_name
        }
        result["metadata"] = metadata

        return result

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
        metrics = response.get("metrics", [])
        
        # Apply user-defined risk thresholds if available
        if self.settings and self.settings.riskThresholds:
            metrics = self._apply_risk_thresholds(metrics)
        
        return metrics
    
    def _apply_risk_thresholds(self, metrics: list) -> list:
        """
        Re-evaluate metric status based on user-defined risk thresholds.
        """
        thresholds = self.settings.riskThresholds
        
        for metric in metrics:
            try:
                label = metric.get("label", "").lower()
                value = float(metric.get("value", 0))
                
                # Apply liquidity ratio threshold (Current Ratio)
                if "current ratio" in label or "liquidity" in label:
                    if value < thresholds.liquidityRatio:
                        metric["status"] = "critical"
                    elif value < thresholds.liquidityRatio * 1.2:
                        metric["status"] = "warning"
                    else:
                        metric["status"] = "healthy"
                
                # Apply debt-to-equity threshold
                elif "debt" in label and "equity" in label:
                    if value > thresholds.debtToEquity:
                        metric["status"] = "critical"
                    elif value > thresholds.debtToEquity * 0.8:
                        metric["status"] = "warning"
                    else:
                        metric["status"] = "healthy"
                
                # Apply net profit margin threshold
                elif "profit margin" in label or "net margin" in label:
                    if value < thresholds.netProfitMargin:
                        metric["status"] = "critical"
                    elif value < thresholds.netProfitMargin * 1.2:
                        metric["status"] = "warning"
                    else:
                        metric["status"] = "healthy"
            except (ValueError, TypeError):
                # Keep original status if value conversion fails
                pass
        
        return metrics

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
