import { __extends, __read } from "tslib";
import React from 'react';
import AsyncView from 'app/views/asyncView';
import { t } from 'app/locale';
var AdminPackages = /** @class */ (function (_super) {
    __extends(AdminPackages, _super);
    function AdminPackages() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminPackages.prototype.getEndpoints = function () {
        return [['data', '/internal/packages/']];
    };
    AdminPackages.prototype.renderBody = function () {
        var data = this.state.data;
        var extensions = data.extensions, modules = data.modules;
        return (<div>
        <h3>{t('Extensions')}</h3>

        {extensions.length > 0 ? (<dl className="vars">
            {extensions.map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return (<React.Fragment key={key}>
                <dt>{key}</dt>
                <dd>
                  <pre className="val">{value}</pre>
                </dd>
              </React.Fragment>);
        })}
          </dl>) : (<p>{t('No extensions registered')}</p>)}

        <h3>{t('Modules')}</h3>

        {modules.length > 0 ? (<dl className="vars">
            {modules.map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return (<React.Fragment key={key}>
                <dt>{key}</dt>
                <dd>
                  <pre className="val">{value}</pre>
                </dd>
              </React.Fragment>);
        })}
          </dl>) : (<p>{t('No modules registered')}</p>)}
      </div>);
    };
    return AdminPackages;
}(AsyncView));
export default AdminPackages;
//# sourceMappingURL=adminPackages.jsx.map