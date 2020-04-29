import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import PDFView from './PDFView';
// import 'normalize.css';

export default function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/">
                    <Home />
                </Route>
                <Route path="/:cat/:subcat" children={<PDFView />} />
            </Switch>
        </Router>
    )
}

function Home() {
    return (
        <ul>
            <li>
                <Link to="/SDE/hw5">SDE HW5</Link>
            </li>
            <li>
                <Link to="/SDE/hw6">SDE HW6</Link>
            </li>
            <li>
                <Link to="/SDE/hw7">SDE HW7</Link>
            </li>
        </ul>
    )
}