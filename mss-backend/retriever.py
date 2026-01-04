from vector_store import PageVectorStore

class ContextRetriever:
    """
    Retrieves context for specific sections of such as Executive Summary, Risks, etc.
    """
    def __init__(self, vector_store: PageVectorStore):
        self.vector_store = vector_store
    
    def retrieve_context(self, section_name: str):
        """
        Retrieves relevant pages and text context for a given section.
        
        Args:
            section_name (str): The section to retrieve context for.
            
        Returns:
            dict: query result with 'pages' and 'context_text'
        """
        query_map = {
            "executive_summary": "overall performance revenue profitability cash flow",
            "financial_metrics": "revenue EBITDA net profit balance sheet",
            "cash_flow_analysis": "cash flow operating investing financing",
            "risks": "risks borrowings liabilities contingencies",
            "recommendation": "financial position repayment capacity"
        }
        
        query = query_map.get(section_name, "")
        if not query:
            return {"pages": [], "context_text": ""}
            
        results = self.vector_store.search(query, top_k=3)
        
        if not results:
             return {"pages": [], "context_text": ""}
        
        # Aggregate unique pages and combined text
        pages = sorted(list(set(r['page'] for r in results)))
        context_text = "\n\n".join([f"--- Page {r['page']} ---\n{r['text']}" for r in results])
        
        return {
            "pages": pages,
            "context_text": context_text
        }
