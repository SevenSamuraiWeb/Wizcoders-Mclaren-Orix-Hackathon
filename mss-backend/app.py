import streamlit as st
import time
import os
import json
from dotenv import load_dotenv
from groq import Groq
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO

# Backend Classes
from pdf_processor import PDFProcessor
from vector_store import PageVectorStore
from retriever import ContextRetriever
from credit_memo_generator import CreditMemoGenerator

# Load environment variables
load_dotenv()


def generate_markdown_summary(memo):
    """Convert memo to markdown format."""
    sections = memo.get("sections", {})
    markdown = f"# Credit Memo Report\n\n"
    markdown += f"**Document Type:** {memo.get('document_type', 'N/A')}\n"
    markdown += f"**Confidence Level:** {memo.get('confidence_level', 'Draft')}\n\n"
    
    # Executive Summary
    markdown += "## 1. Executive Summary\n\n"
    exec_sum = sections.get("executive_summary", {})
    for item in exec_sum.get("highlights", []):
        point = item.get("point", "")
        attr = item.get("attribute", "")
        sources = item.get("sources", [])
        source_str = f" _(Pages: {', '.join(map(str, sources))})_" if sources else ""
        markdown += f"- **{attr}:** {point}{source_str}\n"
    
    markdown += "\n## 2. Key Financial Metrics\n\n"
    fin_metrics = sections.get("financial_metrics", {})
    for m in fin_metrics.get("metrics", []):
        name = m.get("name", "")
        value = m.get("value", "N/A")
        confidence = m.get("confidence", "")
        markdown += f"- **{name}:** {value} ({confidence})\n"
    
    markdown += "\n## 3. Risk Assessment\n\n"
    risks = sections.get("risks", {})
    for risk in risks.get("items", []):
        title = risk.get("risk_title", "")
        severity = risk.get("severity", "")
        desc = risk.get("description", "")
        markdown += f"### {title} ({severity})\n{desc}\n\n"
    
    markdown += "\n## 4. Final Recommendation\n\n"
    rec = sections.get("recommendation", {})
    stance = rec.get("stance", "")
    summary = rec.get("summary", "")
    markdown += f"**Stance:** {stance}\n\n{summary}\n\n"
    markdown += "**Justification:**\n"
    for j in rec.get("justification", []):
        markdown += f"- {j.get('point', '')}\n"
    
    return markdown


