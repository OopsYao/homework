import React from 'react';
import {
    useParams,
} from 'react-router-dom';

import '@phuocng/react-pdf-viewer/cjs/react-pdf-viewer.css';
import Viewer from '@phuocng/react-pdf-viewer';
import { Worker } from '@phuocng/react-pdf-viewer';

export default function App() {
    const { cat, subcat } = useParams();
    return (
        <div>
            <Worker workerUrl="https://unpkg.com/pdfjs-dist@2.3.200/build/pdf.worker.min.js">
                <Viewer fileUrl={`/pdf/${cat}/${subcat}.pdf`} />
            </Worker>
        </div>
    )
}