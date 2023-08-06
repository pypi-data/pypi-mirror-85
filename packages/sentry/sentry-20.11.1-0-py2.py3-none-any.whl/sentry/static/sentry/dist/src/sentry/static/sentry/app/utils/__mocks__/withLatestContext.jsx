import { __extends } from "tslib";
import React from 'react';
var MOCK_ORG = TestStubs.Organization();
var DEFAULTS = {
    organization: MOCK_ORG,
    organizations: [MOCK_ORG],
    project: TestStubs.Project(),
    lastRoute: {},
};
var withLatestContextMock = function (WrappedComponent) {
    return /** @class */ (function (_super) {
        __extends(WithLatestContextMockWrapper, _super);
        function WithLatestContextMockWrapper() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        WithLatestContextMockWrapper.prototype.render = function () {
            return <WrappedComponent {...DEFAULTS} {...this.props}/>;
        };
        return WithLatestContextMockWrapper;
    }(React.Component));
};
export default withLatestContextMock;
//# sourceMappingURL=withLatestContext.jsx.map