/**
 * Export utilities for credit memo data
 */

/**
 * Generate Markdown summary from analysis data
 */
export const generateMarkdownSummary = (data) => {
    let markdown = "# Credit Memo Report\n\n";
    
    // Header info
    markdown += `**Document Type:** ${data.document_type || 'Financial Document'}\n`;
    markdown += `**Confidence Level:** ${data.metadata?.overall_confidence ? Math.round(data.metadata.overall_confidence * 100) + '%' : 'Draft'}\n\n`;
    
    // Executive Summary
    markdown += "## 1. Executive Summary\n\n";
    if (data.summary?.executive_summary) {
        markdown += data.summary.executive_summary + "\n\n";
    }
    if (data.summary?.key_takeaways && data.summary.key_takeaways.length > 0) {
        markdown += "**Key Takeaways:**\n";
        data.summary.key_takeaways.forEach(item => {
            markdown += `- ${item}\n`;
        });
        markdown += "\n";
    }
    
    // 5Cs Analysis
    if (data.credit_analysis_5cs) {
        markdown += "## 2. Credit Analysis (5Cs)\n\n";
        Object.entries(data.credit_analysis_5cs).forEach(([key, value]) => {
            markdown += `### ${key.toUpperCase()}\n`;
            markdown += value.analysis + "\n\n";
            if (value.highlights && value.highlights.length > 0) {
                markdown += "**Highlights:**\n";
                value.highlights.forEach(h => {
                    markdown += `- ${h}\n`;
                });
                markdown += "\n";
            }
        });
    }
    
    // Financial Metrics
    if (data.financial_metrics) {
        markdown += "## 3. Financial Metrics\n\n";
        data.financial_metrics.forEach(metric => {
            markdown += `- **${metric.name}:** ${metric.value}${metric.unit === '%' ? '%' : metric.unit === 'ratio' ? 'x' : ''} (${metric.status})\n`;
        });
        markdown += "\n";
    }
    
    // Risk Assessment
    if (data.risk_assessment) {
        markdown += "## 4. Risk Assessment\n\n";
        if (data.risk_assessment.red_flags && data.risk_assessment.red_flags.length > 0) {
            markdown += "**Red Flags:**\n";
            data.risk_assessment.red_flags.forEach(flag => {
                markdown += `- **${flag.issue}** (${flag.severity} Risk): ${flag.mitigant}\n`;
            });
            markdown += "\n";
        }
        
        if (data.risk_assessment.strengths && data.risk_assessment.strengths.length > 0) {
            markdown += "**Strengths:**\n";
            data.risk_assessment.strengths.forEach(s => {
                markdown += `- ${s.text}\n`;
            });
            markdown += "\n";
        }
        
        if (data.risk_assessment.weaknesses && data.risk_assessment.weaknesses.length > 0) {
            markdown += "**Weaknesses:**\n";
            data.risk_assessment.weaknesses.forEach(w => {
                markdown += `- ${w.text}\n`;
            });
            markdown += "\n";
        }
    }
    
    // Recommendation
    markdown += "## 5. Final Recommendation\n\n";
    markdown += `**Recommendation:** ${data.summary?.recommendation || 'Pending'}\n\n`;
    if (data.summary?.recommendation_justification) {
        markdown += `**Justification:** ${data.summary.recommendation_justification}\n`;
    }
    
    return markdown;
};

/**
 * Generate HTML table for Word document
 */
