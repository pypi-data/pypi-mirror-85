import { __extends, __read } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import find from 'lodash/find';
import flatMap from 'lodash/flatMap';
import { t } from 'app/locale';
import { SENTRY_APP_PERMISSIONS } from 'app/constants';
import SelectField from 'app/views/settings/components/forms/selectField';
var PermissionSelection = /** @class */ (function (_super) {
    __extends(PermissionSelection, _super);
    function PermissionSelection() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            permissions: _this.props.permissions,
        };
        _this.onChange = function (resource, choice) {
            var permissions = _this.state.permissions;
            permissions[resource] = choice;
            _this.save(permissions);
        };
        _this.save = function (permissions) {
            _this.setState({ permissions: permissions });
            _this.props.onChange(permissions);
            _this.context.form.setValue('scopes', _this.permissionStateToList());
        };
        return _this;
    }
    /**
     * Converts the "Permission" values held in `state` to a list of raw
     * API scopes we can send to the server. For example:
     *
     *    ['org:read', 'org:write', ...]
     *
     */
    PermissionSelection.prototype.permissionStateToList = function () {
        var permissions = this.state.permissions;
        var findResource = function (r) { return find(SENTRY_APP_PERMISSIONS, ['resource', r]); };
        return flatMap(Object.entries(permissions), function (_a) {
            var _b, _c, _d;
            var _e = __read(_a, 2), r = _e[0], p = _e[1];
            return (_d = (_c = (_b = findResource(r)) === null || _b === void 0 ? void 0 : _b.choices) === null || _c === void 0 ? void 0 : _c[p]) === null || _d === void 0 ? void 0 : _d.scopes;
        });
    };
    PermissionSelection.prototype.render = function () {
        var _this = this;
        var permissions = this.state.permissions;
        return (<React.Fragment>
        {SENTRY_APP_PERMISSIONS.map(function (config) {
            var toChoice = function (_a) {
                var _b = __read(_a, 2), value = _b[0], opt = _b[1];
                return [value, opt.label];
            };
            var choices = Object.entries(config.choices).map(toChoice);
            var value = permissions[config.resource];
            return (<SelectField deprecatedSelectControl 
            // These are not real fields we want submitted, so we use
            // `--permission` as a suffix here, then filter these
            // fields out when submitting the form in
            // sentryApplicationDetails.jsx
            name={config.resource + "--permission"} key={config.resource} choices={choices} help={t(config.help)} label={t(config.label || config.resource)} onChange={_this.onChange.bind(_this, config.resource)} value={value} defaultValue={value} disabled={_this.props.appPublished} disabledReason={t('Cannot update permissions on a published integration')}/>);
        })}
      </React.Fragment>);
    };
    PermissionSelection.propTypes = {
        permissions: PropTypes.object.isRequired,
        onChange: PropTypes.func.isRequired,
        appPublished: PropTypes.bool,
    };
    PermissionSelection.contextTypes = {
        router: PropTypes.object.isRequired,
        form: PropTypes.object,
    };
    return PermissionSelection;
}(React.Component));
export default PermissionSelection;
//# sourceMappingURL=permissionSelection.jsx.map