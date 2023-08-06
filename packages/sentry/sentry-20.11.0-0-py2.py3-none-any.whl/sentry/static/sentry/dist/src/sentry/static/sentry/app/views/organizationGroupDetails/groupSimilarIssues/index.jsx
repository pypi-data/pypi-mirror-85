import { __rest } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import SimilarStackTrace from './similarStackTrace';
var GroupSimilarIssues = function (_a) {
    var project = _a.project, props = __rest(_a, ["project"]);
    return (<Feature features={['similarity-view']} project={project}>
    <SimilarStackTrace project={project} {...props}/>
  </Feature>);
};
export default GroupSimilarIssues;
//# sourceMappingURL=index.jsx.map