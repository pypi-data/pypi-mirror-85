import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import withOrganization from 'app/utils/withOrganization';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import { Client } from 'app/api';
import withApi from 'app/utils/withApi';
import { formatVersion } from 'app/utils/formatters';
import routeTitleGen from 'app/utils/routeTitle';
import { Body, Main, Side } from 'app/components/layouts/thirds';
import { restoreRelease } from 'app/actionCreators/release';
import ReleaseChart from './chart/';
import Issues from './issues';
import CommitAuthorBreakdown from './commitAuthorBreakdown';
import ProjectReleaseDetails from './projectReleaseDetails';
import OtherProjects from './otherProjects';
import TotalCrashFreeUsers from './totalCrashFreeUsers';
import Deploys from './deploys';
import ReleaseStatsRequest from './releaseStatsRequest';
import ReleaseArchivedNotice from './releaseArchivedNotice';
import { YAxis } from './chart/releaseChartControls';
import { ReleaseContext } from '..';
import { isReleaseArchived } from '../../utils';
var ReleaseOverview = /** @class */ (function (_super) {
    __extends(ReleaseOverview, _super);
    function ReleaseOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleYAxisChange = function (yAxis) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { yAxis: yAxis }) }));
        };
        _this.handleRestore = function (project, successCallback) { return __awaiter(_this, void 0, void 0, function () {
            var _a, params, organization, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, params = _a.params, organization = _a.organization;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, restoreRelease(new Client(), {
                                orgSlug: organization.slug,
                                projectSlug: project.slug,
                                releaseVersion: params.release,
                            })];
                    case 2:
                        _c.sent();
                        successCallback();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ReleaseOverview.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseOverview.prototype.getYAxis = function (hasHealthData) {
        var yAxis = this.props.location.query.yAxis;
        if (typeof yAxis === 'string') {
            return yAxis;
        }
        if (hasHealthData) {
            return YAxis.SESSIONS;
        }
        return YAxis.EVENTS;
    };
    ReleaseOverview.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection, location = _a.location, api = _a.api, router = _a.router;
        return (<ReleaseContext.Consumer>
        {function (_a) {
            var release = _a.release, project = _a.project, deploys = _a.deploys, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
            var commitCount = release.commitCount, version = release.version;
            var hasHealthData = (project.healthData || {}).hasHealthData;
            var hasDiscover = organization.features.includes('discover-basic');
            var yAxis = _this.getYAxis(hasHealthData);
            return (<ReleaseStatsRequest api={api} orgId={organization.slug} projectSlug={project.slug} version={version} selection={selection} location={location} yAxis={yAxis} hasHealthData={hasHealthData} hasDiscover={hasDiscover}>
              {function (_a) {
                var crashFreeTimeBreakdown = _a.crashFreeTimeBreakdown, releaseStatsProps = __rest(_a, ["crashFreeTimeBreakdown"]);
                return (<StyledBody>
                  <Main>
                    {isReleaseArchived(release) && (<ReleaseArchivedNotice onRestore={function () { return _this.handleRestore(project, refetchData); }}/>)}

                    {(hasDiscover || hasHealthData) && (<ReleaseChart {...releaseStatsProps} selection={selection} yAxis={yAxis} onYAxisChange={_this.handleYAxisChange} router={router} organization={organization} hasHealthData={hasHealthData} location={location} api={api} version={version} hasDiscover={hasDiscover}/>)}

                    <Issues orgId={organization.slug} selection={selection} version={version} location={location}/>
                  </Main>
                  <Side>
                    <ProjectReleaseDetails release={release} releaseMeta={releaseMeta} orgSlug={organization.slug} projectSlug={project.slug}/>
                    {commitCount > 0 && (<CommitAuthorBreakdown version={version} orgId={organization.slug} projectSlug={project.slug}/>)}
                    {releaseMeta.projects.length > 1 && (<OtherProjects projects={releaseMeta.projects.filter(function (p) { return p.slug !== project.slug; })} location={location}/>)}
                    {hasHealthData && (<TotalCrashFreeUsers crashFreeTimeBreakdown={crashFreeTimeBreakdown}/>)}
                    {deploys.length > 0 && (<Deploys version={version} orgSlug={organization.slug} deploys={deploys} projectId={project.id}/>)}
                  </Side>
                </StyledBody>);
            }}
            </ReleaseStatsRequest>);
        }}
      </ReleaseContext.Consumer>);
    };
    return ReleaseOverview;
}(AsyncView));
export default withApi(withGlobalSelection(withOrganization(ReleaseOverview)));
var StyledBody = styled(Body)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: -", " -", ";\n"], ["\n  margin: -", " -", ";\n"])), space(2), space(4));
var templateObject_1;
//# sourceMappingURL=index.jsx.map