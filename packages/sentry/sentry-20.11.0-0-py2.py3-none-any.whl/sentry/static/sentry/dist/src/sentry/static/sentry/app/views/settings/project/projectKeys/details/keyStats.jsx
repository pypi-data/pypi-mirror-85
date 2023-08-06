import { __extends } from "tslib";
import React from 'react';
import theme from 'app/utils/theme';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import LoadingError from 'app/components/loadingError';
import Placeholder from 'app/components/placeholder';
import MiniBarChart from 'app/components/charts/miniBarChart';
var getInitialState = function () {
    var until = Math.floor(new Date().getTime() / 1000);
    return {
        since: until - 3600 * 24 * 30,
        until: until,
        loading: true,
        error: false,
        series: [],
        emptyStats: false,
    };
};
var KeyStats = /** @class */ (function (_super) {
    __extends(KeyStats, _super);
    function KeyStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = getInitialState();
        _this.fetchData = function () {
            var _a = _this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/stats/", {
                query: {
                    since: _this.state.since,
                    until: _this.state.until,
                    resolution: '1d',
                },
                success: function (data) {
                    var emptyStats = true;
                    var dropped = [];
                    var accepted = [];
                    data.forEach(function (p) {
                        if (p.total) {
                            emptyStats = false;
                        }
                        dropped.push({ name: p.ts * 1000, value: p.dropped });
                        accepted.push({ name: p.ts * 1000, value: p.accepted });
                    });
                    var series = [
                        {
                            seriesName: t('Accepted'),
                            data: accepted,
                        },
                        {
                            seriesName: t('Rate Limited'),
                            data: dropped,
                        },
                    ];
                    _this.setState({
                        series: series,
                        emptyStats: emptyStats,
                        error: false,
                        loading: false,
                    });
                },
                error: function () {
                    _this.setState({ error: true, loading: false });
                },
            });
        };
        return _this;
    }
    KeyStats.prototype.componentDidMount = function () {
        this.fetchData();
    };
    KeyStats.prototype.render = function () {
        if (this.state.error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        return (<Panel>
        <PanelHeader>{t('Key usage in the last 30 days (by day)')}</PanelHeader>
        <PanelBody withPadding>
          {this.state.loading ? (<Placeholder height="150px"/>) : !this.state.emptyStats ? (<MiniBarChart isGroupedByDate series={this.state.series} height={150} colors={[theme.gray200, theme.red300]} stacked labelYAxisExtents/>) : (<EmptyMessage title={t('Nothing recorded in the last 30 days.')} description={t('Total events captured using these credentials.')}/>)}
        </PanelBody>
      </Panel>);
    };
    return KeyStats;
}(React.Component));
export default KeyStats;
//# sourceMappingURL=keyStats.jsx.map