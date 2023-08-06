import { __assign, __extends } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ErrorBoundary from 'app/components/errorBoundary';
import Field from 'app/views/settings/components/forms/field';
import { IconFlag } from 'app/icons';
import ServiceHookSettingsForm from 'app/views/settings/project/serviceHookSettingsForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import MiniBarChart from 'app/components/charts/miniBarChart';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import getDynamicText from 'app/utils/getDynamicText';
var HookStats = /** @class */ (function (_super) {
    __extends(HookStats, _super);
    function HookStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HookStats.prototype.getEndpoints = function () {
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        var _a = this.props.params, hookId = _a.hookId, orgId = _a.orgId, projectId = _a.projectId;
        return [
            [
                'stats',
                "/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/stats/",
                {
                    query: {
                        since: since,
                        until: until,
                        resolution: '1d',
                    },
                },
            ],
        ];
    };
    HookStats.prototype.renderBody = function () {
        var stats = this.state.stats;
        if (stats === null) {
            return null;
        }
        var emptyStats = true;
        var series = {
            seriesName: t('Events'),
            data: stats.map(function (p) {
                if (p.total) {
                    emptyStats = false;
                }
                return {
                    name: p.ts * 1000,
                    value: p.total,
                };
            }),
        };
        return (<Panel>
        <PanelHeader>{t('Events in the last 30 days (by day)')}</PanelHeader>
        <PanelBody withPadding>
          {!emptyStats ? (<MiniBarChart isGroupedByDate showTimeInTooltip labelYAxisExtents series={[series]} height={150}/>) : (<EmptyMessage title={t('Nothing recorded in the last 30 days.')} description={t('Total webhooks fired for this configuration.')}/>)}
        </PanelBody>
      </Panel>);
    };
    return HookStats;
}(AsyncComponent));
var ProjectServiceHookDetails = /** @class */ (function (_super) {
    __extends(ProjectServiceHookDetails, _super);
    function ProjectServiceHookDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onDelete = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
            addLoadingMessage(t('Saving changes\u2026'));
            _this.api.request("/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/", {
                method: 'DELETE',
                success: function () {
                    clearIndicators();
                    browserHistory.push("/settings/" + orgId + "/projects/" + projectId + "/hooks/");
                },
                error: function () {
                    addErrorMessage(t('Unable to remove application. Please try again.'));
                },
            });
        };
        return _this;
    }
    ProjectServiceHookDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
        return [['hook', "/projects/" + orgId + "/" + projectId + "/hooks/" + hookId + "/"]];
    };
    ProjectServiceHookDetails.prototype.renderBody = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, hookId = _a.hookId;
        var hook = this.state.hook;
        if (!hook) {
            return null;
        }
        return (<React.Fragment>
        <SettingsPageHeader title={t('Service Hook Details')}/>

        <ErrorBoundary>
          <HookStats params={this.props.params}/>
        </ErrorBoundary>

        <ServiceHookSettingsForm orgId={orgId} projectId={projectId} hookId={hookId} initialData={__assign(__assign({}, hook), { isActive: hook.status !== 'disabled' })}/>
        <Panel>
          <PanelHeader>{t('Event Validation')}</PanelHeader>
          <PanelBody>
            <PanelAlert type="info" icon={<IconFlag size="md"/>}>
              Sentry will send the <code>X-ServiceHook-Signature</code> header built using{' '}
              <code>HMAC(SHA256, [secret], [payload])</code>. You should always verify
              this signature before trusting the information provided in the webhook.
            </PanelAlert>
            <Field label={t('Secret')} flexibleControlStateSize inline={false} help={t('The shared secret used for generating event HMAC signatures.')}>
              <TextCopyInput>
                {getDynamicText({
            value: hook.secret,
            fixed: 'a dynamic secret value',
        })}
              </TextCopyInput>
            </Field>
          </PanelBody>
        </Panel>
        <Panel>
          <PanelHeader>{t('Delete Hook')}</PanelHeader>
          <PanelBody>
            <Field label={t('Delete Hook')} help={t('Removing this hook is immediate and permanent.')}>
              <div>
                <Button priority="danger" onClick={this.onDelete}>
                  {t('Delete Hook')}
                </Button>
              </div>
            </Field>
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    return ProjectServiceHookDetails;
}(AsyncView));
export default ProjectServiceHookDetails;
//# sourceMappingURL=projectServiceHookDetails.jsx.map