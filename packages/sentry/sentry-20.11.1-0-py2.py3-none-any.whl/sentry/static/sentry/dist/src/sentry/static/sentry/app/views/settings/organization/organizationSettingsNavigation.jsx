import Reflux from 'reflux';
import React from 'react';
import createReactClass from 'create-react-class';
import SentryTypes from 'app/sentryTypes';
import HookStore from 'app/stores/hookStore';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
import navigationConfiguration from 'app/views/settings/organization/navigationConfiguration';
import withOrganization from 'app/utils/withOrganization';
var OrganizationSettingsNavigation = createReactClass({
    displayName: 'OrganizationSettingsNavigation',
    propTypes: {
        organization: SentryTypes.Organization,
    },
    /**
     * TODO(epurkhiser): Becase the settings organization navigation hooks
     * do not conform to a normal component style hook, and take a single
     * parameter 'organization', we cannot use the `Hook` component here,
     * and must resort to using the mixin style HookStore to retrieve hook data.
     *
     * We should update the hook interface for the two hooks used here
     */
    mixins: [Reflux.listenTo(HookStore, 'handleHooks')],
    getInitialState: function () {
        return this.getHooks();
    },
    componentDidMount: function () {
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState(this.getHooks());
    },
    getHooks: function () {
        // Allow injection via getsentry et all
        var organization = this.props.organization;
        return {
            hookConfigs: HookStore.get('settings:organization-navigation-config').map(function (cb) {
                return cb(organization);
            }),
            hooks: HookStore.get('settings:organization-navigation').map(function (cb) {
                return cb(organization);
            }),
        };
    },
    handleHooks: function (name, hooks) {
        var org = this.props.organization;
        if (name !== 'settings:organization-navigation-config') {
            return;
        }
        this.setState({ hookConfigs: hooks.map(function (cb) { return cb(org); }) });
    },
    render: function () {
        var _a = this.state, hooks = _a.hooks, hookConfigs = _a.hookConfigs;
        var organization = this.props.organization;
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        return (<SettingsNavigation navigationObjects={navigationConfiguration} access={access} features={features} organization={organization} hooks={hooks} hookConfigs={hookConfigs}/>);
    },
});
export default withOrganization(OrganizationSettingsNavigation);
//# sourceMappingURL=organizationSettingsNavigation.jsx.map