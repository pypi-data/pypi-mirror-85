import { __extends } from "tslib";
import React from 'react';
import SettingsBreadcrumbActions from 'app/actions/settingsBreadcrumbActions';
var BreadcrumbTitle = /** @class */ (function (_super) {
    __extends(BreadcrumbTitle, _super);
    function BreadcrumbTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BreadcrumbTitle.prototype.componentDidMount = function () {
        SettingsBreadcrumbActions.mapTitle(this.props);
    };
    BreadcrumbTitle.prototype.render = function () {
        return null;
    };
    return BreadcrumbTitle;
}(React.Component));
export default BreadcrumbTitle;
//# sourceMappingURL=breadcrumbTitle.jsx.map