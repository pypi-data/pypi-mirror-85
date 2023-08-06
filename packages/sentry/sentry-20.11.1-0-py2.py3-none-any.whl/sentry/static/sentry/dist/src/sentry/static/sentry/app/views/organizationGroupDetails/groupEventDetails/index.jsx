import { __extends, __rest } from "tslib";
import React from 'react';
import { fetchOrganizationEnvironments } from 'app/actionCreators/environments';
import { t } from 'app/locale';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import OrganizationEnvironmentsStore from 'app/stores/organizationEnvironmentsStore';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import GroupEventDetails from './groupEventDetails';
var GroupEventDetailsContainer = /** @class */ (function (_super) {
    __extends(GroupEventDetailsContainer, _super);
    function GroupEventDetailsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = OrganizationEnvironmentsStore.get();
        return _this;
    }
    GroupEventDetailsContainer.prototype.componentDidMount = function () {
        var _this = this;
        this.environmentUnsubscribe = OrganizationEnvironmentsStore.listen(function (data) { return _this.setState(data); }, undefined);
        var _a = OrganizationEnvironmentsStore.get(), environments = _a.environments, error = _a.error;
        if (!environments && !error) {
            fetchOrganizationEnvironments(this.props.api, this.props.organization.slug);
        }
    };
    GroupEventDetailsContainer.prototype.componentWillUnmount = function () {
        if (this.environmentUnsubscribe) {
            this.environmentUnsubscribe();
        }
    };
    GroupEventDetailsContainer.prototype.render = function () {
        if (this.state.error) {
            return (<LoadingError message={t("There was an error loading your organization's environments")}/>);
        }
        // null implies loading state
        if (!this.state.environments) {
            return <LoadingIndicator />;
        }
        var _a = this.props, selection = _a.selection, otherProps = __rest(_a, ["selection"]);
        var environments = this.state.environments.filter(function (env) {
            return selection.environments.includes(env.name);
        });
        return <GroupEventDetails {...otherProps} environments={environments}/>;
    };
    return GroupEventDetailsContainer;
}(React.Component));
export { GroupEventDetailsContainer };
export default withApi(withOrganization(withGlobalSelection(GroupEventDetailsContainer)));
//# sourceMappingURL=index.jsx.map