def generate_word_document(memo):
    """Convert memo to Word document format."""
    doc = Document()
    
    # Title
    title = doc.add_heading('Credit Memo Report', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Metadata
    doc.add_paragraph(f"Document Type: {memo.get('document_type', 'N/A')}")
    doc.add_paragraph(f"Confidence Level: {memo.get('confidence_level', 'Draft')}")
    doc.add_paragraph()
    
    sections = memo.get("sections", {})
    
    # Executive Summary
    doc.add_heading('1. Executive Summary', level=1)
    exec_sum = sections.get("executive_summary", {})
    for item in exec_sum.get("highlights", []):
        point = item.get("point", "")
        attr = item.get("attribute", "")
        sources = item.get("sources", [])
        source_str = f" (Pages: {', '.join(map(str, sources))})" if sources else ""
        p = doc.add_paragraph(f"{attr}: {point}{source_str}", style='List Bullet')
    
    # Key Financial Metrics
    doc.add_heading('2. Key Financial Metrics', level=1)
    fin_metrics = sections.get("financial_metrics", {})
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Metric'
    hdr_cells[1].text = 'Value'
    hdr_cells[2].text = 'Confidence'
    
    for m in fin_metrics.get("metrics", []):
        row_cells = table.add_row().cells
        row_cells[0].text = m.get("name", "")
        row_cells[1].text = str(m.get("value", "N/A"))
        row_cells[2].text = m.get("confidence", "")
    
    # Risk Assessment
    doc.add_heading('3. Risk Assessment', level=1)
    risks = sections.get("risks", {})
    for risk in risks.get("items", []):
        title = risk.get("risk_title", "")
        severity = risk.get("severity", "")
        desc = risk.get("description", "")
        doc.add_heading(f"{title} ({severity})", level=2)
        doc.add_paragraph(desc)
    
    # Recommendation
    doc.add_heading('4. Final Recommendation', level=1)
    rec = sections.get("recommendation", {})
    stance = rec.get("stance", "")
    summary = rec.get("summary", "")
    doc.add_paragraph(f"Stance: {stance}").bold = True
    doc.add_paragraph(summary)
    doc.add_heading('Justification:', level=2)
    for j in rec.get("justification", []):
        doc.add_paragraph(j.get('point', ''), style='List Bullet')
    
    return doc


def simplify_text(text, api_key):
    """Simplify text using Groq API."""
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional writer. Simplify the given text while maintaining all important information. Use simpler vocabulary and shorter sentences. Make it easy to understand for non-technical readers."
                },
                {
                    "role": "user",
                    "content": f"Please simplify this text:\n\n{text}"
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.5,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error simplifying text: {str(e)}"

    # 1. Page Configuration
    st.set_page_config(
        page_title="Auto-Credit Memo Generator",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for "Nice" UI
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E3A8A;
            font-weight: 700;
        }
        .section-header {
            font-size: 1.5rem;
            color: #1F2937;
            border-bottom: 2px solid #E5E7EB;
            padding-bottom: 0.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: #F3F4F6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3B82F6;
        }
        .risk-card-high {
            background-color: #FEF2F2;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #FCA5A5;
            margin-bottom: 0.5rem;
        }
        .risk-card-medium {
            background-color: #FFFBEB;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #FCD34D;
            margin-bottom: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Header / Title
    st.markdown('<p class="main-header">📄 AI-Powered Credit Memo Generator</p>', unsafe_allow_html=True)
    st.markdown("Upload a financial statement (PDF) to generate a structured, professional credit memo.")

    # 3. Sidebar for Inputs
    with st.sidebar:
        st.header("Configuration")
        
        # API Key handling
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            api_key = st.text_input("Enter Groq API Key", type="password")
            
        uploaded_file = st.file_uploader("Upload Financial Report (PDF)", type=["pdf"])
        
        st.info("System Status: Ready")
        if uploaded_file:
            st.success("PDF Loaded")

    # 4. Main Area Logic
    if uploaded_file is not None and api_key:
        
        # Initialize session state for generation
        if "memo" not in st.session_state:
            st.session_state.memo = None

        # 5. Generate Button
        if st.button("Generate Credit Memo", type="primary"):
            try:
                with st.spinner("Processing PDF and generating insights... (This may take ~30s)"):
                    # A. Parsing
                    status_text = st.empty()
                    status_text.text("Parsing PDF contents...")
                    bytes_data = uploaded_file.getvalue()
                    processor = PDFProcessor(bytes_data)
                    extracted_data = processor.parse()
                    
                    # B. Vector Indexing
                    status_text.text("Building semantic index...")
                    vector_store = PageVectorStore()
                    vector_store.add_pages(extracted_data)
                    
                    # C. Retrieval & Generation
                    status_text.text("Analyzing sections with AI...")
                    retriever = ContextRetriever(vector_store)
                    client = Groq(api_key=api_key)
                    # Using the specific model as verified
                    generator = CreditMemoGenerator(retriever, client, model_name="meta-llama/llama-4-scout-17b-16e-instruct")
                    
                    # Generate full memo
                    memo = generator.generate_credit_memo()
                    st.session_state.memo = memo
                    
                    status_text.empty()
                    st.toast("Credit Memo Generated Successfully!", icon="✅")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

        # 6. Display Results if generated
        if st.session_state.memo:
            memo = st.session_state.memo
            st.divider()
            
            # --- Header Info ---
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Document Type:** {memo.get('document_type', 'N/A')}")
            with c2:
                st.markdown(f"**Confidence:** `{memo.get('confidence_level', 'Draft')}`")

            sections = memo.get("sections", {})

            # --- Section 1: Executive Summary ---
            st.markdown('<div class="section-header">1. Executive Summary</div>', unsafe_allow_html=True)
            exec_sum = sections.get("executive_summary", {})
            highlights = exec_sum.get("highlights", [])
            
            for item in highlights:
                point = item.get("point", "")
                attr = item.get("attribute", "General")
                sources = item.get("sources", [])
                source_str = f" (Page {', '.join(map(str, sources))})" if sources else ""
                
                st.markdown(f"""
                <div style="margin-bottom: 8px;">
                    <span style="background-color: #E0F2FE; color: #0369A1; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; font-weight: 600;">{attr}</span>
                    {point} <span style="color: #6B7280; font-size: 0.9em;">{source_str}</span>
                </div>
                """, unsafe_allow_html=True)

            # --- Section 2: Key Financial Metrics ---
            st.markdown('<div class="section-header">2. Key Financial Metrics (FY24)</div>', unsafe_allow_html=True)
            fin_metrics = sections.get("financial_metrics", {})
            metrics_list = fin_metrics.get("metrics", [])
            
            # Display in rows of 3
            cols = st.columns(3)
            for i, m in enumerate(metrics_list):
                with cols[i % 3]:
                    st.metric(
                        label=m.get("name", "Metric"),
                        value=str(m.get("value", "N/A")),
                        delta=f"Conf: {m.get('confidence', 'N/A')}",
                        delta_color="off"
                    )
            
            # --- Section 3: Risk Assessment ---
            st.markdown('<div class="section-header">3. Risk Assessment</div>', unsafe_allow_html=True)
            risks = sections.get("risks", {})
            risk_items = risks.get("items", [])
            
            for risk in risk_items:
                severity = risk.get("severity", "Medium")
                title = risk.get("risk_title", "Risk")
                desc = risk.get("description", "")
                r_type = risk.get("risk_type", "General")
                
                css_class = "risk-card-high" if severity == "High" else "risk-card-medium"
                icon = "🔴" if severity == "High" else "⚠️"
                
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{icon} {title}</strong> <span style="color: #6B7280;">({r_type})</span><br>
                    {desc}
                </div>
                """, unsafe_allow_html=True)

            # --- Section 4: Recommendation ---
            st.markdown('<div class="section-header">4. Final Recommendation</div>', unsafe_allow_html=True)
            rec = sections.get("recommendation", {})
            stance = rec.get("stance", "Neutral")
            summary = rec.get("summary", "")
            
            if stance == "Positive":
                st.success(f"**Recommendation: {stance}**\n\n{summary}")
            elif stance == "Negative":
                st.error(f"**Recommendation: {stance}**\n\n{summary}")
            else:
                st.warning(f"**Recommendation: {stance}**\n\n{summary}")
                
            # Justification
            st.markdown("**Basis for Recommendation:**")
            for j in rec.get("justification", []):
                st.markdown(f"- {j.get('point', '')}")

            # --- Export and Edit Section ---
            st.divider()
            st.markdown('<div class="section-header">📝 Edit & Export</div>', unsafe_allow_html=True)
            
            # Create columns for buttons and text area
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📄 Download as Markdown", use_container_width=True):
                    md_content = generate_markdown_summary(memo)
                    st.download_button(
                        label="📥 Save Markdown",
                        data=md_content,
                        file_name="credit_memo.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            
            with col2:
                if st.button("📋 Download as Word", use_container_width=True):
                    doc = generate_word_document(memo)
                    doc_buffer = BytesIO()
                    doc.save(doc_buffer)
                    doc_buffer.seek(0)
                    st.download_button(
                        label="📥 Save Word",
                        data=doc_buffer.getvalue(),
                        file_name="credit_memo.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            
            with col3:
                if st.button("✨ Simplify Content", use_container_width=True):
                    if "simplified_memo" not in st.session_state:
                        st.session_state.simplified_memo = None
                    
                    with st.spinner("Simplifying content..."):
                        # Simplify each section
                        simplified = memo.copy()
                        simplified_sections = {}
                        
                        for section_name, section_data in sections.items():
                            if isinstance(section_data, dict):
                                simplified_section = {}
                                for key, value in section_data.items():
                                    if isinstance(value, str) and len(value) > 50:
                                        simplified_section[key] = simplify_text(value, api_key)
                                    elif isinstance(value, list):
                                        simplified_section[key] = value
                                    else:
                                        simplified_section[key] = value
                                simplified_sections[section_name] = simplified_section
                        
                        simplified["sections"] = simplified_sections
                        st.session_state.simplified_memo = simplified
                        st.success("Content simplified! View below ⬇️")
            
            with col4:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.simplified_memo = None
                    st.rerun()
            
            # Show simplified version if available
            if st.session_state.get("simplified_memo"):
                st.info("ℹ️ Showing simplified version")
                memo = st.session_state.simplified_memo
                sections = memo.get("sections", {})
            
            # Text editing area
            st.markdown("#### ✏️ Edit Summary")
            st.info("You can edit the generated content below and then export it.")
            
            # Create editable text areas for each section
            edited_content = {}
            
            # Executive Summary Editor
            with st.expander("Edit Executive Summary", expanded=False):
                exec_sum = sections.get("executive_summary", {})
                current_text = "\n".join([f"- {item.get('point', '')}" for item in exec_sum.get("highlights", [])])
                edited_content["executive_summary"] = st.text_area("Executive Summary Points:", value=current_text, height=150, key="exec_edit")
            
            # Financial Metrics Editor
            with st.expander("Edit Financial Metrics", expanded=False):
                fin_metrics = sections.get("financial_metrics", {})
                current_text = "\n".join([f"{m.get('name', '')}: {m.get('value', 'N/A')}" for m in fin_metrics.get("metrics", [])])
                edited_content["financial_metrics"] = st.text_area("Financial Metrics:", value=current_text, height=150, key="metrics_edit")
            
            # Risks Editor
            with st.expander("Edit Risk Assessment", expanded=False):
                risks = sections.get("risks", {})
                current_text = "\n".join([f"{risk.get('risk_title', '')} ({risk.get('severity', '')}): {risk.get('description', '')}" for risk in risks.get("items", [])])
                edited_content["risks"] = st.text_area("Risk Assessment:", value=current_text, height=150, key="risks_edit")
            
            # Recommendation Editor
            with st.expander("Edit Recommendation", expanded=False):
                rec = sections.get("recommendation", {})
                current_text = f"{rec.get('stance', '')}\n\n{rec.get('summary', '')}"
                edited_content["recommendation"] = st.text_area("Recommendation:", value=current_text, height=150, key="rec_edit")
            
            # Export edited content
            st.markdown("#### 📥 Export Edited Content")
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                if st.button("Save as Markdown (with edits)", use_container_width=True):
                    edited_md = "# Credit Memo Report (Edited)\n\n"
                    edited_md += f"**Document Type:** {memo.get('document_type', 'N/A')}\n\n"
                    for section_name, content in edited_content.items():
                        if content:
                            edited_md += f"## {section_name.replace('_', ' ').title()}\n{content}\n\n"
                    
                    st.download_button(
                        label="📥 Download Edited Markdown",
                        data=edited_md,
                        file_name="credit_memo_edited.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            
            with export_col2:
                if st.button("Save as Word (with edits)", use_container_width=True):
                    doc = Document()
                    title = doc.add_heading('Credit Memo Report (Edited)', 0)
                    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    for section_name, content in edited_content.items():
                        if content:
                            doc.add_heading(section_name.replace('_', ' ').title(), level=1)
                            doc.add_paragraph(content)
                    
                    doc_buffer = BytesIO()
                    doc.save(doc_buffer)
                    doc_buffer.seek(0)
                    
                    st.download_button(
                        label="📥 Download Edited Word",
                        data=doc_buffer.getvalue(),
                        file_name="credit_memo_edited.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

            # --- Raw Data Expander ---
            with st.expander("View Raw JSON Output"):
                st.json(memo)

    elif not api_key:
        st.warning("Please provide a Groq API Key in the sidebar or .env file to proceed.")
    else:
        st.info("👈 Please upload a PDF document to begin.")

if __name__ == "__main__":
    main()
