import { __extends } from "tslib";
import React from 'react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import Link from 'app/components/links/link';
import { t, tct } from 'app/locale';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import Form from 'app/views/settings/components/forms/form';
import projectSecurityAndPrivacyGroups from 'app/data/forms/projectSecurityAndPrivacyGroups';
import ProjectActions from 'app/actions/projectActions';
import withProject from 'app/utils/withProject';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import DataScrubbing from '../components/dataScrubbing';
var ProjectSecurityAndPrivacy = /** @class */ (function (_super) {
    __extends(ProjectSecurityAndPrivacy, _super);
    function ProjectSecurityAndPrivacy() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateProject = function (data) {
            // This will update our project global state
            ProjectActions.updateSuccess(data);
        };
        return _this;
    }
    ProjectSecurityAndPrivacy.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var initialData = project;
        var projectSlug = project.slug;
        var endpoint = "/projects/" + organization.slug + "/" + projectSlug + "/";
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        var relayPiiConfig = project.relayPiiConfig;
        var apiMethod = 'PUT';
        var title = t('Security & Privacy');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} objSlug={projectSlug}/>
        <SettingsPageHeader title={title}/>
        <Form saveOnBlur allowUndo initialData={initialData} apiMethod={apiMethod} apiEndpoint={endpoint} onSubmitSuccess={this.handleUpdateProject} onSubmitError={function () { return addErrorMessage('Unable to save change'); }}>
          <JsonForm additionalFieldProps={{ organization: organization }} features={features} disabled={!access.has('project:write')} forms={projectSecurityAndPrivacyGroups}/>
        </Form>
        <DataScrubbing additionalContext={<span>
              {tct('These rules can be configured at the organization level in [linkToOrganizationSecurityAndPrivacy].', {
            linkToOrganizationSecurityAndPrivacy: (<Link to={"/settings/" + organization.slug + "/security-and-privacy/"}>
                      {title}
                    </Link>),
        })}
            </span>} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('project:write')} organization={organization} projectId={project.id} onSubmitSuccess={this.handleUpdateProject}/>
      </React.Fragment>);
    };
    return ProjectSecurityAndPrivacy;
}(React.Component));
export default withProject(ProjectSecurityAndPrivacy);
//# sourceMappingURL=index.jsx.map