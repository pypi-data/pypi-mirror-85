import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import ConfigStore from 'app/stores/configStore';
import LatestContextStore from 'app/stores/latestContextStore';
import SentryTypes from 'app/sentryTypes';
import getDisplayName from 'app/utils/getDisplayName';
import withOrganizations from 'app/utils/withOrganizations';
var withLatestContext = function (WrappedComponent) {
    return withOrganizations(createReactClass({
        displayName: "withLatestContext(" + getDisplayName(WrappedComponent) + ")",
        propTypes: {
            organization: SentryTypes.Organization,
            organizations: PropTypes.arrayOf(SentryTypes.Organization).isRequired,
        },
        mixins: [Reflux.connect(LatestContextStore, 'latestContext')],
        render: function () {
            var organizations = this.props.organizations;
            var latestContext = this.state.latestContext;
            var _a = latestContext || {}, organization = _a.organization, project = _a.project, lastRoute = _a.lastRoute;
            // Even though org details exists in LatestContextStore,
            // fetch organization from OrganizationsStore so that we can
            // expect consistent data structure because OrganizationsStore has a list
            // of orgs but not full org details
            var latestOrganization = organization ||
                (organizations && organizations.length
                    ? organizations.find(function (_a) {
                        var slug = _a.slug;
                        return slug === ConfigStore.get('lastOrganization');
                    }) || organizations[0]
                    : null);
            // TODO(billy): Below is going to be wrong if component is passed project, it will override
            // project from `latestContext`
            return (<WrappedComponent organizations={organizations} project={project} lastRoute={lastRoute} {...this.props} organization={(this.props.organization || latestOrganization)}/>);
        },
    }));
};
export default withLatestContext;
//# sourceMappingURL=withLatestContext.jsx.map