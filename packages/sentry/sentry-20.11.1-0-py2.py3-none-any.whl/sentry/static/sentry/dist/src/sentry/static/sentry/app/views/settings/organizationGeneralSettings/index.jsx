import { __extends } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import { Panel, PanelHeader } from 'app/components/panels';
import { addLoadingMessage } from 'app/actionCreators/indicator';
import { changeOrganizationSlug, removeAndRedirectToRemainingOrganization, updateOrganization, } from 'app/actionCreators/organizations';
import { t, tct } from 'app/locale';
import Field from 'app/views/settings/components/forms/field';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
import PermissionAlert from 'app/views/settings/organization/permissionAlert';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import OrganizationSettingsForm from './organizationSettingsForm';
var OrganizationGeneralSettings = /** @class */ (function (_super) {
    __extends(OrganizationGeneralSettings, _super);
    function OrganizationGeneralSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemoveOrganization = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, params = _a.params;
            if (!organization) {
                return;
            }
            addLoadingMessage();
            removeAndRedirectToRemainingOrganization(api, {
                orgId: params.orgId,
                successMessage: organization.name + " is queued for deletion.",
                errorMessage: "Error removing the " + organization.name + " organization",
            });
        };
        _this.handleSave = function (prevData, data) {
            if (data.slug && data.slug !== prevData.slug) {
                changeOrganizationSlug(prevData, data);
                browserHistory.replace("/settings/" + data.slug + "/");
            }
            else {
                // This will update OrganizationStore (as well as OrganizationsStore
                // which is slightly incorrect because it has summaries vs a detailed org)
                updateOrganization(data);
            }
        };
        return _this;
    }
    OrganizationGeneralSettings.prototype.render = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var orgId = params.orgId;
        var access = new Set(organization.access);
        var hasProjects = organization.projects && !!organization.projects.length;
        return (<React.Fragment>
        <SentryDocumentTitle title={t('General Settings')} objSlug={orgId}/>
        <div>
          <SettingsPageHeader title={t('Organization Settings')}/>
          <PermissionAlert />

          <OrganizationSettingsForm {...this.props} initialData={organization} access={access} onSave={this.handleSave}/>

          {access.has('org:admin') && !organization.isDefault && (<Panel>
              <PanelHeader>{t('Remove Organization')}</PanelHeader>
              <Field label={t('Remove Organization')} help={t('Removing this organization will delete all data including projects and their associated events.')}>
                <div>
                  <LinkWithConfirmation className="btn btn-danger" priority="danger" title={t('Remove %s organization', organization && organization.name)} message={<div>
                        <TextBlock>
                          {tct('Removing the organization, [name] is permanent and cannot be undone! Are you sure you want to continue?', {
            name: organization && <strong>{organization.name}</strong>,
        })}
                        </TextBlock>

                        {hasProjects && (<div>
                            <TextBlock noMargin>
                              {t('This will also remove the following associated projects:')}
                            </TextBlock>
                            <ul className="ref-projects">
                              {organization.projects.map(function (project) { return (<li key={project.slug}>{project.slug}</li>); })}
                            </ul>
                          </div>)}
                      </div>} onConfirm={this.handleRemoveOrganization}>
                    {t('Remove Organization')}
                  </LinkWithConfirmation>
                </div>
              </Field>
            </Panel>)}
        </div>
      </React.Fragment>);
    };
    return OrganizationGeneralSettings;
}(React.Component));
export default withApi(withOrganization(OrganizationGeneralSettings));
//# sourceMappingURL=index.jsx.map