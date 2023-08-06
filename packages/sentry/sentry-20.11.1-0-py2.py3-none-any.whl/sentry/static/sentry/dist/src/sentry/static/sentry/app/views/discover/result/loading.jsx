import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LoadingIndicator from 'app/components/loadingIndicator';
import { LoadingContainer } from '../styles';
var Loading = /** @class */ (function (_super) {
    __extends(Loading, _super);
    function Loading() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Loading.prototype.render = function () {
        return (<Background>
        <LoadingContainer>
          <LoadingIndicator />
        </LoadingContainer>
      </Background>);
    };
    return Loading;
}(React.Component));
export default Loading;
export var Background = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  left: 0;\n  right: 0;\n  top: 0;\n  bottom: 0;\n  background-color: rgba(250, 249, 251, 0.7);\n"], ["\n  position: absolute;\n  left: 0;\n  right: 0;\n  top: 0;\n  bottom: 0;\n  background-color: rgba(250, 249, 251, 0.7);\n"])));
var templateObject_1;
//# sourceMappingURL=loading.jsx.map