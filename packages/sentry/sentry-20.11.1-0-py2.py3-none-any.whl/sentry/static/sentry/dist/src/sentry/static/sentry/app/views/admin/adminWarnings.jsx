import { __extends, __read } from "tslib";
import React from 'react';
import AsyncView from 'app/views/asyncView';
import { t } from 'app/locale';
var AdminWarnings = /** @class */ (function (_super) {
    __extends(AdminWarnings, _super);
    function AdminWarnings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminWarnings.prototype.getEndpoints = function () {
        return [['data', '/internal/warnings/']];
    };
    AdminWarnings.prototype.renderBody = function () {
        var data = this.state.data;
        if (data === null) {
            return null;
        }
        var groups = data.groups, warnings = data.warnings;
        return (<div>
        <h3>{t('System Warnings')}</h3>
        {!warnings && !groups && t('There are no warnings at this time')}

        {groups.map(function (_a) {
            var _b = __read(_a, 2), groupName = _b[0], groupedWarnings = _b[1];
            return (<React.Fragment key={groupName}>
            <h4>{groupName}</h4>
            <ul>
              {groupedWarnings.map(function (warning, i) { return (<li key={i}>{warning}</li>); })}
            </ul>
          </React.Fragment>);
        })}

        {warnings.length > 0 && (<React.Fragment>
            <h4>Miscellaneous</h4>
            <ul>
              {warnings.map(function (warning, i) { return (<li key={i}>{warning}</li>); })}
            </ul>
          </React.Fragment>)}
      </div>);
    };
    return AdminWarnings;
}(AsyncView));
export default AdminWarnings;
//# sourceMappingURL=adminWarnings.jsx.map