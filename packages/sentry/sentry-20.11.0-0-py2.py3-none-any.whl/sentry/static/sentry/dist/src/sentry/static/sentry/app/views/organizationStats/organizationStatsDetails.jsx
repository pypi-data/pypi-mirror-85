import { __extends } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import ProjectTable from 'app/views/organizationStats/projectTable';
import TextBlock from 'app/views/settings/components/text/textBlock';
import PageHeading from 'app/components/pageHeading';
import { ProjectTableLayout, ProjectTableDataElement, } from 'app/views/organizationStats/projectTableLayout';
import MiniBarChart from 'app/components/charts/miniBarChart';
import { PageContent } from 'app/styles/organization';
import PerformanceAlert from 'app/views/organizationStats/performanceAlert';
var OrganizationStats = /** @class */ (function (_super) {
    __extends(OrganizationStats, _super);
    function OrganizationStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationStats.prototype.renderContent = function () {
        var _a = this.props, statsLoading = _a.statsLoading, orgTotal = _a.orgTotal, statsError = _a.statsError, orgSeries = _a.orgSeries, projectsLoading = _a.projectsLoading, projectTotals = _a.projectTotals, projectMap = _a.projectMap, projectsError = _a.projectsError, organization = _a.organization;
        var colors = orgSeries === null || orgSeries === void 0 ? void 0 : orgSeries.map(function (series) { return series.color || ''; });
        return (<div>
        <PageHeading withMargins>{t('Organization Stats')}</PageHeading>
        <div className="row">
          <div className="col-md-9">
            <TextBlock>
              {t("The chart below reflects events the system has received\n                across your entire organization. Events are broken down into\n                three categories: Accepted, Rate Limited, and Filtered. Rate\n                Limited events are entries that the system threw away due to quotas\n                being hit, and Filtered events are events that were blocked\n                due to your inbound data filter rules.")}
            </TextBlock>
          </div>
          {orgTotal && (<div className="col-md-3 stats-column">
              <h6 className="nav-header">{t('Events per minute')}</h6>
              <p className="count">{orgTotal.avgRate}</p>
            </div>)}
        </div>
        <div>
          <PerformanceAlert />
          {statsLoading ? (<LoadingIndicator />) : statsError ? (<LoadingError />) : (<Panel>
              <PanelBody withPadding>
                <MiniBarChart isGroupedByDate showTimeInTooltip labelYAxisExtents stacked height={150} colors={colors} series={orgSeries !== null && orgSeries !== void 0 ? orgSeries : undefined}/>
              </PanelBody>
            </Panel>)}
        </div>

        <Panel>
          <PanelHeader>
            <ProjectTableLayout>
              <div>{t('Project')}</div>
              <ProjectTableDataElement>{t('Accepted')}</ProjectTableDataElement>
              <ProjectTableDataElement>{t('Rate Limited')}</ProjectTableDataElement>
              <ProjectTableDataElement>{t('Filtered')}</ProjectTableDataElement>
              <ProjectTableDataElement>{t('Total')}</ProjectTableDataElement>
            </ProjectTableLayout>
          </PanelHeader>
          <PanelBody>
            {!orgTotal || !projectTotals || statsLoading || projectsLoading ? (<LoadingIndicator />) : projectsError ? (<LoadingError />) : (<ProjectTable projectTotals={projectTotals} orgTotal={orgTotal} organization={organization} projectMap={projectMap}/>)}
          </PanelBody>
        </Panel>
        {this.props.pageLinks && <Pagination {...this.props}/>}
      </div>);
    };
    OrganizationStats.prototype.render = function () {
        return <PageContent>{this.renderContent()}</PageContent>;
    };
    return OrganizationStats;
}(React.Component));
export default OrganizationStats;
//# sourceMappingURL=organizationStatsDetails.jsx.map