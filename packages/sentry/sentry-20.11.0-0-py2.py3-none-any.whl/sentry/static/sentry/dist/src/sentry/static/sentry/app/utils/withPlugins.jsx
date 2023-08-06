import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import { defined } from 'app/utils';
import { fetchPlugins } from 'app/actionCreators/plugins';
import getDisplayName from 'app/utils/getDisplayName';
import PluginsStore from 'app/stores/pluginsStore';
import SentryTypes from 'app/sentryTypes';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
/**
 * Higher order component that fetches list of plugins and
 * passes PluginsStore to component as `plugins`
 */
var withPlugins = function (WrappedComponent) {
    return withOrganization(withProject(createReactClass({
        displayName: "withPlugins(" + getDisplayName(WrappedComponent) + ")",
        propTypes: {
            organization: SentryTypes.Organization.isRequired,
            project: SentryTypes.Project.isRequired,
        },
        mixins: [Reflux.connect(PluginsStore, 'store')],
        componentDidMount: function () {
            this.fetchPlugins();
        },
        componentDidUpdate: function (prevProps, _prevState, prevContext) {
            var _a = this.props, organization = _a.organization, project = _a.project;
            // Only fetch plugins when a org slug or project slug has changed
            var prevOrg = prevProps.organization || (prevContext && prevContext.organization);
            var prevProject = prevProps.project || (prevContext && prevContext.project);
            // If previous org/project is undefined then it means:
            // the HoC has mounted, `fetchPlugins` has been called (via cDM), and
            // store was updated. We don't need to fetchPlugins again (or it will cause an infinite loop)
            //
            // This is for the unusual case where component is mounted and receives a new org/project prop
            // e.g. when switching projects via breadcrumbs in settings.
            if (!defined(prevProject) || !defined(prevOrg)) {
                return;
            }
            var isOrgSame = prevOrg.slug === organization.slug;
            var isProjectSame = prevProject.slug === project.slug;
            // Don't do anything if org and project are the same
            if (isOrgSame && isProjectSame) {
                return;
            }
            this.fetchPlugins();
        },
        fetchPlugins: function () {
            var _a = this.props, organization = _a.organization, project = _a.project;
            if (!project || !organization) {
                return;
            }
            fetchPlugins({ projectId: project.slug, orgId: organization.slug });
        },
        render: function () {
            return (<WrappedComponent {...this.props} plugins={this.state.store}/>);
        },
    })));
};
export default withPlugins;
//# sourceMappingURL=withPlugins.jsx.map