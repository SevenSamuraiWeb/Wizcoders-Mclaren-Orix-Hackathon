import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react';

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

const PDFViewer = ({ file }) => {
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);
    const [scale, setScale] = useState(1.0);

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }

    const changePage = (offset) => {
        setPageNumber(prevPageNumber => prevPageNumber + offset);
    }

    const previousPage = () => changePage(-1);
    const nextPage = () => changePage(1);

    return (
        <div className="flex flex-col h-full bg-slate-800 rounded-xl overflow-hidden shadow-lg border border-slate-700">
            {/* PDF Controls */}
            <div className="h-12 bg-slate-900 flex items-center justify-between px-4 border-b border-slate-700 text-slate-300">
                <div className="flex items-center space-x-2 text-sm">
                    <span>Page {pageNumber} of {numPages || '--'}</span>
                </div>

                <div className="flex items-center space-x-1">
                    <button
                        disabled={pageNumber <= 1}
                        onClick={previousPage}
                        className="p-1 hover:bg-slate-700 rounded disabled:opacity-30 disabled:hover:bg-transparent"
                    >
                        <ChevronLeft size={18} />
                    </button>
                    <button
                        disabled={pageNumber >= numPages}
                        onClick={nextPage}
                        className="p-1 hover:bg-slate-700 rounded disabled:opacity-30 disabled:hover:bg-transparent"
                    >
                        <ChevronRight size={18} />
                    </button>
                </div>

                <div className="flex items-center space-x-2">
                    <button
                        onClick={() => setScale(s => Math.max(0.5, s - 0.1))}
                        className="p-1 hover:bg-slate-700 rounded"
                    >
                        <ZoomOut size={18} />
                    </button>
                    <span className="text-xs w-10 text-center">{(scale * 100).toFixed(0)}%</span>
                    <button
                        onClick={() => setScale(s => Math.min(2.0, s + 0.1))}
                        className="p-1 hover:bg-slate-700 rounded"
                    >
                        <ZoomIn size={18} />
                    </button>
                </div>
            </div>

            {/* PDF Canvas */}
            <div className="flex-1 overflow-auto bg-slate-500/10 flex justify-center p-4">
                <Document
                    file={file}
                    onLoadSuccess={onDocumentLoadSuccess}
                    loading={<div className="text-white">Loading PDF...</div>}
                >
                    <Page
                        pageNumber={pageNumber}
                        scale={scale}
                        className="shadow-xl"
                        renderTextLayer={true}
                        renderAnnotationLayer={true}
                    />
                </Document>
            </div>
        </div>
    );
};

export default PDFViewer;
