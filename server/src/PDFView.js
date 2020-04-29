import React from 'react';
import {
    useParams,
} from 'react-router-dom';

import '@phuocng/react-pdf-viewer/cjs/react-pdf-viewer.css';
import Viewer, { Worker } from '@phuocng/react-pdf-viewer';

export default function App() {
    const renderPage = props => {
        return (
            <>
                {props.svgLayer.children}
                {props.textLayer.children}
                {props.annotationLayer.children}
            </>
        );
    };
    const { cat, subcat } = useParams();
    return (
        <div>
            <Worker workerUrl="https://unpkg.com/pdfjs-dist@2.3.200/build/pdf.worker.min.js">
                <Viewer
                    fileUrl={`/pdf/${cat}/${subcat}.pdf`}
                    renderPage={renderPage} />
            </Worker>
        </div>
    )
}