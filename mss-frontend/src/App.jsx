import React, { useState } from 'react';
import Layout from './components/Layout';
import FileUpload from './components/FileUpload';
import PDFViewer from './components/PDFViewer';
import AnalysisDashboard from './components/AnalysisDashboard';
import { Loader2 } from 'lucide-react';

function App() {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = (uploadedFile) => {
    setIsProcessing(true);
    // Simulate processing time
    setTimeout(() => {
      setFile(uploadedFile);
      setIsProcessing(false);
    }, 1500);
  };

  return (
    <Layout>
      <div className="h-full flex flex-col">
        {!file && !isProcessing && (
          <div className="flex-1 flex flex-col items-center justify-center fade-in">
            <div className="w-full max-w-4xl px-4">
              <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-slate-900 mb-2">
                  Financial Analysis <span className="text-indigo-600">Reimagined</span>
                </h1>
                <p className="text-lg text-slate-500">
                  Upload your credit memos and get instant AI-powered insights.
                </p>
              </div>
              <FileUpload onFileUpload={handleFileUpload} />
            </div>
          </div>
        )}

        {isProcessing && (
          <div className="flex-1 flex flex-col items-center justify-center animate-in fade-in zoom-in duration-300">
            <div className="text-center">
              <Loader2 className="w-16 h-16 text-indigo-600 animate-spin mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-800">Processing Document...</h3>
              <p className="text-slate-500">Extracting key financial metrics and risk factors.</p>
            </div>
          </div>
        )}

        {file && !isProcessing && (
          <div className="flex-1 flex flex-row gap-6 h-full p-2 overflow-hidden animate-in slide-in-from-bottom-4 duration-500">
            {/* Left Pane: PDF Viewer */}
            <div className="w-1/2 h-full min-w-[400px]">
              <PDFViewer file={file} />
            </div>

            {/* Right Pane: Analysis Dashboard */}
            <div className="w-1/2 h-full min-w-[400px] overflow-hidden">
              <AnalysisDashboard />
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

export default App;
