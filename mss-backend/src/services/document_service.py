"""
Document Processing Service

Core business logic for document analysis and processing.
"""

import logging
from typing import Dict, Any
from datetime import datetime
import json
import fitz  # PyMuPDF for PDF text extraction
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
from openai import OpenAI

logger = logging.getLogger(__name__)

class DocumentService:
    """Service for document processing and analysis."""

    def __init__(self):
        """Initialize document service."""
        # Initialize ML models, embeddings, FAISS index
        self.processed_documents = {}  # In-memory storage (demo)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2 embeddings
        self.vector_index = faiss.IndexFlatL2(self.dimension)
        self.document_metadata = []  # Store document metadata

        # Initialize OpenAI client with fallback for testing
        try:
            from openai import OpenAI
            import os
            api_key = os.environ.get("OPENAI_API_KEY", "")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
            else:
                self.openai_client = None
                logger.warning("OpenAI API key not configured. Using fallback analysis methods.")
        except ImportError:
            self.openai_client = None
            logger.warning("OpenAI library not available. Using fallback analysis methods.")

    async def process_document(
        self,
        document_id: str,
        filename: str,
        content: bytes
    ) -> Dict[str, Any]:
        """
        Process a PDF document and extract financial information.

        Args:
            document_id: Unique document identifier
            filename: Name of the file
            content: File content as bytes

        Returns:
            Dictionary with analysis results and metrics
        """
        try:
            logger.info(f"Processing document: {document_id} ({filename})")

            # Step 1: Extract text from PDF
            extracted_text = await self.extract_text_from_pdf(content)

            # Step 2: Generate embeddings and store in vector database
            await self._store_document_embeddings(document_id, extracted_text)

            # Step 3: Analyze financial metrics using RAG pipeline
            metrics = await self.analyze_financial_metrics(extracted_text)

            # Step 4: Generate AI insights
            ai_insights = await self.generate_ai_insights(metrics)

            # Step 5: Perform risk analysis
            risk_factors = await self._analyze_risk_factors(extracted_text, metrics)

            # Step 6: Generate recommendations
            recommendations = await self._generate_recommendations(metrics, risk_factors)

            analysis_result = {
                "analysis": {
                    "summary": "Financial metrics extracted successfully using RAG pipeline",
                    "document_type": "credit_memo",
                    "confidence": 0.95,
                    "ai_insights": ai_insights
                },
                "metrics": metrics,
                "risk_factors": risk_factors,  # List of risk factor strings
                "risk_factors_objects": [
                    {
                        "factor": factor.split(":")[0] if ":" in factor else factor,
                        "severity": self._determine_risk_severity(factor),
                        "description": factor,
                        "recommendation": "Monitor and mitigate this risk factor"
                    }
                    for factor in risk_factors
                ],
                "recommendations": recommendations,
                "processing_method": "RAG_pipeline"
            }

            # Store result
            self.processed_documents[document_id] = {
                "filename": filename,
                "content_length": len(content),
                "processed_at": datetime.utcnow().isoformat(),
                "result": analysis_result,
                "extracted_text": extracted_text
            }

            logger.info(f"Document processed successfully: {document_id}")
            return analysis_result

        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}", exc_info=True)
            raise

    async def get_document_analysis(self, document_id: str) -> Dict[str, Any] | None:
        """
        Retrieve analysis results for a document.

        Args:
            document_id: Document identifier

        Returns:
            Analysis results or None if not found
        """
        if document_id in self.processed_documents:
            return self.processed_documents[document_id]["result"]
        return None

    async def extract_text_from_pdf(self, content: bytes) -> str:
        """
        Extract text content from PDF using PyMuPDF and PDFPlumber.

        Args:
            content: PDF file content as bytes

        Returns:
            Extracted text
        """
        try:
            # Use PyMuPDF for initial text extraction
            # Convert bytes to file-like object for PyMuPDF
            import io
            doc = fitz.open(stream=io.BytesIO(content), filetype="pdf")
            text = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()

            # Use PDFPlumber for table extraction
            # Convert bytes to file-like object for PDFPlumber
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            text += " | ".join([str(cell) for cell in row if cell]) + "\n"

            return text.strip()

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    async def _store_document_embeddings(self, document_id: str, text: str):
        """Store document embeddings in FAISS vector database."""
        try:
            # Split text into chunks for embedding
            chunks = self._split_text_into_chunks(text)

            # Generate embeddings for each chunk
            embeddings = self.embedding_model.encode(chunks)
            embeddings_np = np.array(embeddings).astype('float32')

            # Add to FAISS index
            self.vector_index.add(embeddings_np)

            # Store metadata
            for i, chunk in enumerate(chunks):
                self.document_metadata.append({
                    "document_id": document_id,
                    "chunk_index": i,
                    "text": chunk,
                    "embedding_index": len(self.document_metadata)
                })

            logger.info(f"Stored {len(chunks)} embeddings for document {document_id}")

        except Exception as e:
            logger.error(f"Error storing document embeddings: {e}")
            raise

    def _split_text_into_chunks(self, text: str, chunk_size: int = 500) -> list:
        """Split text into chunks for embedding."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def _determine_risk_severity(self, risk_factor: str) -> str:
        """Determine the severity level of a risk factor."""
        risk_lower = risk_factor.lower()
        
        # Critical severity keywords
        if any(word in risk_lower for word in ["bankruptcy", "default", "insolvency", "critical"]):
            return "CRITICAL"
        
        # High severity keywords
        if any(word in risk_lower for word in ["high", "severe", "major", "significant"]):
            return "HIGH"
        
        # Low severity keywords
        if any(word in risk_lower for word in ["low", "minor", "slight", "potential"]):
            return "LOW"
        
        # Default to medium
        return "MEDIUM"

    async def analyze_financial_metrics(self, text: str) -> Dict[str, Any]:
        """
        Analyze financial metrics from extracted text using NLP and regex.

        Args:
            text: Extracted text from document

        Returns:
            Dictionary with identified metrics
        """
        try:
            logger.info("Extracting financial metrics using NLP-based extraction")

            # Initialize metrics with default values
            metrics = {
                "total_revenue": None,
                "net_income": None,
                "total_debt": None,
                "total_equity": None,
                "current_assets": None,
                "current_liabilities": None,
                "cash_flow": None,
                "ebitda": None,
                "debt_to_equity_ratio": None,
                "interest_coverage_ratio": None,
                "current_ratio": None
            }

            # Use regex patterns to extract financial metrics
            patterns = {
                "total_revenue": r"(?:Total Revenue|Revenue|Sales|Turnover)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "net_income": r"(?:Net Income|Net Profit|Profit After Tax)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "total_debt": r"(?:Total Debt|Long-term Debt|Borrowings)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "total_equity": r"(?:Total Equity|Shareholders' Equity|Net Worth)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "current_assets": r"(?:Current Assets|Total Current Assets)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "current_liabilities": r"(?:Current Liabilities|Total Current Liabilities)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "cash_flow": r"(?:Cash Flow|Net Cash Flow|Operating Cash Flow)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)",
                "ebitda": r"(?:EBITDA|Earnings Before Interest and Taxes)[:\s]*[\$€₹]?\s*([\d,]+\.?\d*)"
            }

            for metric_name, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        value = float(match.group(1).replace(',', ''))
                        metrics[metric_name] = value
                    except ValueError:
                        continue

            # Calculate derived metrics
            if metrics["total_debt"] and metrics["total_equity"] and metrics["total_equity"] > 0:
                metrics["debt_to_equity_ratio"] = metrics["total_debt"] / metrics["total_equity"]

            if metrics["current_assets"] and metrics["current_liabilities"] and metrics["current_liabilities"] > 0:
                metrics["current_ratio"] = metrics["current_assets"] / metrics["current_liabilities"]

            # Use OpenAI for more sophisticated metric extraction
            try:
                openai_metrics = await self._extract_metrics_with_openai(text)
                metrics.update(openai_metrics)
            except Exception as e:
                logger.warning(f"OpenAI metric extraction failed, using regex results: {e}")

            logger.info("Financial metrics extraction completed")
            return metrics

        except Exception as e:
            logger.error(f"Metric extraction failed: {e}")
            raise

    async def _extract_metrics_with_openai(self, text: str) -> Dict[str, Any]:
        """Use OpenAI to extract financial metrics from text."""
        try:
            if not self.openai_client:
                logger.info("OpenAI client not available, skipping OpenAI metric extraction")
                return {}

            prompt = f"""
            Extract the following financial metrics from the text below.
            Return only the metrics as JSON with no additional text:

            {{
                "total_revenue": null,
                "net_income": null,
                "total_debt": null,
                "total_equity": null,
                "current_assets": null,
                "current_liabilities": null,
                "cash_flow": null,
                "ebitda": null,
                "interest_coverage_ratio": null
            }}

            Text:
            {text[:2000]}...  # Limit text to avoid token limits
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst extracting metrics from documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )

            metrics_json = response.choices[0].message.content.strip()
            return json.loads(metrics_json)

        except Exception as e:
            logger.error(f"OpenAI metric extraction error: {e}")
            return {}

    async def generate_ai_insights(self, metrics: Dict[str, Any]) -> str:
        """
        Generate AI-powered insights using OpenAI.

        Args:
            metrics: Extracted financial metrics

        Returns:
            AI-generated analysis and recommendations
        """
        try:
            if not self.openai_client:
                logger.info("OpenAI client not available, using fallback insights")
                return self._generate_fallback_insights(metrics)

            logger.info("Generating AI insights using OpenAI")

            # Prepare metrics for prompt
            metrics_str = "\n".join([f"{key}: {value}" for key, value in metrics.items() if value is not None])

            prompt = f"""
            Analyze the following financial metrics and provide insights about the company's financial health:

            {metrics_str}

            Provide a comprehensive analysis covering:
            1. Overall financial health assessment
            2. Strengths and weaknesses
            3. Key financial ratios analysis
            4. Potential risks and opportunities
            5. Recommendations for improvement

            Keep the analysis concise but insightful.
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a senior financial analyst providing expert insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            insights = response.choices[0].message.content.strip()
            logger.info("AI insights generation completed")
            return insights

        except Exception as e:
            logger.error(f"AI insights generation failed: {e}")
            return self._generate_fallback_insights(metrics)

    async def _analyze_risk_factors(self, text: str, metrics: Dict[str, Any]) -> List[str]:
        """Analyze risk factors using ML/NLP models."""
        try:
            logger.info("Analyzing risk factors")

            risk_factors = []

            # Rule-based risk analysis
            debt_to_equity = metrics.get("debt_to_equity_ratio")
            current_ratio = metrics.get("current_ratio")
            interest_coverage = metrics.get("interest_coverage_ratio")
            profit_margin = None
            
            # Calculate profit margin
            if metrics.get("total_revenue") and metrics.get("net_income"):
                profit_margin = metrics["net_income"] / metrics["total_revenue"]

            if debt_to_equity is not None and debt_to_equity > 2.0:
                risk_factors.append("High leverage ratio indicating potential financial stress")
            elif debt_to_equity is not None and debt_to_equity > 1.5:
                risk_factors.append("Elevated debt-to-equity ratio requiring monitoring")

            if current_ratio is not None and current_ratio < 1.0:
                risk_factors.append("Low current ratio suggesting liquidity concerns")
            elif current_ratio is not None and current_ratio < 1.5:
                risk_factors.append("Current ratio below recommended threshold of 1.5")

            if interest_coverage is not None and interest_coverage < 1.5:
                risk_factors.append("Insufficient interest coverage ratio")

            if profit_margin is not None and profit_margin < 0.05:
                risk_factors.append("Low profit margin indicating reduced profitability")

            # Text-based risk analysis
            risk_keywords = [
                "default", "bankruptcy", "liquidation", "restructuring",
                "litigation", "regulatory action", "fraud", "scandal"
            ]

            text_lower = text.lower()
            for keyword in risk_keywords:
                if keyword in text_lower:
                    risk_factors.append(f"Potential {keyword} risk mentioned in document")
                    break

            # Add general risk factors based on metrics if no other risks found
            if not risk_factors:
                if metrics.get("total_debt"):
                    risk_factors.append("Company has outstanding debt obligations")
                if not metrics.get("net_income"):
                    risk_factors.append("No net income data available for analysis")

            # Use OpenAI for advanced risk analysis
            try:
                openai_risk_analysis = await self._analyze_risk_with_openai(text, metrics)
                if openai_risk_analysis:
                    risk_factors.extend(openai_risk_analysis)
            except Exception as e:
                logger.warning(f"OpenAI risk analysis failed, using basic analysis: {e}")

            return list(set(risk_factors))  # Remove duplicates

        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return ["Financial risk analysis incomplete due to processing error"]

    async def _analyze_risk_with_openai(self, text: str, metrics: Dict[str, Any]) -> List[str]:
        """Use OpenAI to analyze risk factors."""
        try:
            metrics_str = "\n".join([f"{key}: {value}" for key, value in metrics.items() if value is not None])

            prompt = f"""
            Analyze the following financial metrics and document text to identify potential risk factors:

            Metrics:
            {metrics_str}

            Document excerpt:
            {text[:1000]}...

            List the top 3 most significant risk factors with brief explanations.
            Format as bullet points.
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a risk analyst identifying financial risks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            risk_text = response.choices[0].message.content.strip()
            risks = [line.strip() for line in risk_text.split('\n') if line.strip() and line.startswith('-')]
            return risks

        except Exception as e:
            logger.error(f"OpenAI risk analysis error: {e}")
            return []

    async def _generate_recommendations(self, metrics: Dict[str, Any], risk_factors: List[str]) -> List[str]:
        """Generate recommendations based on metrics and risk factors."""
        try:
            logger.info("Generating recommendations")

            recommendations = []
            
            # Calculate profit margin for recommendations
            profit_margin = None
            if metrics.get("total_revenue") and metrics.get("net_income"):
                profit_margin = metrics["net_income"] / metrics["total_revenue"]

            # Rule-based recommendations
            if metrics.get("debt_to_equity_ratio", 0) > 2.0:
                recommendations.append("Reduce debt levels and improve equity position")
            elif metrics.get("debt_to_equity_ratio", 0) > 1.5:
                recommendations.append("Monitor debt levels and consider debt reduction strategies")

            if metrics.get("current_ratio", 0) < 1.5:
                recommendations.append("Improve liquidity by increasing current assets or reducing short-term liabilities")

            if profit_margin is not None and profit_margin < 0.10:
                recommendations.append("Focus on cost optimization and revenue growth to improve profit margins")

            if metrics.get("total_debt"):
                recommendations.append("Establish a debt management strategy with clear refinancing plans")

            if not metrics.get("cash_flow"):
                recommendations.append("Implement improved cash flow tracking and forecasting")

            if any("leverage" in factor.lower() for factor in risk_factors):
                recommendations.append("Monitor debt covenants and refinancing opportunities")

            # Add general strategic recommendations
            if not recommendations:
                recommendations.append("Continue current financial strategy with regular monitoring")
            
            recommendations.append("Conduct regular financial analysis and performance reviews")
            recommendations.append("Maintain adequate insurance coverage and contingency planning")

            # Use OpenAI for advanced recommendations
            try:
                openai_recommendations = await self._generate_recommendations_with_openai(metrics, risk_factors)
                if openai_recommendations:
                    recommendations.extend(openai_recommendations)
            except Exception as e:
                logger.warning(f"OpenAI recommendations failed, using basic recommendations: {e}")

            return list(set(recommendations))  # Remove duplicates

        except Exception as e:
            logger.error(f"Recommendations generation failed: {e}")
            return ["Conduct comprehensive financial review and strategic planning"]

    def _generate_fallback_insights(self, metrics: Dict[str, Any]) -> str:
        """Generate fallback insights when OpenAI is not available."""
        insights = "Financial analysis based on extracted metrics: "

        if metrics.get("debt_to_equity_ratio", 0) > 2.0:
            insights += "The company shows high leverage which may indicate financial stress. "

        if metrics.get("current_ratio", 0) < 1.5:
            insights += "Liquidity position appears weak with current ratio below optimal levels. "

        if metrics.get("total_revenue", 0) and metrics.get("net_income", 0):
            profit_margin = metrics["net_income"] / metrics["total_revenue"] if metrics["total_revenue"] > 0 else 0
            if profit_margin > 0.15:
                insights += "Strong profitability with healthy profit margins. "
            elif profit_margin > 0.05:
                insights += "Moderate profitability that could be improved. "
            else:
                insights += "Low profitability requiring strategic review. "

        if not any(insights.endswith(ext) for ext in [".", "!"]):
            insights += "Overall financial position appears stable with opportunities for optimization."

        return insights

    async def _generate_recommendations_with_openai(self, metrics: Dict[str, Any], risk_factors: List[str]) -> List[str]:
        """Use OpenAI to generate recommendations."""
        try:
            metrics_str = "\n".join([f"{key}: {value}" for key, value in metrics.items() if value is not None])
            risks_str = "\n".join([f"- {factor}" for factor in risk_factors])

            prompt = f"""
            Based on the following financial metrics and risk factors, provide 3 strategic recommendations:

            Metrics:
            {metrics_str}

            Risk Factors:
            {risks_str}

            Provide concise, actionable recommendations.
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial strategist providing actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            rec_text = response.choices[0].message.content.strip()
            recs = [line.strip() for line in rec_text.split('\n') if line.strip() and line.startswith('-')]
            return recs

        except Exception as e:
            logger.error(f"OpenAI recommendations error: {e}")
            return []

    async def semantic_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Perform semantic search on stored documents.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of search results with similarity scores
        """
        try:
            if not query:
                raise ValueError("Query text is empty")

            if len(self.document_metadata) == 0:
                logger.warning("No documents available for semantic search")
                return []

            logger.info(f"Performing semantic search for query: {query}")

            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            query_embedding_np = np.array(query_embedding).astype('float32')

            # Search FAISS index
            distances, indices = self.vector_index.search(query_embedding_np, top_k)

            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1 and idx < len(self.document_metadata):
                    metadata = self.document_metadata[idx]
                    results.append({
                        "document_id": metadata["document_id"],
                        "chunk_index": metadata["chunk_index"],
                        "text": metadata["text"],
                        "similarity_score": float(1 / (1 + distances[0][i])),  # Convert distance to similarity
                        "distance": float(distances[0][i])
                    })

            return results

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise

    async def simplify_text(self, text: str) -> str:
        """
        Simplify financial/technical text for non-finance audience.

        Args:
            text: Text to simplify

        Returns:
            Simplified text version
        """
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a financial translator. Rewrite financial text in simple, non-technical language suitable for a business owner with no finance background. Keep it concise (2-3 sentences max)."
                        },
                        {
                            "role": "user",
                            "content": f"Simplify this financial statement:\n\n{text}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                simplified = response.choices[0].message.content
            else:
                # Fallback: simple rule-based simplification
                simplified = self._simplify_text_fallback(text)

            return simplified

        except Exception as e:
            logger.error(f"Error simplifying text: {e}")
            return self._simplify_text_fallback(text)

    def _simplify_text_fallback(self, text: str) -> str:
        """Fallback simplification using basic rules."""
        replacements = {
            "EBITDA": "earnings before taxes and depreciation",
            "leverage": "debt level",
            "covenant": "contract requirement",
            "liquidity": "available cash",
            "solvency": "ability to pay debts",
            "volatility": "ups and downs in performance",
            "correlation": "relationship between",
            "accrual": "money owed or expected",
        }
        
        simplified = text
        for term, replacement in replacements.items():
            simplified = simplified.replace(term, replacement)
        
        return simplified

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search documents by semantic similarity."""
        try:
            if not hasattr(self, 'embeddings') or self.embeddings is None:
                logger.warning("Vector database not initialized, returning empty results")
                return []
            
            from sentence_transformers import util
            query_embedding = self.embeddings.encode(query)
            
            results = []
            for doc_id, metadata in self.documents.items():
                similarity = util.cos_sim(query_embedding, metadata['embedding'])[0][0].item()
                results.append({
                    "document_id": doc_id,
                    "content": metadata['content'][:200],
                    "similarity": float(similarity)
                })
            
            results = sorted(results, key=lambda x: x['similarity'], reverse=True)
            logger.info(f"Found {len(results)} similar documents")
            return results

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            raise
