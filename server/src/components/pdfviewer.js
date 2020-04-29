import React from 'react';

export default class PDFViewer extends React.Component {
  constructor(props) {
    super(props);
    this.viewerRef = React.createRef();
  }

  mountIFrame(source, element) {
    const iframe = document.createElement('iframe');

    iframe.src = `/pdfjs/web/viewer.html?file=${source}`;
    iframe.width = '100%';
    iframe.height = '100%';

    element.appendChild(iframe);
  }

  componentDidMount() {
    const { src } = this.props;
    console.log(src)
    const element = this.viewerRef.current;

    this.mountIFrame(src, element);
  }


  render() {
    return (
      <div ref={this.viewerRef} id='viewer' style={{ width: '100%', height: '100%' }}>
      </div>
    )
  }
}