import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import SentryTypes from 'app/sentryTypes';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import withOrganization from 'app/utils/withOrganization';
var DiscoverContainer = /** @class */ (function (_super) {
    __extends(DiscoverContainer, _super);
    function DiscoverContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DiscoverContainer.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    DiscoverContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<Feature features={['discover-basic']} organization={organization} hookName="feature-disabled:discover2-page" renderDisabled={this.renderNoAccess}>
        {children}
      </Feature>);
    };
    DiscoverContainer.propTypes = {
        organization: SentryTypes.Organization.isRequired,
    };
    return DiscoverContainer;
}(React.Component));
export default withOrganization(DiscoverContainer);
//# sourceMappingURL=index.jsx.map