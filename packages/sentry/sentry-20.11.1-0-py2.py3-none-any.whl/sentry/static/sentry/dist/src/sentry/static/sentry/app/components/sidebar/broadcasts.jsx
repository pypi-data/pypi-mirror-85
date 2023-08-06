import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { getAllBroadcasts, markBroadcastsAsSeen } from 'app/actionCreators/broadcasts';
import { t } from 'app/locale';
import LoadingIndicator from 'app/components/loadingIndicator';
import SidebarItem from 'app/components/sidebar/sidebarItem';
import SidebarPanel from 'app/components/sidebar/sidebarPanel';
import SidebarPanelEmpty from 'app/components/sidebar/sidebarPanelEmpty';
import SidebarPanelItem from 'app/components/sidebar/sidebarPanelItem';
import { IconBroadcast } from 'app/icons';
import withApi from 'app/utils/withApi';
var MARK_SEEN_DELAY = 1000;
var POLLER_DELAY = 600000; // 10 minute poll (60 * 10 * 1000)
var Broadcasts = /** @class */ (function (_super) {
    __extends(Broadcasts, _super);
    function Broadcasts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            broadcasts: [],
            loading: true,
            error: false,
        };
        _this.poller = null;
        _this.timer = null;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var data, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (this.poller) {
                            this.stopPoll();
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, getAllBroadcasts(this.props.api, this.props.organization.slug)];
                    case 2:
                        data = _b.sent();
                        this.setState({ loading: false, broadcasts: data || [] });
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        this.setState({ loading: false, error: true });
                        return [3 /*break*/, 4];
                    case 4:
                        this.startPoll();
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * If tab/window loses visibility (note: this is different than focus), stop
         * polling for broadcasts data, otherwise, if it gains visibility, start
         * polling again.
         */
        _this.handleVisibilityChange = function () { return (document.hidden ? _this.stopPoll() : _this.startPoll()); };
        _this.handleShowPanel = function () {
            _this.timer = window.setTimeout(_this.markSeen, MARK_SEEN_DELAY);
            _this.props.onShowPanel();
        };
        _this.markSeen = function () { return __awaiter(_this, void 0, void 0, function () {
            var unseenBroadcastIds;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        unseenBroadcastIds = this.unseenIds;
                        if (unseenBroadcastIds.length === 0) {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, markBroadcastsAsSeen(this.props.api, unseenBroadcastIds)];
                    case 1:
                        _a.sent();
                        this.setState(function (state) { return ({
                            broadcasts: state.broadcasts.map(function (item) { return (__assign(__assign({}, item), { hasSeen: true })); }),
                        }); });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Broadcasts.prototype.componentDidMount = function () {
        this.fetchData();
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
    };
    Broadcasts.prototype.componentWillUnmount = function () {
        if (this.timer) {
            window.clearTimeout(this.timer);
            this.timer = null;
        }
        if (this.poller) {
            this.stopPoll();
        }
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
    };
    Broadcasts.prototype.startPoll = function () {
        this.poller = window.setTimeout(this.fetchData, POLLER_DELAY);
    };
    Broadcasts.prototype.stopPoll = function () {
        if (this.poller) {
            window.clearTimeout(this.poller);
            this.poller = null;
        }
    };
    Object.defineProperty(Broadcasts.prototype, "unseenIds", {
        get: function () {
            return this.state.broadcasts
                ? this.state.broadcasts.filter(function (item) { return !item.hasSeen; }).map(function (item) { return item.id; })
                : [];
        },
        enumerable: false,
        configurable: true
    });
    Broadcasts.prototype.render = function () {
        var _a = this.props, orientation = _a.orientation, collapsed = _a.collapsed, currentPanel = _a.currentPanel, showPanel = _a.showPanel, hidePanel = _a.hidePanel;
        var _b = this.state, broadcasts = _b.broadcasts, loading = _b.loading;
        var unseenPosts = this.unseenIds;
        return (<React.Fragment>
        <SidebarItem data-test-id="sidebar-broadcasts" orientation={orientation} collapsed={collapsed} active={currentPanel === 'broadcasts'} badge={unseenPosts.length} icon={<IconBroadcast size="md"/>} label={t("What's new")} onClick={this.handleShowPanel} id="broadcasts"/>

        {showPanel && currentPanel === 'broadcasts' && (<SidebarPanel data-test-id="sidebar-broadcasts-panel" orientation={orientation} collapsed={collapsed} title={t("What's new in Sentry")} hidePanel={hidePanel}>
            {loading ? (<LoadingIndicator />) : broadcasts.length === 0 ? (<SidebarPanelEmpty>
                {t('No recent updates from the Sentry team.')}
              </SidebarPanelEmpty>) : (broadcasts.map(function (item) { return (<SidebarPanelItem key={item.id} hasSeen={item.hasSeen} title={item.title} message={item.message} link={item.link} cta={item.cta}/>); }))}
          </SidebarPanel>)}
      </React.Fragment>);
    };
    return Broadcasts;
}(React.Component));
export default withApi(Broadcasts);
//# sourceMappingURL=broadcasts.jsx.map