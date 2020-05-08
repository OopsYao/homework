import React from 'react';
import { Link } from 'react-router-dom';

export default () => {
    document.title = 'Oops 404';
    return (
        <div>
            <p>This is a 404 page.</p>
            <Link to='/'>Back to home</Link>
        </div>
    )
}