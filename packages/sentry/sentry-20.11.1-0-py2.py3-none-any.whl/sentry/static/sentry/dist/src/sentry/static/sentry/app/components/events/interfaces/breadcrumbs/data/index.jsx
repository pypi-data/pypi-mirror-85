import React from 'react';
import Default from './default';
import Exception from './exception';
import Http from './http';
import { BreadcrumbType } from '../types';
var Data = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId, searchTerm = _a.searchTerm;
    if (breadcrumb.type === BreadcrumbType.HTTP) {
        return <Http breadcrumb={breadcrumb} searchTerm={searchTerm}/>;
    }
    if (breadcrumb.type === BreadcrumbType.WARNING ||
        breadcrumb.type === BreadcrumbType.ERROR) {
        return <Exception breadcrumb={breadcrumb} searchTerm={searchTerm}/>;
    }
    return (<Default event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm}/>);
};
export default Data;
//# sourceMappingURL=index.jsx.map