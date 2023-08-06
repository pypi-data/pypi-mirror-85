import { __assign, __rest } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { fetchOrgMembers } from 'app/actionCreators/members';
import Alert from 'app/components/alert';
import LoadingIndicator from 'app/components/loadingIndicator';
import Projects from 'app/utils/projects';
import withApi from 'app/utils/withApi';
function AlertBuilderProjectProvider(props) {
    var children = props.children, params = props.params, organization = props.organization, api = props.api, other = __rest(props, ["children", "params", "organization", "api"]);
    var projectId = params.projectId;
    return (<Projects orgId={organization.slug} slugs={[projectId]}>
      {function (_a) {
        var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, isIncomplete = _a.isIncomplete;
        if (!initiallyLoaded) {
            return <LoadingIndicator />;
        }
        // if loaded, but project fetching states incomplete, project doesn't exist
        if (isIncomplete) {
            return (<Alert type="warning">
              {t('The project you were looking for was not found.')}
            </Alert>);
        }
        var project = projects[0];
        // fetch members list for mail action fields
        fetchOrgMembers(api, organization.slug, [Number(project.id)]);
        return (<React.Fragment>
            {children && React.isValidElement(children)
            ? React.cloneElement(children, __assign(__assign(__assign({}, other), children.props), { project: project,
                organization: organization }))
            : children}
          </React.Fragment>);
    }}
    </Projects>);
}
export default withApi(AlertBuilderProjectProvider);
//# sourceMappingURL=projectProvider.jsx.map