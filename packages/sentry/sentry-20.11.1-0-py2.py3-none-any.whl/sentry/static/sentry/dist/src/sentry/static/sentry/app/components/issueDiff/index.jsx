import { __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import LoadingIndicator from 'app/components/loadingIndicator';
import getStacktraceBody from 'app/utils/getStacktraceBody';
import ButtonBar from 'app/components/buttonBar';
import Button from 'app/components/button';
import space from 'app/styles/space';
import renderGroupingInfo from './renderGroupingInfo';
var defaultProps = {
    baseEventId: 'latest',
    targetEventId: 'latest',
};
var IssueDiff = /** @class */ (function (_super) {
    __extends(IssueDiff, _super);
    function IssueDiff() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            groupingDiff: false,
            baseEvent: [],
            targetEvent: [],
            // `SplitDiffAsync` is an async-loaded component
            // This will eventually contain a reference to the exported component from `./splitDiff`
            SplitDiffAsync: undefined,
        };
        _this.toggleDiffMode = function () {
            _this.setState(function (state) { return ({ groupingDiff: !state.groupingDiff, loading: true }); }, _this.fetchData);
        };
        _this.fetchEventData = function (issueId, eventId) { return __awaiter(_this, void 0, void 0, function () {
            var _a, orgId, project, api, groupingDiff, paramEventId, event_1, groupingInfo, event;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, orgId = _a.orgId, project = _a.project, api = _a.api;
                        groupingDiff = this.state.groupingDiff;
                        paramEventId = eventId;
                        if (!(eventId === 'latest')) return [3 /*break*/, 2];
                        return [4 /*yield*/, api.requestPromise("/issues/" + issueId + "/events/latest/")];
                    case 1:
                        event_1 = _b.sent();
                        paramEventId = event_1.eventID;
                        _b.label = 2;
                    case 2:
                        if (!groupingDiff) return [3 /*break*/, 4];
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + project.slug + "/events/" + paramEventId + "/grouping-info/")];
                    case 3:
                        groupingInfo = _b.sent();
                        return [2 /*return*/, renderGroupingInfo(groupingInfo)];
                    case 4: return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + project.slug + "/events/" + paramEventId + "/")];
                    case 5:
                        event = _b.sent();
                        return [2 /*return*/, getStacktraceBody(event)];
                }
            });
        }); };
        return _this;
    }
    IssueDiff.prototype.componentDidMount = function () {
        this.fetchData();
    };
    IssueDiff.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, baseIssueId = _a.baseIssueId, targetIssueId = _a.targetIssueId, baseEventId = _a.baseEventId, targetEventId = _a.targetEventId;
        // Fetch component and event data
        Promise.all([
            import(/* webpackChunkName: "splitDiff" */ '../splitDiff'),
            this.fetchEventData(baseIssueId, baseEventId !== null && baseEventId !== void 0 ? baseEventId : 'latest'),
            this.fetchEventData(targetIssueId, targetEventId !== null && targetEventId !== void 0 ? targetEventId : 'latest'),
        ])
            .then(function (_a) {
            var _b = __read(_a, 3), SplitDiffAsync = _b[0].default, baseEvent = _b[1], targetEvent = _b[2];
            _this.setState({
                SplitDiffAsync: SplitDiffAsync,
                baseEvent: baseEvent,
                targetEvent: targetEvent,
                loading: false,
            });
        })
            .catch(function () {
            addErrorMessage(t('Error loading events'));
        });
    };
    IssueDiff.prototype.render = function () {
        var _a = this.props, className = _a.className, project = _a.project;
        var _b = this.state, DiffComponent = _b.SplitDiffAsync, loading = _b.loading, groupingDiff = _b.groupingDiff, baseEvent = _b.baseEvent, targetEvent = _b.targetEvent;
        var showDiffToggle = project.features.includes('similarity-view-v2');
        return (<StyledIssueDiff className={className} loading={loading}>
        {loading && <LoadingIndicator />}
        {!loading && showDiffToggle && (<HeaderWrapper>
            <ButtonBar merged active={groupingDiff ? 'grouping' : 'event'}>
              <Button barId="event" size="small" onClick={this.toggleDiffMode}>
                {t('Diff stack trace and message')}
              </Button>
              <Button barId="grouping" size="small" onClick={this.toggleDiffMode}>
                {t('Diff grouping information')}
              </Button>
            </ButtonBar>
          </HeaderWrapper>)}
        {!loading &&
            DiffComponent &&
            baseEvent.map(function (value, i) {
                var _a;
                return (<DiffComponent key={i} base={value} target={(_a = targetEvent[i]) !== null && _a !== void 0 ? _a : ''} type="words"/>);
            })}
      </StyledIssueDiff>);
    };
    IssueDiff.defaultProps = defaultProps;
    return IssueDiff;
}(React.Component));
export default withApi(IssueDiff);
// required for tests which do not provide API as context
export { IssueDiff };
var StyledIssueDiff = styled('div', {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'loading'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  overflow: auto;\n  padding: ", ";\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  ", ";\n"], ["\n  background-color: ", ";\n  overflow: auto;\n  padding: ", ";\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  ",
    ";\n"])), function (p) { return p.theme.backgroundSecondary; }, space(1), function (p) {
    return p.loading &&
        "\n        background-color: " + p.theme.background + ";\n        justify-content: center;\n      ";
});
var HeaderWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map