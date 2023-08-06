import { __assign, __rest } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import OrganizationsStore from 'app/stores/organizationsStore';
var withOrganizations = function (WrappedComponent) {
    return createReactClass({
        displayName: "withOrganizations(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.connect(OrganizationsStore, 'organizations')],
        render: function () {
            var _a = this.props, organizationsLoading = _a.organizationsLoading, organizations = _a.organizations, props = __rest(_a, ["organizationsLoading", "organizations"]);
            return (<WrappedComponent {...__assign({ organizationsLoading: organizationsLoading !== null && organizationsLoading !== void 0 ? organizationsLoading : !OrganizationsStore.loaded, organizations: organizations !== null && organizations !== void 0 ? organizations : this.state.organizations }, props)}/>);
        },
    });
};
export default withOrganizations;
//# sourceMappingURL=withOrganizations.jsx.map