import React from 'react';
import {
    useParams,
} from 'react-router-dom';

import Viewer from './components/pdfviewer';
import './ViewPage.css'

export default function ViewPage() {
    const { cat, subcat } = useParams();
    return (
        <Viewer src={`/pdf/${cat}/${subcat}.pdf`} />
    )
}