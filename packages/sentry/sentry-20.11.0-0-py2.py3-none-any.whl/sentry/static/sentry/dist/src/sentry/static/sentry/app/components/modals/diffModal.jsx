import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import IssueDiff from 'app/components/issueDiff';
var DiffModal = function (_a) {
    var className = _a.className, Body = _a.Body, props = __rest(_a, ["className", "Body"]);
    return (<Body>
    <IssueDiff className={className} {...props}/>
  </Body>);
};
var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .modal-dialog {\n    display: flex;\n    margin: 0;\n    left: 10px;\n    right: 10px;\n    top: 10px;\n    bottom: 10px;\n    width: auto;\n  }\n  .modal-content {\n    display: flex;\n    flex: 1;\n  }\n  .modal-body {\n    display: flex;\n    overflow: hidden;\n    flex: 1;\n  }\n"], ["\n  .modal-dialog {\n    display: flex;\n    margin: 0;\n    left: 10px;\n    right: 10px;\n    top: 10px;\n    bottom: 10px;\n    width: auto;\n  }\n  .modal-content {\n    display: flex;\n    flex: 1;\n  }\n  .modal-body {\n    display: flex;\n    overflow: hidden;\n    flex: 1;\n  }\n"])));
export { modalCss };
export default DiffModal;
var templateObject_1;
//# sourceMappingURL=diffModal.jsx.map