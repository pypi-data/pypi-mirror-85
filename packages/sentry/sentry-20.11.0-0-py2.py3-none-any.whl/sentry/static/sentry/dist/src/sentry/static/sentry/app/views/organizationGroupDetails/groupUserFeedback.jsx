import { __assign, __extends, __read } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import EventUserFeedback from 'app/components/events/userFeedback';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel } from 'app/components/panels';
import Pagination from 'app/components/pagination';
import withOrganization from 'app/utils/withOrganization';
import UserFeedbackEmpty from 'app/views/userFeedback/userFeedbackEmpty';
import { fetchGroupUserReports } from './utils';
var GroupUserFeedback = /** @class */ (function (_super) {
    __extends(GroupUserFeedback, _super);
    function GroupUserFeedback() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            reportList: [],
            pageLinks: '',
        };
        _this.fetchData = function () {
            _this.setState({
                loading: true,
                error: false,
            });
            fetchGroupUserReports(_this.props.group.id, __assign(__assign({}, _this.props.params), { cursor: _this.props.location.query.cursor || '' }))
                .then(function (_a) {
                var _b = __read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
                _this.setState({
                    error: false,
                    loading: false,
                    reportList: data,
                    pageLinks: jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link'),
                });
            })
                .catch(function () {
                _this.setState({
                    error: true,
                    loading: false,
                });
            });
        };
        return _this;
    }
    GroupUserFeedback.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupUserFeedback.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.params, this.props.params) ||
            prevProps.location.pathname !== this.props.location.pathname ||
            prevProps.location.search !== this.props.location.search) {
            this.fetchData();
        }
    };
    GroupUserFeedback.prototype.render = function () {
        var _a = this.state, reportList = _a.reportList, loading = _a.loading, error = _a.error;
        var _b = this.props, organization = _b.organization, group = _b.group;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        if (reportList.length) {
            return (<div className="row">
          <div className="col-md-9">
            {reportList.map(function (item, idx) { return (<EventUserFeedback key={idx} report={item} orgId={organization.slug} issueId={group.id}/>); })}
            <Pagination pageLinks={this.state.pageLinks} {...this.props}/>
          </div>
        </div>);
        }
        return (<Panel>
        <UserFeedbackEmpty projectIds={[group.project.id]}/>
      </Panel>);
    };
    return GroupUserFeedback;
}(React.Component));
export default withOrganization(GroupUserFeedback);
//# sourceMappingURL=groupUserFeedback.jsx.map