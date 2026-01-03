@echo off
REM QUICK SETUP SCRIPT - Get the hackathon system running in 2 minutes (Windows)

echo.
echo 🚀 HACKATHON SYSTEM SETUP
echo ==========================
echo.

REM Navigate to backend
cd mss-backend

REM Step 1: Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Dependency installation failed
    echo Try: pip install reportlab==4.0.9 separately
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Step 2: Test synthetic data generator
echo 🧪 Testing synthetic PDF generator...
python -c ^
"from tests.synthetic_data_generator import SyntheticFinancialPDFGenerator; ^
import tempfile; ^
generator = SyntheticFinancialPDFGenerator('TechCorp Inc.'); ^
with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f: ^
    pdf_path = f.name; ^
generator.create_pdf(pdf_path); ^
print(f'✓ Generated test PDF: {pdf_path}'); ^
import os; ^
os.remove(pdf_path); ^
print('✓ Cleanup complete')"

if errorlevel 1 (
    echo ❌ Synthetic data generator test failed
    exit /b 1
)

REM Step 3: Test credit memo generation
echo.
echo 🧪 Testing credit memo generation...
python test_credit_memo.py

if errorlevel 1 (
    echo ❌ Credit memo test failed
    exit /b 1
)

echo.
echo ==========================
echo ✅ SETUP COMPLETE!
echo ==========================
echo.
echo Next steps:
echo 1. Start the backend:
echo    uvicorn src.main:app --reload --port 8001
echo.
echo 2. In another terminal, start the frontend:
echo    cd mss-frontend
echo    npm run dev
echo.
echo 3. Open http://localhost:5173 in your browser
echo.
echo 🏆 Demo ready for judges!
echo.
pause
