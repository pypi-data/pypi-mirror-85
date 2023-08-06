import { __extends } from "tslib";
import DocumentTitle from 'react-document-title';
import React from 'react';
import AsyncComponent from 'app/components/asyncComponent';
var AsyncView = /** @class */ (function (_super) {
    __extends(AsyncView, _super);
    function AsyncView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AsyncView.prototype.getTitle = function () {
        return '';
    };
    AsyncView.prototype.render = function () {
        var title = this.getTitle();
        return (<DocumentTitle title={(title ? title + " - " : '') + "Sentry"}>
        {this.renderComponent()}
      </DocumentTitle>);
    };
    return AsyncView;
}(AsyncComponent));
export default AsyncView;
//# sourceMappingURL=asyncView.jsx.map