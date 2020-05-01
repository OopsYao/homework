import React from 'react';
import { Link } from 'react-router-dom';

export default () => (
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
        <li>
            <Link to="/st-cal/wk8">金随 W8</Link>
        </li>
        <li>
            <Link to="/st-cal/wk9">金随 W9</Link>
        </li>
        <li>
            <Link to="/tsa/hw8">时序 H8</Link>
        </li>
        <li>
            <Link to="/tsa/hw9">时序 H9</Link>
        </li>
    </ul>
)