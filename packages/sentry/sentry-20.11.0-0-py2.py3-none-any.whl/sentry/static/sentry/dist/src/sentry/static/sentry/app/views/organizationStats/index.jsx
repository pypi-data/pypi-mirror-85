import { __extends } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import theme from 'app/utils/theme';
import OrganizationStatsDetails from './organizationStatsDetails';
var OrganizationStatsContainer = /** @class */ (function (_super) {
    __extends(OrganizationStatsContainer, _super);
    function OrganizationStatsContainer(props) {
        var _this = _super.call(this, props) || this;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 7;
        _this.state = {
            projectsError: false,
            projectsLoading: false,
            projectsRequestsPending: 0,
            statsError: false,
            statsLoading: false,
            statsRequestsPending: 0,
            projectMap: {},
            rawProjectData: { received: {}, rejected: {}, blacklisted: {} },
            rawOrgData: { received: [], rejected: [], blacklisted: [] },
            orgSeries: null,
            orgTotal: null,
            projectTotals: null,
            querySince: since,
            queryUntil: until,
            pageLinks: null,
        };
        return _this;
    }
    OrganizationStatsContainer.prototype.UNSAFE_componentWillMount = function () {
        this.fetchData();
    };
    OrganizationStatsContainer.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // If query string changes, it will be due to pagination.
        // Intentionally only fetch projects since stats are fetched for a fixed period during
        // the initial payload
        if (nextProps.location.search !== this.props.location.search) {
            this.setState({
                projectsError: false,
                projectsRequestsPending: 1,
                projectsLoading: true,
            });
        }
    };
    OrganizationStatsContainer.prototype.componentDidUpdate = function (prevProps) {
        var prevParams = prevProps.params, currentParams = this.props.params;
        if (prevParams.orgId !== currentParams.orgId) {
            this.fetchData();
        }
        // Query string is changed, probably due to pagination, re-fetch only project data
        if (prevProps.location.search !== this.props.location.search) {
            // Not sure why, but when we use pagination and the new results load and re-render,
            // the scroll position does not reset to top like in Audit Log
            if (window.scrollTo) {
                window.scrollTo(0, 0);
            }
            this.fetchProjectData();
        }
        var state = this.state;
        if (state.statsLoading && !state.statsRequestsPending) {
            this.processOrgData();
        }
        if (state.projectsLoading && !state.projectsRequestsPending) {
            this.processProjectData();
        }
    };
    OrganizationStatsContainer.prototype.fetchProjectData = function () {
        var _this = this;
        this.props.api.request(this.getOrganizationProjectsEndpoint(), {
            query: this.props.location.query,
            success: function (data, _textStatus, jqxhr) {
                var projectMap = {};
                data.forEach(function (project) {
                    projectMap[project.id] = project;
                });
                _this.setState(function (prevState) { return ({
                    pageLinks: jqxhr ? jqxhr.getResponseHeader('Link') : null,
                    projectMap: projectMap,
                    projectsRequestsPending: prevState.projectsRequestsPending - 1,
                }); });
            },
            error: function () {
                _this.setState({
                    projectsError: true,
                });
            },
        });
    };
    OrganizationStatsContainer.prototype.fetchData = function () {
        var _this = this;
        this.setState({
            statsError: false,
            statsLoading: true,
            statsRequestsPending: 3,
            projectsError: false,
            projectsLoading: true,
            projectsRequestsPending: 4,
        });
        var statEndpoint = this.getOrganizationStatsEndpoint();
        Object.keys(this.state.rawOrgData).forEach(function (statName) {
            _this.props.api.request(statEndpoint, {
                query: {
                    since: _this.state.querySince,
                    until: _this.state.queryUntil,
                    resolution: '1h',
                    stat: statName,
                },
                success: function (data) {
                    _this.setState(function (prevState) {
                        var rawOrgData = prevState.rawOrgData;
                        rawOrgData[statName] = data;
                        return {
                            rawOrgData: rawOrgData,
                            statsRequestsPending: prevState.statsRequestsPending - 1,
                        };
                    });
                },
                error: function () {
                    _this.setState({
                        statsError: true,
                    });
                },
            });
        });
        Object.keys(this.state.rawProjectData).forEach(function (statName) {
            _this.props.api.request(statEndpoint, {
                query: {
                    since: _this.state.querySince,
                    until: _this.state.queryUntil,
                    stat: statName,
                    group: 'project',
                },
                success: function (data) {
                    _this.setState(function (prevState) {
                        var rawProjectData = prevState.rawProjectData;
                        rawProjectData[statName] = data;
                        return {
                            rawProjectData: rawProjectData,
                            projectsRequestsPending: prevState.projectsRequestsPending - 1,
                        };
                    });
                },
                error: function () {
                    _this.setState({
                        projectsError: true,
                    });
                },
            });
        });
        this.fetchProjectData();
    };
    OrganizationStatsContainer.prototype.getOrganizationStatsEndpoint = function () {
        var params = this.props.params;
        return '/organizations/' + params.orgId + '/stats/';
    };
    OrganizationStatsContainer.prototype.getOrganizationProjectsEndpoint = function () {
        var params = this.props.params;
        return '/organizations/' + params.orgId + '/projects/';
    };
    OrganizationStatsContainer.prototype.processOrgData = function () {
        var oReceived = 0;
        var oRejected = 0;
        var oBlacklisted = 0;
        var aReceived = [0, 0]; // received, points
        var rawOrgData = this.state.rawOrgData;
        var orgAccepted = {
            seriesName: t('Accepted'),
            color: theme.gray200,
            data: [],
        };
        var orgRejected = {
            seriesName: t('Rate limited'),
            color: theme.red300,
            data: [],
        };
        var orgFiltered = {
            seriesName: t('Filtered'),
            color: theme.orange400,
            data: [],
        };
        rawOrgData.received.forEach(function (point, idx) {
            var dReceived = point[1];
            var dRejected = rawOrgData.rejected[idx][1];
            var dFiltered = rawOrgData.blacklisted[idx][1];
            var dAccepted = Math.max(0, dReceived - dRejected - dFiltered);
            var time = point[0] * 1000;
            orgAccepted.data.push({ name: time, value: dAccepted });
            orgRejected.data.push({ name: time, value: dRejected });
            orgFiltered.data.push({ name: time, value: dFiltered });
            oReceived += dReceived;
            oRejected += dRejected;
            oBlacklisted += dFiltered;
            if (dReceived > 0) {
                aReceived[0] += dReceived;
                aReceived[1] += 1;
            }
        });
        this.setState({
            orgSeries: [orgAccepted, orgRejected, orgFiltered],
            orgTotal: {
                id: '',
                received: oReceived,
                rejected: oRejected,
                blacklisted: oBlacklisted,
                accepted: Math.max(0, oReceived - oRejected - oBlacklisted),
                avgRate: aReceived[1] ? Math.round(aReceived[0] / aReceived[1] / 60) : 0,
            },
            statsLoading: false,
        });
    };
    OrganizationStatsContainer.prototype.processProjectData = function () {
        var rawProjectData = this.state.rawProjectData;
        var projectTotals = [];
        Object.keys(rawProjectData.received).forEach(function (projectId) {
            var data = rawProjectData.received[projectId];
            var pReceived = 0;
            var pRejected = 0;
            var pBlacklisted = 0;
            data.forEach(function (point, idx) {
                pReceived += point[1];
                pRejected += rawProjectData.rejected[projectId][idx][1];
                pBlacklisted += rawProjectData.blacklisted[projectId][idx][1];
            });
            projectTotals.push({
                id: projectId,
                received: pReceived,
                rejected: pRejected,
                blacklisted: pBlacklisted,
                accepted: Math.max(0, pReceived - pRejected - pBlacklisted),
            });
        });
        this.setState({
            projectTotals: projectTotals,
            projectsLoading: false,
        });
    };
    OrganizationStatsContainer.prototype.render = function () {
        var organization = this.props.organization;
        return (<DocumentTitle title={"Stats - " + organization.slug + " - Sentry"}>
        <OrganizationStatsDetails organization={organization} {...this.state}/>
      </DocumentTitle>);
    };
    return OrganizationStatsContainer;
}(React.Component));
export { OrganizationStatsContainer };
export default withApi(withOrganization(OrganizationStatsContainer));
//# sourceMappingURL=index.jsx.map