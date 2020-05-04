import React from 'react';
import { Link } from 'react-router-dom';

export default () => {
    const items = []
    for (const cat in DOC_TREE) {
        for (let subcat of DOC_TREE[cat]) {
            items.push(<li key={`${cat}/${subcat}`}>
                <Link to={`/${cat}/${subcat}`}>{cat} {subcat}</Link>
            </li>)
        }
    }
    return (
        <ul>{items}</ul>
    )
}