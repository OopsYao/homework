import React from 'react';
import Viewer from '@phuocng/react-pdf-viewer';
import '@phuocng/react-pdf-viewer/cjs/react-pdf-viewer.css';
import { Worker } from '@phuocng/react-pdf-viewer';

export default function App() {
    return (
        <main>
            <Worker workerUrl="https://unpkg.com/pdfjs-dist@2.3.200/build/pdf.worker.min.js">
                <Viewer fileUrl="/pdf/SDE/hw5/main.pdf" />
            </Worker>
        </main>
    )
}