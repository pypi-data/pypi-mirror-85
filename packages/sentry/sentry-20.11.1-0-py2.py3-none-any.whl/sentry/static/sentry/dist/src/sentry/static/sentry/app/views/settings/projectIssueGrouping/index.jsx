import { __assign, __extends } from "tslib";
import React from 'react';
import { fields } from 'app/data/forms/projectIssueGrouping';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import routeTitleGen from 'app/utils/routeTitle';
import ProjectActions from 'app/actions/projectActions';
import Feature from 'app/components/acl/feature';
import ExternalLink from 'app/components/links/externalLink';
import UpgradeGrouping from './upgradeGrouping';
var ProjectDebugSymbols = /** @class */ (function (_super) {
    __extends(ProjectDebugSymbols, _super);
    function ProjectDebugSymbols() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (response) {
            // This will update our project context
            ProjectActions.updateSuccess(response);
        };
        return _this;
    }
    ProjectDebugSymbols.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Issue Grouping'), projectId, false);
    };
    ProjectDebugSymbols.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { groupingConfigs: [], groupingEnhancementBases: [] });
    };
    ProjectDebugSymbols.prototype.getEndpoints = function () {
        return [
            ['groupingConfigs', '/grouping-configs/'],
            ['groupingEnhancementBases', '/grouping-enhancements/'],
        ];
    };
    ProjectDebugSymbols.prototype.renderBody = function () {
        var _a = this.state, groupingConfigs = _a.groupingConfigs, groupingEnhancementBases = _a.groupingEnhancementBases;
        var _b = this.props, organization = _b.organization, project = _b.project, params = _b.params;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoint = "/projects/" + orgId + "/" + projectId + "/";
        var access = new Set(organization.access);
        var jsonFormProps = {
            additionalFieldProps: {
                organization: organization,
                groupingConfigs: groupingConfigs,
                groupingEnhancementBases: groupingEnhancementBases,
            },
            features: new Set(organization.features),
            access: access,
            disabled: !access.has('project:write'),
        };
        return (<React.Fragment>
        <SettingsPageHeader title={t('Issue Grouping')}/>

        <TextBlock>
          {tct("All events have a fingerprint. Events with the same fingerprint are grouped together into an issue. To learn more about issue grouping, [link: read the docs].", {
            link: (<ExternalLink href="https://docs.sentry.io/platform-redirect/?next=%2Fdata-management%2Fevent-grouping%2F"/>),
        })}
        </TextBlock>

        <Form saveOnBlur allowUndo initialData={project} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmit}>
          <JsonForm {...jsonFormProps} title={t('Fingerprint Rules')} fields={[fields.fingerprintingRules]}/>

          <JsonForm {...jsonFormProps} title={t('Stack Trace Rules')} fields={[fields.groupingEnhancements]}/>

          <Feature features={['set-grouping-config']} organization={organization}>
            <JsonForm {...jsonFormProps} title={t('Change defaults')} fields={[fields.groupingConfig, fields.groupingEnhancementsBase]}/>
          </Feature>

          <UpgradeGrouping groupingConfigs={groupingConfigs !== null && groupingConfigs !== void 0 ? groupingConfigs : []} groupingEnhancementBases={groupingEnhancementBases !== null && groupingEnhancementBases !== void 0 ? groupingEnhancementBases : []} organization={organization} projectId={params.projectId} project={project} api={this.api} onUpgrade={this.fetchData}/>
        </Form>
      </React.Fragment>);
    };
    return ProjectDebugSymbols;
}(AsyncView));
export default ProjectDebugSymbols;
//# sourceMappingURL=index.jsx.map