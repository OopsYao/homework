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
    componentDidMount() {
        // TODO use cat and subcat
        const { url } = this.props.match;
        import(`~/pdf${url}.pdf`).then(url => {
            console.log(`PDF url: ${JSON.stringify(url)}`)
            this.setState({ doc: url.default })
        }).catch(_ => {
            this.setState({ doc: null })
            import('@/pages/404').then(md => {
                this.setState({ view404: md.default })
            })
        })
    }
    render() {
        if (this.state.doc) {
            return <Viewer src={`/${this.state.doc}`} />
        } else if (this.state.doc === null && this.state.view404) {
            return React.createElement(this.state.view404)
        } else {
            return <div />
        }
    }
}
export default withRouter(View);