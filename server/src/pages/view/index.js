import React from 'react';
import {
    useParams,
} from 'react-router-dom';

import Viewer from '@/components/PDFViewer';
import './ViewPage.css'

export default () => {
    // TODO Check :cat/:subcat really exist, and render 404 if not
    const { cat, subcat } = useParams();
    return (
        <Viewer src={`/pdf/${cat}/${subcat}.pdf`} />
    )
}