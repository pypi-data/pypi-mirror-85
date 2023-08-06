import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import React from 'react';
import * as queryString from 'query-string';
import { t } from 'app/locale';
import space from 'app/styles/space';
import GroupingActions from 'app/actions/groupingActions';
import GroupingStore from 'app/stores/groupingStore';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import ButtonBar from 'app/components/buttonBar';
import Button from 'app/components/button';
import Alert from 'app/components/alert';
import { callIfFunction } from 'app/utils/callIfFunction';
import List from './list';
var SimilarStackTrace = /** @class */ (function (_super) {
    __extends(SimilarStackTrace, _super);
    function SimilarStackTrace() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            similarItems: [],
            filteredSimilarItems: [],
            similarLinks: null,
            loading: true,
            error: false,
            v2: false,
        };
        _this.onGroupingChange = function (_a) {
            var mergedParent = _a.mergedParent, similarItems = _a.similarItems, similarLinks = _a.similarLinks, filteredSimilarItems = _a.filteredSimilarItems, loading = _a.loading, error = _a.error;
            if (similarItems) {
                _this.setState({
                    similarItems: similarItems,
                    similarLinks: similarLinks,
                    filteredSimilarItems: filteredSimilarItems,
                    loading: loading !== null && loading !== void 0 ? loading : false,
                    error: error !== null && error !== void 0 ? error : false,
                });
                return;
            }
            if (!mergedParent) {
                return;
            }
            if (mergedParent !== _this.props.params.groupId) {
                var params = _this.props.params;
                // Merge success, since we can't specify target, we need to redirect to new parent
                browserHistory.push("/organizations/" + params.orgId + "/issues/" + mergedParent + "/similar/");
                return;
            }
            return;
        };
        _this.listener = GroupingStore.listen(_this.onGroupingChange, undefined);
        _this.handleMerge = function () {
            var _a = _this.props, params = _a.params, location = _a.location;
            var query = location.query;
            if (!params) {
                return;
            }
            // You need at least 1 similarItem OR filteredSimilarItems to be able to merge,
            // so `firstIssue` should always exist from one of those lists.
            //
            // Similar issues API currently does not return issues across projects,
            // so we can assume that the first issues project slug is the project in
            // scope
            var _b = __read(_this.state.similarItems.length
                ? _this.state.similarItems
                : _this.state.filteredSimilarItems, 1), firstIssue = _b[0];
            GroupingActions.merge({
                params: params,
                query: query,
                projectId: firstIssue.issue.project.slug,
            });
        };
        _this.toggleSimilarityVersion = function () {
            _this.setState(function (prevState) { return ({ v2: !prevState.v2 }); }, _this.fetchData);
        };
        return _this;
    }
    SimilarStackTrace.prototype.componentDidMount = function () {
        this.fetchData();
    };
    SimilarStackTrace.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.params.groupId !== this.props.params.groupId ||
            nextProps.location.search !== this.props.location.search) {
            this.fetchData();
        }
    };
    SimilarStackTrace.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    SimilarStackTrace.prototype.fetchData = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        this.setState({ loading: true, error: false });
        var reqs = [];
        if (this.hasSimilarityFeature()) {
            var version = this.state.v2 ? '2' : '1';
            reqs.push({
                endpoint: "/issues/" + params.groupId + "/similar/?" + queryString.stringify(__assign(__assign({}, location.query), { limit: 50, version: version })),
                dataKey: 'similar',
                version: version,
            });
        }
        GroupingActions.fetch(reqs);
    };
    SimilarStackTrace.prototype.hasSimilarityV2Feature = function () {
        return this.props.project.features.includes('similarity-view-v2');
    };
    SimilarStackTrace.prototype.hasSimilarityFeature = function () {
        return this.props.project.features.includes('similarity-view');
    };
    SimilarStackTrace.prototype.render = function () {
        var _a = this.props, params = _a.params, project = _a.project;
        var orgId = params.orgId, groupId = params.groupId;
        var _b = this.state, similarItems = _b.similarItems, filteredSimilarItems = _b.filteredSimilarItems, loading = _b.loading, error = _b.error, v2 = _b.v2, similarLinks = _b.similarLinks;
        var hasV2 = this.hasSimilarityV2Feature();
        var isLoading = loading;
        var isError = error && !isLoading;
        var isLoadedSuccessfully = !isError && !isLoading;
        var hasSimilarItems = this.hasSimilarityFeature() &&
            (similarItems.length >= 0 || filteredSimilarItems.length >= 0) &&
            isLoadedSuccessfully;
        return (<React.Fragment>
        <Alert type="warning">
          {t('This is an experimental feature. Data may not be immediately available while we process merges.')}
        </Alert>
        <HeaderWrapper>
          <Title>{t('Issues with a similar stack trace')}</Title>
          {hasV2 && (<ButtonBar merged active={v2 ? 'new' : 'old'}>
              <Button barId="old" size="small" onClick={this.toggleSimilarityVersion}>
                {t('Old Algorithm')}
              </Button>
              <Button barId="new" size="small" onClick={this.toggleSimilarityVersion}>
                {t('New Algorithm')}
              </Button>
            </ButtonBar>)}
        </HeaderWrapper>
        {isLoading && <LoadingIndicator />}
        {isError && (<LoadingError message={t('Unable to load similar issues, please try again later')} onRetry={this.fetchData}/>)}
        {hasSimilarItems && (<List items={similarItems} filteredItems={filteredSimilarItems} onMerge={this.handleMerge} orgId={orgId} project={project} groupId={groupId} pageLinks={similarLinks}/>)}
      </React.Fragment>);
    };
    return SimilarStackTrace;
}(React.Component));
export default SimilarStackTrace;
var Title = styled('h4')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var HeaderWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map