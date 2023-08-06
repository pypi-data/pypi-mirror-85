import React from 'react';
import DocumentTitle from 'react-document-title';
var SentryDocumentTitle = function (props) {
    var _title = props.title + " - " + props.objSlug + " - Sentry";
    return <DocumentTitle title={_title}>{props.children}</DocumentTitle>;
};
export default SentryDocumentTitle;
//# sourceMappingURL=sentryDocumentTitle.jsx.map