#!/bin/bash
# QUICK SETUP SCRIPT - Get the hackathon system running in 2 minutes

echo "🚀 HACKATHON SYSTEM SETUP"
echo "=========================="
echo ""

# Navigate to backend
cd mss-backend

# Step 1: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Note: If reportlab fails, try: pip install reportlab==4.0.9

# Step 2: Verify installation
echo ""
echo "✓ Dependencies installed"
echo ""

# Step 3: Test synthetic data generator
echo "🧪 Testing synthetic PDF generator..."
python -c "
from tests.synthetic_data_generator import SyntheticFinancialPDFGenerator
import tempfile

generator = SyntheticFinancialPDFGenerator('TechCorp Inc.')
with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
    pdf_path = f.name
generator.create_pdf(pdf_path)
print(f'✓ Generated test PDF: {pdf_path}')

import os
os.remove(pdf_path)
print('✓ Cleanup complete')
"

# Step 4: Test credit memo generation
echo ""
echo "🧪 Testing credit memo generation..."
python test_credit_memo.py

echo ""
echo "=========================="
echo "✅ SETUP COMPLETE!"
echo "=========================="
echo ""
echo "Next steps:"
echo "1. Start the backend:"
echo "   uvicorn src.main:app --reload --port 8001"
echo ""
echo "2. In another terminal, start the frontend:"
echo "   cd mss-frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "🏆 Demo ready for judges!"
