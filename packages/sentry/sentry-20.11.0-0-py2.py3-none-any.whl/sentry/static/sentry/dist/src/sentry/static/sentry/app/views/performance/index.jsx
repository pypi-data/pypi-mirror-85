import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import SentryTypes from 'app/sentryTypes';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import withOrganization from 'app/utils/withOrganization';
var PerformanceContainer = /** @class */ (function (_super) {
    __extends(PerformanceContainer, _super);
    function PerformanceContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PerformanceContainer.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    PerformanceContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<Feature hookName="feature-disabled:performance-page" features={['performance-view']} organization={organization} renderDisabled={this.renderNoAccess}>
        {children}
      </Feature>);
    };
    PerformanceContainer.propTypes = {
        organization: SentryTypes.Organization.isRequired,
    };
    return PerformanceContainer;
}(React.Component));
export default withOrganization(PerformanceContainer);
//# sourceMappingURL=index.jsx.map