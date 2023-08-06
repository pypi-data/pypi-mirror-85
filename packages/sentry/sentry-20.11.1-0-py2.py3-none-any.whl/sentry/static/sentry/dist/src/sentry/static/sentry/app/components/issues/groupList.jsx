import { __assign } from "tslib";
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import { browserHistory } from 'react-router';
import * as qs from 'query-string';
import { Panel, PanelBody } from 'app/components/panels';
import { fetchOrgMembers, indexMembersByProject } from 'app/actionCreators/members';
import { t } from 'app/locale';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import GroupStore from 'app/stores/groupStore';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import StreamGroup from 'app/components/stream/group';
import StreamManager from 'app/utils/streamManager';
import withApi from 'app/utils/withApi';
import Pagination from 'app/components/pagination';
import GroupListHeader from './groupListHeader';
var defaultProps = {
    canSelectGroups: true,
    withChart: true,
    withPagination: true,
};
var GroupList = createReactClass({
    displayName: 'GroupList',
    propTypes: {
        api: PropTypes.object.isRequired,
        query: PropTypes.string.isRequired,
        canSelectGroups: PropTypes.bool,
        withChart: PropTypes.bool,
        orgId: PropTypes.string.isRequired,
        endpointPath: PropTypes.string,
        renderEmptyMessage: PropTypes.func,
        queryParams: PropTypes.object,
        withPagination: PropTypes.bool,
    },
    contextTypes: {
        location: PropTypes.object,
    },
    mixins: [Reflux.listenTo(GroupStore, 'onGroupChange')],
    getInitialState: function () {
        return {
            loading: true,
            error: false,
            groups: [],
        };
    },
    componentWillMount: function () {
        this._streamManager = new StreamManager(GroupStore);
        this.fetchData();
    },
    shouldComponentUpdate: function (nextProps, nextState) {
        return (!isEqual(this.state, nextState) ||
            nextProps.endpointPath !== this.props.endpointPath ||
            nextProps.query !== this.props.query ||
            !isEqual(nextProps.queryParams, this.props.queryParams));
    },
    componentDidUpdate: function (prevProps) {
        if (prevProps.orgId !== this.props.orgId ||
            prevProps.endpointPath !== this.props.endpointPath ||
            prevProps.query !== this.props.query ||
            !isEqual(prevProps.queryParams, this.props.queryParams)) {
            this.fetchData();
        }
    },
    componentWillUnmount: function () {
        GroupStore.loadInitialData([]);
    },
    fetchData: function () {
        var _this = this;
        GroupStore.loadInitialData([]);
        var _a = this.props, api = _a.api, orgId = _a.orgId;
        this.setState({
            loading: true,
            error: false,
        });
        fetchOrgMembers(api, orgId).then(function (members) {
            _this.setState({ memberList: indexMembersByProject(members) });
        });
        api.request(this.getGroupListEndpoint(), {
            success: function (data, _, jqXHR) {
                _this._streamManager.push(data);
                _this.setState({
                    error: false,
                    loading: false,
                    pageLinks: jqXHR.getResponseHeader('Link'),
                });
            },
            error: function () {
                _this.setState({
                    error: true,
                    loading: false,
                });
            },
        });
    },
    getGroupListEndpoint: function () {
        var _a = this.props, orgId = _a.orgId, endpointPath = _a.endpointPath, queryParams = _a.queryParams;
        var path = endpointPath !== null && endpointPath !== void 0 ? endpointPath : "/organizations/" + orgId + "/issues/";
        var queryParameters = queryParams !== null && queryParams !== void 0 ? queryParams : this.getQueryParams();
        return path + "?" + qs.stringify(queryParameters);
    },
    getQueryParams: function () {
        var query = this.props.query;
        var queryParams = this.context.location.query;
        queryParams.limit = 50;
        queryParams.sort = 'new';
        queryParams.query = query;
        return queryParams;
    },
    onCursorChange: function (cursor, path, query, pageDiff) {
        var queryPageInt = parseInt(query.page, 10);
        var nextPage = isNaN(queryPageInt) ? pageDiff : queryPageInt + pageDiff;
        // unset cursor and page when we navigate back to the first page
        // also reset cursor if somehow the previous button is enabled on
        // first page and user attempts to go backwards
        if (nextPage <= 0) {
            cursor = undefined;
            nextPage = undefined;
        }
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), { cursor: cursor }),
        });
    },
    onGroupChange: function () {
        var groups = this._streamManager.getAllItems();
        if (!isEqual(groups, this.state.groups)) {
            this.setState({
                groups: groups,
            });
        }
    },
    render: function () {
        var _a = this.props, canSelectGroups = _a.canSelectGroups, withChart = _a.withChart, renderEmptyMessage = _a.renderEmptyMessage, withPagination = _a.withPagination;
        var _b = this.state, loading = _b.loading, error = _b.error, groups = _b.groups, memberList = _b.memberList, pageLinks = _b.pageLinks;
        if (loading) {
            return <LoadingIndicator />;
        }
        else if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        else if (groups.length === 0) {
            if (typeof renderEmptyMessage === 'function') {
                return renderEmptyMessage();
            }
            return (<Panel>
          <PanelBody>
            <EmptyStateWarning>
              <p>{t("There don't seem to be any events fitting the query.")}</p>
            </EmptyStateWarning>
          </PanelBody>
        </Panel>);
        }
        return (<React.Fragment>
        <Panel>
          <GroupListHeader withChart={withChart}/>
          <PanelBody>
            {groups.map(function (_a) {
            var id = _a.id, project = _a.project;
            var members = memberList && memberList.hasOwnProperty(project.slug)
                ? memberList[project.slug]
                : null;
            return (<StreamGroup key={id} id={id} canSelect={canSelectGroups} withChart={withChart} memberList={members}/>);
        })}
          </PanelBody>
        </Panel>
        {withPagination && (<Pagination pageLinks={pageLinks} onCursor={this.onCursorChange}/>)}
      </React.Fragment>);
    },
});
GroupList.defaultProps = defaultProps;
export { GroupList };
export default withApi(GroupList);
//# sourceMappingURL=groupList.jsx.map