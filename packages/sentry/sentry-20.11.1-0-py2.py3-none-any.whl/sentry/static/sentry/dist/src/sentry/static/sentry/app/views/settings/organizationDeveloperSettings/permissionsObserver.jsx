import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { toResourcePermissions } from 'app/utils/consolidatedScopes';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import PermissionSelection from 'app/views/settings/organizationDeveloperSettings/permissionSelection';
import Subscriptions from 'app/views/settings/organizationDeveloperSettings/resourceSubscriptions';
var PermissionsObserver = /** @class */ (function (_super) {
    __extends(PermissionsObserver, _super);
    function PermissionsObserver(props) {
        var _this = _super.call(this, props) || this;
        _this.onPermissionChange = function (permissions) {
            _this.setState({ permissions: permissions });
        };
        _this.onEventChange = function (events) {
            _this.setState({ events: events });
        };
        _this.state = {
            permissions: _this.scopeListToPermissionState(),
            events: _this.props.events,
        };
        return _this;
    }
    /**
     * Converts the list of raw API scopes passed in to an object that can
     * before stored and used via `state`. This object is structured by
     * resource and holds "Permission" values. For example:
     *
     *    {
     *      'Project': 'read',
     *      ...,
     *    }
     *
     */
    PermissionsObserver.prototype.scopeListToPermissionState = function () {
        return toResourcePermissions(this.props.scopes);
    };
    PermissionsObserver.prototype.render = function () {
        var _a = this.state, permissions = _a.permissions, events = _a.events;
        return (<React.Fragment>
        <Panel>
          <PanelHeader>{t('Permissions')}</PanelHeader>
          <PanelBody>
            <PermissionSelection permissions={permissions} onChange={this.onPermissionChange} appPublished={this.props.appPublished}/>
          </PanelBody>
        </Panel>
        <Panel>
          <PanelHeader>{t('Webhooks')}</PanelHeader>
          <PanelBody>
            <Subscriptions permissions={permissions} events={events} onChange={this.onEventChange} webhookDisabled={this.props.webhookDisabled}/>
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    PermissionsObserver.propTypes = {
        scopes: PropTypes.arrayOf(PropTypes.string).isRequired,
        events: PropTypes.arrayOf(PropTypes.string).isRequired,
        webhookDisabled: PropTypes.bool.isRequired,
        appPublished: PropTypes.bool.isRequired,
    };
    PermissionsObserver.contextTypes = {
        router: PropTypes.object.isRequired,
        form: PropTypes.object,
    };
    PermissionsObserver.defaultProps = {
        webhookDisabled: false,
        appPublished: false,
    };
    return PermissionsObserver;
}(React.Component));
export default PermissionsObserver;
//# sourceMappingURL=permissionsObserver.jsx.map