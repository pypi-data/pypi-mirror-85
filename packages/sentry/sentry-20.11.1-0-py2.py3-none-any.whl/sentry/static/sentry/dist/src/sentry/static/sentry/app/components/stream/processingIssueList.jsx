import { __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import { Client } from 'app/api';
import { fetchProcessingIssues } from 'app/actionCreators/processingIssues';
import ProcessingIssueHint from 'app/components/stream/processingIssueHint';
import SentryTypes from 'app/sentryTypes';
var defaultProps = {
    showProject: false,
};
var ProcessingIssueList = /** @class */ (function (_super) {
    __extends(ProcessingIssueList, _super);
    function ProcessingIssueList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            issues: [],
        };
        _this.api = new Client();
        return _this;
    }
    ProcessingIssueList.prototype.componentDidMount = function () {
        this.fetchIssues();
    };
    ProcessingIssueList.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.projectIds, this.props.projectIds)) {
            this.fetchIssues();
        }
    };
    ProcessingIssueList.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ProcessingIssueList.prototype.fetchIssues = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projectIds = _a.projectIds;
        var promise = fetchProcessingIssues(this.api, organization.slug, projectIds);
        promise.then(function (data) {
            var hasIssues = data === null || data === void 0 ? void 0 : data.some(function (p) { return p.hasIssues || p.resolveableIssues > 0 || p.issuesProcessing > 0; });
            if (data && hasIssues) {
                _this.setState({ issues: data });
            }
        }, function () {
            // this is okay. it's just a ui hint
        });
    };
    ProcessingIssueList.prototype.render = function () {
        var issues = this.state.issues;
        var _a = this.props, organization = _a.organization, showProject = _a.showProject;
        return (<React.Fragment>
        {issues.map(function (p, idx) { return (<ProcessingIssueHint key={idx} issue={p} projectId={p.project} orgId={organization.slug} showProject={showProject}/>); })}
      </React.Fragment>);
    };
    ProcessingIssueList.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        projectIds: PropTypes.array,
        showProject: PropTypes.bool,
    };
    ProcessingIssueList.defaultProps = defaultProps;
    return ProcessingIssueList;
}(React.Component));
export default ProcessingIssueList;
//# sourceMappingURL=processingIssueList.jsx.map