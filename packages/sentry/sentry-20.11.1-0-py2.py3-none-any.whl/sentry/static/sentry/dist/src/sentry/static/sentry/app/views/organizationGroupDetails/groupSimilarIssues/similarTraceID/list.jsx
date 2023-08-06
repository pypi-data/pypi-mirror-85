import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import pick from 'lodash/pick';
import * as Sentry from '@sentry/react';
import styled from '@emotion/styled';
import { tct } from 'app/locale';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import GroupListHeader from 'app/components/issues/groupListHeader';
import { Panel, PanelBody } from 'app/components/panels';
import StreamGroup from 'app/components/stream/group';
import GroupStore from 'app/stores/groupStore';
import Pagination from 'app/components/pagination';
import withApi from 'app/utils/withApi';
import LoadingIndicator from 'app/components/loadingIndicator';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LoadingError from 'app/components/loadingError';
import DateTime from 'app/components/dateTime';
var List = /** @class */ (function (_super) {
    __extends(List, _super);
    function List() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            groups: [],
            hasError: false,
            isLoading: true,
        };
        _this.getGroups = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, orgSlug, location, issues, issuesIds, groups, convertedGroups, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgSlug = _a.orgSlug, location = _a.location, issues = _a.issues;
                        if (!issues.length) {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        issuesIds = issues.map(function (issue) { return "group=" + issue['issue.id']; }).join('&');
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/issues/?" + issuesIds, {
                                method: 'GET',
                                data: __assign({ sort: 'new' }, pick(location.query, __spread(Object.values(URL_PARAM), ['cursor']))),
                            })];
                    case 2:
                        groups = _b.sent();
                        convertedGroups = this.convertGroupsIntoEventFormat(groups);
                        // this is necessary, because the AssigneeSelector component fetches the group from the GroupStore
                        GroupStore.add(convertedGroups);
                        this.setState({ groups: convertedGroups, isLoading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        Sentry.captureException(error_1);
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        // this little hack is necessary until we factored the groupStore or the EventOrGroupHeader component
        // the goal of this function is to insert the properties eventID and groupID, so then the link rendered
        // in the EventOrGroupHeader component will always have the structure '/organization/:orgSlug/issues/:groupId/event/:eventId/',
        // providing a smooth navigation between issues with the same trace ID
        _this.convertGroupsIntoEventFormat = function (groups) {
            var issues = _this.props.issues;
            return groups
                .map(function (group) {
                // the issue must always be found
                var foundIssue = issues.find(function (issue) { return group.id === String(issue['issue.id']); });
                if (foundIssue) {
                    // the eventID is the reason why we need to use the DiscoverQuery component.
                    // At the moment the /issues/ endpoint above doesn't return this information
                    return __assign(__assign({}, group), { eventID: foundIssue.id, groupID: group.id });
                }
                return undefined;
            })
                .filter(function (event) { return !!event; });
        };
        _this.handleRetry = function () {
            _this.getGroups();
        };
        _this.renderContent = function () {
            var _a = _this.props, issues = _a.issues, period = _a.period, traceID = _a.traceID;
            if (!issues.length) {
                return (<EmptyStateWarning small withIcon={false}>
          {tct('No issues with the same trace ID [traceID] were found in the period between [start] and [end]', {
                    traceID: traceID,
                    start: <DateTime date={period.start} timeAndDate/>,
                    end: <DateTime date={period.start} timeAndDate/>,
                })}
        </EmptyStateWarning>);
            }
            return issues.map(function (issue) { return (<StreamGroup key={issue.id} id={String(issue['issue.id'])} canSelect={false} withChart={false}/>); });
        };
        return _this;
    }
    List.prototype.componentDidMount = function () {
        this.getGroups();
    };
    List.prototype.handleCursorChange = function (cursor, path, query, pageDiff) {
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), { cursor: pageDiff <= 0 ? undefined : cursor }),
        });
    };
    List.prototype.render = function () {
        var _a = this.props, pageLinks = _a.pageLinks, traceID = _a.traceID;
        var _b = this.state, isLoading = _b.isLoading, hasError = _b.hasError;
        if (isLoading) {
            return <LoadingIndicator />;
        }
        if (hasError) {
            return (<LoadingError message={tct('An error occurred while fetching issues with the trace ID [traceID]', {
                traceID: traceID,
            })} onRetry={this.handleRetry}/>);
        }
        return (<React.Fragment>
        <StyledPanel>
          <GroupListHeader withChart={false}/>
          <PanelBody>{this.renderContent()}</PanelBody>
        </StyledPanel>
        <StyledPagination pageLinks={pageLinks} onCursor={this.handleCursorChange}/>
      </React.Fragment>);
    };
    return List;
}(React.Component));
export default withApi(List);
var StyledPagination = styled(Pagination)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var StyledPanel = styled(Panel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=list.jsx.map