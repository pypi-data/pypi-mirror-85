import { __extends, __read } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import LoadingError from 'app/components/loadingError';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import MiniBarChart from 'app/components/charts/miniBarChart';
import theme from 'app/utils/theme';
var STAT_OPS = {
    'browser-extensions': { title: t('Browser Extension'), color: theme.gray200 },
    cors: { title: 'CORS', color: theme.orange400 },
    'error-message': { title: t('Error Message'), color: theme.purple300 },
    'discarded-hash': { title: t('Discarded Issue'), color: theme.gray200 },
    'invalid-csp': { title: t('Invalid CSP'), color: theme.blue300 },
    'ip-address': { title: t('IP Address'), color: theme.red200 },
    'legacy-browsers': { title: t('Legacy Browser'), color: theme.gray200 },
    localhost: { title: t('Localhost'), color: theme.blue300 },
    'release-version': { title: t('Release'), color: theme.purple200 },
    'web-crawlers': { title: t('Web Crawler'), color: theme.red300 },
};
var ProjectFiltersChart = /** @class */ (function (_super) {
    __extends(ProjectFiltersChart, _super);
    function ProjectFiltersChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            statsError: false,
            formattedData: [],
            blankStats: true,
        };
        _this.fetchData = function () {
            _this.getFilterStats();
        };
        return _this;
    }
    ProjectFiltersChart.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectFiltersChart.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    ProjectFiltersChart.prototype.formatData = function (rawData) {
        var _this = this;
        var seriesWithData = new Set();
        var transformed = Object.keys(STAT_OPS).map(function (stat) { return ({
            data: rawData[stat].map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], value = _b[1];
                if (value > 0) {
                    seriesWithData.add(STAT_OPS[stat].title);
                    _this.setState({ blankStats: false });
                }
                return { name: timestamp * 1000, value: value };
            }),
            seriesName: STAT_OPS[stat].title,
            color: STAT_OPS[stat].color,
        }); });
        return transformed.filter(function (series) { return seriesWithData.has(series.seriesName); });
    };
    ProjectFiltersChart.prototype.getFilterStats = function () {
        var _this = this;
        var statOptions = Object.keys(STAT_OPS);
        var project = this.props.project;
        var orgId = this.props.params.orgId;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        var statEndpoint = "/projects/" + orgId + "/" + project.slug + "/stats/";
        var query = {
            since: since,
            until: until,
            resolution: '1d',
        };
        var requests = statOptions.map(function (stat) {
            return _this.props.api.requestPromise(statEndpoint, {
                query: Object.assign({ stat: stat }, query),
            });
        });
        Promise.all(requests)
            .then(function (results) {
            var rawStatsData = {};
            for (var i = 0; i < statOptions.length; i++) {
                rawStatsData[statOptions[i]] = results[i];
            }
            _this.setState({
                formattedData: _this.formatData(rawStatsData),
                error: false,
                loading: false,
            });
        })
            .catch(function () {
            _this.setState({ error: true, loading: false });
        });
    };
    ProjectFiltersChart.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error, formattedData = _a.formattedData;
        var isLoading = loading || !formattedData;
        var hasError = !isLoading && error;
        var hasLoaded = !isLoading && !error;
        var colors = formattedData
            ? formattedData.map(function (series) { return series.color || theme.gray200; })
            : undefined;
        return (<Panel>
        <PanelHeader>{t('Errors filtered in the last 30 days (by day)')}</PanelHeader>

        <PanelBody withPadding>
          {isLoading && <Placeholder height="100px"/>}
          {hasError && <LoadingError onRetry={this.fetchData}/>}
          {hasLoaded && !this.state.blankStats && (<MiniBarChart series={formattedData} colors={colors} height={100} isGroupedByDate stacked labelYAxisExtents/>)}
          {hasLoaded && this.state.blankStats && (<EmptyMessage title={t('Nothing filtered in the last 30 days.')} description={t('Issues filtered as a result of your settings below will be shown here.')}/>)}
        </PanelBody>
      </Panel>);
    };
    return ProjectFiltersChart;
}(React.Component));
export { ProjectFiltersChart };
export default withApi(ProjectFiltersChart);
//# sourceMappingURL=projectFiltersChart.jsx.map