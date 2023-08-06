import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import LineChart from 'app/components/charts/lineChart';
import { Panel, PanelBody, PanelHeader, PanelFooter } from 'app/components/panels';
import BarChart from 'app/components/charts/barChart';
import Link from 'app/components/links/link';
import DateTime from 'app/components/dateTime';
import space from 'app/styles/space';
import { t } from 'app/locale';
import RequestLog from './requestLog';
var SentryApplicationDashboard = /** @class */ (function (_super) {
    __extends(SentryApplicationDashboard, _super);
    function SentryApplicationDashboard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SentryApplicationDashboard.prototype.getEndpoints = function () {
        var appSlug = this.props.params.appSlug;
        // Default time range for now: 90 days ago to now
        var now = Math.floor(new Date().getTime() / 1000);
        var ninety_days_ago = 3600 * 24 * 90;
        return [
            [
                'stats',
                "/sentry-apps/" + appSlug + "/stats/",
                { query: { since: now - ninety_days_ago, until: now } },
            ],
            [
                'interactions',
                "/sentry-apps/" + appSlug + "/interaction/",
                { query: { since: now - ninety_days_ago, until: now } },
            ],
            ['app', "/sentry-apps/" + appSlug + "/"],
        ];
    };
    SentryApplicationDashboard.prototype.getTitle = function () {
        return t('Integration Dashboard');
    };
    SentryApplicationDashboard.prototype.renderInstallData = function () {
        var _a = this.state, app = _a.app, stats = _a.stats;
        var totalUninstalls = stats.totalUninstalls, totalInstalls = stats.totalInstalls;
        return (<React.Fragment>
        <h5>{t('Installation & Interaction Data')}</h5>
        <Row>
          {app.datePublished ? (<StatsSection>
              <StatsHeader>{t('Date published')}</StatsHeader>
              <DateTime dateOnly date={app.datePublished}/>
            </StatsSection>) : null}
          <StatsSection>
            <StatsHeader>{t('Total installs')}</StatsHeader>
            <p>{totalInstalls}</p>
          </StatsSection>
          <StatsSection>
            <StatsHeader>{t('Total uninstalls')}</StatsHeader>
            <p>{totalUninstalls}</p>
          </StatsSection>
        </Row>
        {this.renderInstallCharts()}
      </React.Fragment>);
    };
    SentryApplicationDashboard.prototype.renderInstallCharts = function () {
        var _a = this.state.stats, installStats = _a.installStats, uninstallStats = _a.uninstallStats;
        var installSeries = {
            data: installStats.map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
            seriesName: t('installed'),
        };
        var uninstallSeries = {
            data: uninstallStats.map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
            seriesName: t('uninstalled'),
        };
        return (<Panel>
        <PanelHeader>{t('Installations/Uninstallations over Last 90 Days')}</PanelHeader>
        <ChartWrapper>
          <BarChart series={[installSeries, uninstallSeries]} height={150} stacked isGroupedByDate legend={{
            show: true,
            orient: 'horizontal',
            data: ['installed', 'uninstalled'],
            itemWidth: 15,
        }} yAxis={{ type: 'value', minInterval: 1, max: 'dataMax' }} xAxis={{ type: 'time' }} grid={{ left: space(4), right: space(4) }}/>
        </ChartWrapper>
      </Panel>);
    };
    SentryApplicationDashboard.prototype.renderIntegrationViews = function () {
        var views = this.state.interactions.views;
        var _a = this.props.params, appSlug = _a.appSlug, orgId = _a.orgId;
        return (<Panel>
        <PanelHeader>{t('Integration Views')}</PanelHeader>
        <PanelBody>
          <InteractionsChart data={{ Views: views }}/>
        </PanelBody>

        <PanelFooter>
          <StyledFooter>
            {t('Integration views are measured through views on the ')}
            <Link to={"/sentry-apps/" + appSlug + "/external-install/"}>
              {t('external installation page')}
            </Link>
            {t(' and views on the Learn More/Install modal on the ')}
            <Link to={"/settings/" + orgId + "/integrations/"}>{t('integrations page')}</Link>
          </StyledFooter>
        </PanelFooter>
      </Panel>);
    };
    SentryApplicationDashboard.prototype.renderComponentInteractions = function () {
        var componentInteractions = this.state.interactions.componentInteractions;
        var componentInteractionsDetails = {
            'stacktrace-link': t('Each link click or context menu open counts as one interaction'),
            'issue-link': t('Each open of the issue link modal counts as one interaction'),
        };
        return (<Panel>
        <PanelHeader>{t('Component Interactions')}</PanelHeader>

        <PanelBody>
          <InteractionsChart data={componentInteractions}/>
        </PanelBody>

        <PanelFooter>
          <StyledFooter>
            {Object.keys(componentInteractions).map(function (component, idx) {
            return componentInteractionsDetails[component] && (<React.Fragment key={idx}>
                    <strong>{component + ": "}</strong>
                    {componentInteractionsDetails[component]}
                    <br />
                  </React.Fragment>);
        })}
          </StyledFooter>
        </PanelFooter>
      </Panel>);
    };
    SentryApplicationDashboard.prototype.renderBody = function () {
        var app = this.state.app;
        return (<div>
        <SettingsPageHeader title={t('Integration Dashboard') + " - " + app.name}/>
        {app.status === 'published' && this.renderInstallData()}
        {app.status === 'published' && this.renderIntegrationViews()}
        {app.schema.elements && this.renderComponentInteractions()}
        <RequestLog app={app}/>
      </div>);
    };
    return SentryApplicationDashboard;
}(AsyncView));
export default SentryApplicationDashboard;
var InteractionsChart = function (_a) {
    var data = _a.data;
    var elementInteractionsSeries = Object.keys(data).map(function (key) {
        var seriesData = data[key].map(function (point) { return ({
            value: point[1],
            name: point[0] * 1000,
        }); });
        return {
            seriesName: key,
            data: seriesData,
        };
    });
    return (<ChartWrapper>
      <LineChart isGroupedByDate series={elementInteractionsSeries} grid={{ left: space(4), right: space(4) }} legend={{
        show: true,
        orient: 'horizontal',
        data: Object.keys(data),
    }}/>
    </ChartWrapper>);
};
var Row = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StatsSection = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(4));
var StatsHeader = styled('h6')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: 12px;\n  text-transform: uppercase;\n  color: ", ";\n"], ["\n  margin-bottom: ", ";\n  font-size: 12px;\n  text-transform: uppercase;\n  color: ", ";\n"])), space(1), function (p) { return p.theme.subText; });
var StyledFooter = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(1.5));
var ChartWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(3));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map