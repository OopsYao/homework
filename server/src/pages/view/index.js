import React from 'react';
import {
    withRouter
} from 'react-router-dom';

import Viewer from '@/components/PDFViewer';
import './ViewPage.css'

class View extends React.Component {
    constructor() {
        super()
        this.state = { docAvailable: false }
    }
    handleRes(res) {
        if (res.ok) {
            this.setState({ docAvailable: true })
        } else {
            import('@/pages/404').then(md => {
                this.setState({ md })
            })
        }
    }
    componentDidMount() {
        const { url } = this.props.match;
        fetch(`/pdf${url}.pdf`, { method: 'HEAD' })
            .then(this.handleRes.bind(this))
    }
    render() {
        // TODO How to get :cat and :subcat
        const { url } = this.props.match;
        if (this.state.docAvailable) {
            return <Viewer src={`/pdf${url}.pdf`} />
        } else if (this.state.md) {
            // TODO Ask myself? What is default
            // TODO and the dynamic takes effect? (can be replaced by import)
            return React.createElement(this.state.md.default)
        } else {
            return <div />
        }
    }
}
export default withRouter(View);