export const generateWordHTML = (data) => {
    let html = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #1e3a8a; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
            h2 { color: #374151; margin-top: 20px; border-bottom: 1px solid #e5e7eb; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            th, td { border: 1px solid #d1d5db; padding: 10px; text-align: left; }
            th { background-color: #f3f4f6; font-weight: bold; }
            .metric-value { font-weight: bold; color: #059669; }
            .risk-high { color: #dc2626; }
            .risk-medium { color: #f59e0b; }
            ul { margin: 10px 0; padding-left: 20px; }
            li { margin: 5px 0; }
            .recommendation { 
                padding: 15px; 
                border-radius: 5px; 
                margin: 15px 0;
            }
            .recommendation.positive { background-color: #dcfce7; color: #166534; }
            .recommendation.neutral { background-color: #fef3c7; color: #92400e; }
            .recommendation.negative { background-color: #fee2e2; color: #991b1b; }
        </style>
    </head>
    <body>
        <h1>Credit Memo Report</h1>
        <p><strong>Document Type:</strong> ${data.document_type || 'Financial Document'}</p>
        <p><strong>Confidence Level:</strong> ${data.metadata?.overall_confidence ? Math.round(data.metadata.overall_confidence * 100) + '%' : 'Draft'}</p>
    `;
    
    // Executive Summary
    html += `<h2>1. Executive Summary</h2>`;
    if (data.summary?.executive_summary) {
        html += `<p>${data.summary.executive_summary}</p>`;
    }
    if (data.summary?.key_takeaways && data.summary.key_takeaways.length > 0) {
        html += `<h3>Key Takeaways</h3><ul>`;
        data.summary.key_takeaways.forEach(item => {
            html += `<li>${item}</li>`;
        });
        html += `</ul>`;
    }
    
    // 5Cs Analysis
    if (data.credit_analysis_5cs) {
        html += `<h2>2. Credit Analysis (5Cs)</h2>`;
        Object.entries(data.credit_analysis_5cs).forEach(([key, value]) => {
            html += `<h3>${key.toUpperCase()}</h3>`;
            html += `<p>${value.analysis}</p>`;
            if (value.highlights && value.highlights.length > 0) {
                html += `<ul>`;
                value.highlights.forEach(h => {
                    html += `<li>${h}</li>`;
                });
                html += `</ul>`;
            }
        });
    }
    
    // Financial Metrics
    if (data.financial_metrics && data.financial_metrics.length > 0) {
        html += `<h2>3. Financial Metrics</h2>`;
        html += `<table><tr><th>Metric</th><th>Value</th><th>Status</th></tr>`;
        data.financial_metrics.forEach(metric => {
            const statusClass = metric.status === 'healthy' ? 'metric-value' : 'risk-medium';
            html += `<tr><td>${metric.name}</td><td class="${statusClass}">${metric.value}${metric.unit === '%' ? '%' : metric.unit === 'ratio' ? 'x' : ''}</td><td>${metric.status}</td></tr>`;
        });
        html += `</table>`;
    }
    
    // Risk Assessment
    if (data.risk_assessment) {
        html += `<h2>4. Risk Assessment</h2>`;
        if (data.risk_assessment.red_flags && data.risk_assessment.red_flags.length > 0) {
            html += `<h3>Red Flags</h3><ul>`;
            data.risk_assessment.red_flags.forEach(flag => {
                const riskClass = flag.severity === 'High' ? 'risk-high' : 'risk-medium';
                html += `<li><strong class="${riskClass}">${flag.issue}</strong> (${flag.severity}): ${flag.mitigant}</li>`;
            });
            html += `</ul>`;
        }
        
        if (data.risk_assessment.strengths && data.risk_assessment.strengths.length > 0) {
            html += `<h3>Strengths</h3><ul>`;
            data.risk_assessment.strengths.forEach(s => {
                html += `<li>${s.text}</li>`;
            });
            html += `</ul>`;
        }
        
        if (data.risk_assessment.weaknesses && data.risk_assessment.weaknesses.length > 0) {
            html += `<h3>Weaknesses</h3><ul>`;
            data.risk_assessment.weaknesses.forEach(w => {
                html += `<li>${w.text}</li>`;
            });
            html += `</ul>`;
        }
    }
    
    // Recommendation
    const recommendation = data.summary?.recommendation || 'Pending';
    const recClass = recommendation === 'Approve' || recommendation === 'Positive' ? 'positive' : 
                     recommendation === 'Conditional Approval' || recommendation === 'Neutral' ? 'neutral' : 'negative';
    html += `<div class="recommendation ${recClass}">
        <h2>5. Final Recommendation</h2>
        <p><strong>Recommendation:</strong> ${recommendation}</p>
        ${data.summary?.recommendation_justification ? `<p><strong>Justification:</strong> ${data.summary.recommendation_justification}</p>` : ''}
    </div>`;
    
    html += `</body></html>`;
    return html;
};

/**
 * Convert HTML to formatted text for markdown/plain text export
 */
export const htmlToText = (html) => {
    const tmp = document.createElement('DIV');
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || '';
};

/**
 * Download content as file
 */
export const downloadFile = (content, filename, mimeType) => {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
};

/**
 * Download as Word document (using html2pdf or similar)
 */
export const downloadAsWord = (data, filename = 'credit_memo.doc') => {
    const html = generateWordHTML(data);
    const blob = new Blob([html], { type: 'application/msword' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
};

/**
 * Simplify text using backend API
 */
export const simplifyText = async (text, apiKey) => {
    try {
        const response = await fetch('/api/simplify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error('Failed to simplify text');
        }
        
        const data = await response.json();
        return data.simplified_text || text;
    } catch (error) {
        console.error('Simplify error:', error);
        return text;
    }
};
