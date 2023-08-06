import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { PageContent } from 'app/styles/organization';
import { defined } from 'app/utils';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import Duration from 'app/components/duration';
import Feature from 'app/components/acl/feature';
import Link from 'app/components/links/link';
import NavTabs from 'app/components/navTabs';
import Placeholder from 'app/components/placeholder';
import SeenByList from 'app/components/seenByList';
import { IconWarning } from 'app/icons';
import { SectionHeading } from 'app/components/charts/styles';
import Projects from 'app/utils/projects';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { Panel, PanelBody, PanelFooter } from 'app/components/panels';
import Button from 'app/components/button';
import { AlertRuleThresholdType } from 'app/views/settings/incidentRules/types';
import { makeDefaultCta } from 'app/views/settings/incidentRules/presets';
import { DATASET_EVENT_TYPE_FILTERS } from 'app/views/settings/incidentRules/constants';
import Activity from './activity';
import Chart from './chart';
import { AlertRuleStatus, IncidentStatus, IncidentStatusMethod, } from '../types';
import { getIncidentMetricPreset, DATA_SOURCE_LABELS } from '../utils';
var DetailsBody = /** @class */ (function (_super) {
    __extends(DetailsBody, _super);
    function DetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(DetailsBody.prototype, "metricPreset", {
        get: function () {
            var incident = this.props.incident;
            return incident ? getIncidentMetricPreset(incident) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Return a string describing the threshold based on the threshold and the type
     */
    DetailsBody.prototype.getThresholdText = function (value, thresholdType, isAlert) {
        if (isAlert === void 0) { isAlert = false; }
        if (!defined(value)) {
            return '';
        }
        var isAbove = thresholdType === AlertRuleThresholdType.ABOVE;
        var direction = isAbove === isAlert ? '>' : '<';
        return direction + " " + value;
    };
    DetailsBody.prototype.renderRuleDetails = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        var incident = this.props.incident;
        if (incident === undefined) {
            return <Placeholder height="200px"/>;
        }
        var criticalTrigger = incident === null || incident === void 0 ? void 0 : incident.alertRule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = incident === null || incident === void 0 ? void 0 : incident.alertRule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        return (<RuleDetails>
        <span>{t('Data Source')}</span>
        <span>{DATA_SOURCE_LABELS[(_a = incident.alertRule) === null || _a === void 0 ? void 0 : _a.dataset]}</span>

        <span>{t('Metric')}</span>
        <span>{(_b = incident.alertRule) === null || _b === void 0 ? void 0 : _b.aggregate}</span>

        <span>{t('Time Window')}</span>
        <span>
          {incident && <Duration seconds={incident.alertRule.timeWindow * 60}/>}
        </span>

        {((_c = incident.alertRule) === null || _c === void 0 ? void 0 : _c.query) && (<React.Fragment>
            <span>{t('Filter')}</span>
            <span title={(_d = incident.alertRule) === null || _d === void 0 ? void 0 : _d.query}>{(_e = incident.alertRule) === null || _e === void 0 ? void 0 : _e.query}</span>
          </React.Fragment>)}

        <span>{t('Critical Trigger')}</span>
        <span>
          {this.getThresholdText(criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold, (_f = incident.alertRule) === null || _f === void 0 ? void 0 : _f.thresholdType, true)}
        </span>

        {defined(warningTrigger) && (<React.Fragment>
            <span>{t('Warning Trigger')}</span>
            <span>
              {this.getThresholdText(warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold, (_g = incident.alertRule) === null || _g === void 0 ? void 0 : _g.thresholdType, true)}
            </span>
          </React.Fragment>)}

        {defined((_h = incident.alertRule) === null || _h === void 0 ? void 0 : _h.resolveThreshold) && (<React.Fragment>
            <span>{t('Resolution')}</span>
            <span>
              {this.getThresholdText((_j = incident.alertRule) === null || _j === void 0 ? void 0 : _j.resolveThreshold, (_k = incident.alertRule) === null || _k === void 0 ? void 0 : _k.thresholdType)}
            </span>
          </React.Fragment>)}
      </RuleDetails>);
    };
    DetailsBody.prototype.renderChartHeader = function () {
        var _a, _b, _c, _d, _e;
        var incident = this.props.incident;
        var alertRule = incident === null || incident === void 0 ? void 0 : incident.alertRule;
        return (<ChartHeader>
        <div>
          {(_b = (_a = this.metricPreset) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : t('Custom metric')}
          <ChartParameters>
            {tct('Metric: [metric] over [window]', {
            metric: <code>{(_c = alertRule === null || alertRule === void 0 ? void 0 : alertRule.aggregate) !== null && _c !== void 0 ? _c : '\u2026'}</code>,
            window: (<code>
                  {incident ? (<Duration seconds={incident.alertRule.timeWindow * 60}/>) : ('\u2026')}
                </code>),
        })}
            {((alertRule === null || alertRule === void 0 ? void 0 : alertRule.query) || ((_d = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _d === void 0 ? void 0 : _d.dataset)) &&
            tct('Filter: [datasetType] [filter]', {
                datasetType: ((_e = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _e === void 0 ? void 0 : _e.dataset) && (<code>{DATASET_EVENT_TYPE_FILTERS[incident.alertRule.dataset]}</code>),
                filter: (alertRule === null || alertRule === void 0 ? void 0 : alertRule.query) && <code>{alertRule.query}</code>,
            })}
          </ChartParameters>
        </div>
      </ChartHeader>);
    };
    DetailsBody.prototype.renderChartActions = function () {
        var _this = this;
        var _a = this.props, incident = _a.incident, params = _a.params, stats = _a.stats;
        return (
        // Currently only one button in pannel, hide panel if not available
        <Feature features={['discover-basic']}>
        <ChartActions>
          <Projects slugs={incident === null || incident === void 0 ? void 0 : incident.projects} orgId={params.orgId}>
            {function (_a) {
            var initiallyLoaded = _a.initiallyLoaded, fetching = _a.fetching, projects = _a.projects;
            var preset = _this.metricPreset;
            var ctaOpts = {
                orgSlug: params.orgId,
                projects: (initiallyLoaded ? projects : []),
                incident: incident,
                stats: stats,
            };
            var _b = preset
                ? preset.makeCtaParams(ctaOpts)
                : makeDefaultCta(ctaOpts), buttonText = _b.buttonText, props = __rest(_b, ["buttonText"]);
            return (<Button size="small" priority="primary" disabled={!incident || fetching || !initiallyLoaded} {...props}>
                  {buttonText}
                </Button>);
        }}
          </Projects>
        </ChartActions>
      </Feature>);
    };
    DetailsBody.prototype.render = function () {
        var _a, _b;
        var _c = this.props, params = _c.params, incident = _c.incident, stats = _c.stats;
        return (<StyledPageContent>
        <Main>
          {incident &&
            incident.status === IncidentStatus.CLOSED &&
            incident.statusMethod === IncidentStatusMethod.RULE_UPDATED && (<AlertWrapper>
                <Alert type="warning" icon={<IconWarning size="sm"/>}>
                  {t('This alert has been auto-resolved because the rule that triggered it has been modified or deleted')}
                </Alert>
              </AlertWrapper>)}
          <PageContent>
            <ChartPanel>
              <PanelBody withPadding>
                {this.renderChartHeader()}
                {incident && stats ? (<Chart triggers={incident.alertRule.triggers} resolveThreshold={incident.alertRule.resolveThreshold} aggregate={incident.alertRule.aggregate} data={stats.eventStats.data} started={incident.dateStarted} closed={incident.dateClosed || undefined}/>) : (<Placeholder height="200px"/>)}
              </PanelBody>
              {this.renderChartActions()}
            </ChartPanel>
          </PageContent>
          <DetailWrapper>
            <ActivityPageContent>
              <StyledNavTabs underlined>
                <li className="active">
                  <Link to="">{t('Activity')}</Link>
                </li>

                <SeenByTab>
                  {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={t('People who have viewed this alert')}/>)}
                </SeenByTab>
              </StyledNavTabs>
              <Activity incident={incident} params={params} incidentStatus={!!incident ? incident.status : null}/>
            </ActivityPageContent>
            <Sidebar>
              <SidebarHeading>
                <span>{t('Alert Rule')}</span>
                {((_a = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _a === void 0 ? void 0 : _a.status) !== AlertRuleStatus.SNAPSHOT && (<SideHeaderLink disabled={!!(incident === null || incident === void 0 ? void 0 : incident.id)} to={(incident === null || incident === void 0 ? void 0 : incident.id) ? {
            pathname: "/organizations/" + params.orgId + "/alerts/metric-rules/" + (incident === null || incident === void 0 ? void 0 : incident.projects[0]) + "/" + ((_b = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _b === void 0 ? void 0 : _b.id) + "/",
        }
            : ''}>
                    {t('View Alert Rule')}
                  </SideHeaderLink>)}
              </SidebarHeading>
              {this.renderRuleDetails()}
            </Sidebar>
          </DetailWrapper>
        </Main>
      </StyledPageContent>);
    };
    return DetailsBody;
}(React.Component));
export default DetailsBody;
var Main = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  padding-top: ", ";\n  flex-grow: 1;\n"], ["\n  background-color: ", ";\n  padding-top: ", ";\n  flex-grow: 1;\n"])), function (p) { return p.theme.background; }, space(3));
var DetailWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ActivityPageContent = styled(PageContent)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    width: 100%;\n    margin-bottom: 0;\n  }\n"], ["\n  @media (max-width: ", ") {\n    width: 100%;\n    margin-bottom: 0;\n  }\n"])), theme.breakpoints[0]);
var Sidebar = styled(PageContent)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 400px;\n  flex: none;\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    width: 100%;\n    padding-top: ", ";\n    margin-bottom: 0;\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  width: 400px;\n  flex: none;\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    width: 100%;\n    padding-top: ", ";\n    margin-bottom: 0;\n    border-bottom: 1px solid ", ";\n  }\n"])), space(3), theme.breakpoints[0], space(3), function (p) { return p.theme.border; });
var SidebarHeading = styled(SectionHeading)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var SideHeaderLink = styled(Link)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-weight: normal;\n"], ["\n  font-weight: normal;\n"])));
var StyledPageContent = styled(PageContent)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  padding: 0;\n  flex-direction: column;\n"], ["\n  padding: 0;\n  flex-direction: column;\n"])));
var ChartPanel = styled(Panel)(templateObject_8 || (templateObject_8 = __makeTemplateObject([""], [""])));
var ChartHeader = styled('header')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var ChartActions = styled(PanelFooter)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  padding: ", ";\n"])), space(2));
var ChartParameters = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  align-items: center;\n  overflow-x: auto;\n\n  > * {\n    position: relative;\n  }\n\n  > *:not(:last-of-type):after {\n    content: '';\n    display: block;\n    height: 70%;\n    width: 1px;\n    background: ", ";\n    position: absolute;\n    right: -", ";\n    top: 15%;\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  align-items: center;\n  overflow-x: auto;\n\n  > * {\n    position: relative;\n  }\n\n  > *:not(:last-of-type):after {\n    content: '';\n    display: block;\n    height: 70%;\n    width: 1px;\n    background: ", ";\n    position: absolute;\n    right: -", ";\n    top: 15%;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(4), function (p) { return p.theme.gray200; }, space(2));
var AlertWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  padding: ", " ", " 0;\n"], ["\n  padding: ", " ", " 0;\n"])), space(2), space(4));
var StyledNavTabs = styled(NavTabs)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var SeenByTab = styled('li')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"], ["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"])), space(2));
var StyledSeenByList = styled(SeenByList)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var RuleDetails = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  display: grid;\n  font-size: ", ";\n  grid-template-columns: auto max-content;\n  margin-bottom: ", ";\n\n  & > span {\n    padding: ", " ", ";\n  }\n\n  & > span:nth-child(2n + 1) {\n    width: 125px;\n  }\n\n  & > span:nth-child(2n + 2) {\n    text-align: right;\n    width: 215px;\n    text-overflow: ellipsis;\n    white-space: nowrap;\n    overflow: hidden;\n  }\n\n  & > span:nth-child(4n + 1),\n  & > span:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"], ["\n  display: grid;\n  font-size: ", ";\n  grid-template-columns: auto max-content;\n  margin-bottom: ", ";\n\n  & > span {\n    padding: ", " ", ";\n  }\n\n  & > span:nth-child(2n + 1) {\n    width: 125px;\n  }\n\n  & > span:nth-child(2n + 2) {\n    text-align: right;\n    width: 215px;\n    text-overflow: ellipsis;\n    white-space: nowrap;\n    overflow: hidden;\n  }\n\n  & > span:nth-child(4n + 1),\n  & > span:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, space(2), space(0.5), space(1), function (p) { return p.theme.rowBackground; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=body.jsx.map