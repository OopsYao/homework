import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";

// import PDFView from './PDFView';
// import 'normalize.css';
import Home from '@/pages/home';
import ViewPage from '@/pages/view';
import NoMatch from '@/pages/404';

export default function App() {
    return (
        <Router>
            <Switch>
                <Route exact path='/'>
                    <Home />
                </Route>
                <Route path='/:cat/:subcat' children={<ViewPage />} />
                <Route path='*'>
                    <NoMatch />
                </Route>
            </Switch>
        </Router>
    )
}
