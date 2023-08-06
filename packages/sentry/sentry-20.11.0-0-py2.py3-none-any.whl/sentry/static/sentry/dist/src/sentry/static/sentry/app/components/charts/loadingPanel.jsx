import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LoadingMask from 'app/components/loadingMask';
var LoadingPanel = styled(function (_a) {
    var _height = _a.height, props = __rest(_a, ["height"]);
    return (<div {...props}>
    <LoadingMask />
  </div>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  flex-shrink: 0;\n  overflow: hidden;\n  height: ", ";\n  position: relative;\n  border-color: transparent;\n  margin-bottom: 0;\n"], ["\n  flex: 1;\n  flex-shrink: 0;\n  overflow: hidden;\n  height: ", ";\n  position: relative;\n  border-color: transparent;\n  margin-bottom: 0;\n"])), function (p) { return p.height; });
LoadingPanel.defaultProps = {
    height: '200px',
};
export default LoadingPanel;
var templateObject_1;
//# sourceMappingURL=loadingPanel.jsx.map