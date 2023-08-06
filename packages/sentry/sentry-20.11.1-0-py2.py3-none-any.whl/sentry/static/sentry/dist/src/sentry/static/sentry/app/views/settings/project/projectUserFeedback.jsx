import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import space from 'app/styles/space';
import TextBlock from 'app/views/settings/components/text/textBlock';
import formGroups from 'app/data/forms/userFeedback';
import routeTitleGen from 'app/utils/routeTitle';
var ProjectUserFeedbackSettings = /** @class */ (function (_super) {
    __extends(ProjectUserFeedbackSettings, _super);
    function ProjectUserFeedbackSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            Sentry.showReportDialog({
                // should never make it to the Sentry API, but just in case, use throwaway id
                eventId: '00000000000000000000000000000000',
            });
        };
        return _this;
    }
    ProjectUserFeedbackSettings.prototype.componentDidMount = function () {
        window.sentryEmbedCallback = function (embed) {
            // Mock the embed's submit xhr to always be successful
            // NOTE: this will not have errors if the form is empty
            embed.submit = function (_body) {
                var _this = this;
                this._submitInProgress = true;
                setTimeout(function () {
                    _this._submitInProgress = false;
                    _this.onSuccess();
                }, 500);
            };
        };
    };
    ProjectUserFeedbackSettings.prototype.componentWillUnmount = function () {
        window.sentryEmbedCallback = null;
    };
    ProjectUserFeedbackSettings.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [
            ['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"],
            ['project', "/projects/" + orgId + "/" + projectId + "/"],
        ];
    };
    ProjectUserFeedbackSettings.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('User Feedback'), projectId, false);
    };
    ProjectUserFeedbackSettings.prototype.renderBody = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return (<div>
        <SettingsPageHeader title={t('User Feedback')}/>
        <TextBlock>
          {t("Don't rely on stack traces and graphs alone to understand\n            the cause and impact of errors. Enable User Feedback to collect\n            your users' comments when they encounter a crash or bug.")}
        </TextBlock>
        <TextBlock>
          {t("When configured, your users will be presented with a dialog prompting\n            them for additional information. That information will get attached to\n            the issue in Sentry.")}
        </TextBlock>
        <ButtonList>
          <Button external href="https://docs.sentry.io/enriching-error-data/user-feedback/">
            {t('Read the docs')}
          </Button>
          <Button priority="primary" onClick={this.handleClick}>
            {t('Open the report dialog')}
          </Button>
        </ButtonList>

        <Form saveOnBlur apiMethod="PUT" apiEndpoint={"/projects/" + orgId + "/" + projectId + "/"} initialData={this.state.project.options}>
          <Access access={['project:write']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return <JsonForm disabled={!hasAccess} forms={formGroups}/>;
        }}
          </Access>
        </Form>
      </div>);
    };
    return ProjectUserFeedbackSettings;
}(AsyncView));
var ButtonList = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"])), space(1), space(2));
export default ProjectUserFeedbackSettings;
var templateObject_1;
//# sourceMappingURL=projectUserFeedback.jsx.map