import { __extends } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import { metric } from 'app/utils/analytics';
import withOrganization, { isLightweightOrganization } from 'app/utils/withOrganization';
var IssueListContainer = /** @class */ (function (_super) {
    __extends(IssueListContainer, _super);
    function IssueListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IssueListContainer.prototype.componentDidMount = function () {
        // Setup here as render() may be expensive
        this.startMetricCollection();
    };
    /**
     * The user can (1) land on IssueList as the first page as they enter Sentry,
     * or (2) navigate into IssueList with the stores preloaded with data.
     *
     * Case (1) will be slower and we can easily identify it as it uses the
     * lightweight organization
     */
    IssueListContainer.prototype.startMetricCollection = function () {
        var isLightWeight = isLightweightOrganization(this.props.organization);
        var startType = isLightWeight ? 'cold-start' : 'warm-start';
        metric.mark({ name: 'page-issue-list-start', data: { start_type: startType } });
        metric.startTransaction({
            name: '/organizations/:orgId/issues/',
            op: isLightWeight ? 'pageload manual-first-paint' : 'navigation manual-first-paint',
        });
    };
    IssueListContainer.prototype.getTitle = function () {
        return "Issues - " + this.props.organization.slug + " - Sentry";
    };
    IssueListContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<DocumentTitle title={this.getTitle()}>
        <GlobalSelectionHeader>
          <LightWeightNoProjectMessage organization={organization}>
            {children}
          </LightWeightNoProjectMessage>
        </GlobalSelectionHeader>
      </DocumentTitle>);
    };
    return IssueListContainer;
}(React.Component));
export default withOrganization(IssueListContainer);
export { IssueListContainer };
//# sourceMappingURL=container.jsx.map