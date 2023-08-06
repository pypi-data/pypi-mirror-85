import { __extends, __rest } from "tslib";
import React from 'react';
import { analytics, metric } from 'app/utils/analytics';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization, { isLightweightOrganization } from 'app/utils/withOrganization';
import GroupDetails from './groupDetails';
var OrganizationGroupDetails = /** @class */ (function (_super) {
    __extends(OrganizationGroupDetails, _super);
    function OrganizationGroupDetails(props) {
        var _this = _super.call(this, props) || this;
        // Setup in the constructor as render() may be expensive
        _this.startMetricCollection();
        return _this;
    }
    OrganizationGroupDetails.prototype.componentDidMount = function () {
        analytics('issue_page.viewed', {
            group_id: parseInt(this.props.params.groupId, 10),
            org_id: parseInt(this.props.organization.id, 10),
        });
    };
    /**
     * See "page-issue-list-start" for explanation on hot/cold-starts
     */
    OrganizationGroupDetails.prototype.startMetricCollection = function () {
        var startType = isLightweightOrganization(this.props.organization)
            ? 'cold-start'
            : 'warm-start';
        metric.mark({ name: 'page-issue-details-start', data: { start_type: startType } });
    };
    OrganizationGroupDetails.prototype.render = function () {
        var _a = this.props, selection = _a.selection, props = __rest(_a, ["selection"]);
        return (<GroupDetails key={this.props.params.groupId + "-envs:" + selection.environments.join(',')} environments={selection.environments} {...props}/>);
    };
    return OrganizationGroupDetails;
}(React.Component));
export default withOrganization(withGlobalSelection(OrganizationGroupDetails));
//# sourceMappingURL=index.jsx.map