import { __extends, __read } from "tslib";
import React from 'react';
import groupBy from 'lodash/groupBy';
import { tct } from 'app/locale';
import AddIntegration from 'app/views/organizationIntegrations/addIntegration';
import AlertLink from 'app/components/alertLink';
import AsyncComponent from 'app/components/asyncComponent';
var MigrationWarnings = /** @class */ (function (_super) {
    __extends(MigrationWarnings, _super);
    function MigrationWarnings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MigrationWarnings.prototype.getEndpoints = function () {
        var orgId = this.props.orgId;
        return [['unmigratableRepos', "/organizations/" + orgId + "/repos/?status=unmigratable"]];
    };
    Object.defineProperty(MigrationWarnings.prototype, "unmigratableReposByOrg", {
        get: function () {
            // Group by [GitHub|BitBucket|VSTS] Org name
            return groupBy(this.state.unmigratableRepos, function (repo) { return repo.name.split('/')[0]; });
        },
        enumerable: false,
        configurable: true
    });
    MigrationWarnings.prototype.render = function () {
        var _this = this;
        return Object.entries(this.unmigratableReposByOrg).map(function (_a) {
            var _b = __read(_a, 2), orgName = _b[0], repos = _b[1];
            // Repos use 'visualstudio', Integrations use 'vsts'. Normalize to 'vsts'.
            var key = repos[0].provider.id === 'visualstudio' ? 'vsts' : repos[0].provider.id;
            var provider = _this.props.providers.find(function (p) { return p.key === key; });
            // The Org might not have access to this Integration yet.
            if (!provider) {
                return '';
            }
            return (<AddIntegration key={provider.key} provider={provider} onInstall={_this.props.onInstall}>
            {function (onClick) { return (<AlertLink href="" onClick={function () { return onClick(); }}>
                {tct("Your [orgName] repositories can't send commit data to Sentry. Add a [orgName] [providerName] instance here.", {
                orgName: orgName,
                providerName: provider.name,
            })}
              </AlertLink>); }}
          </AddIntegration>);
        });
    };
    return MigrationWarnings;
}(AsyncComponent));
export default MigrationWarnings;
//# sourceMappingURL=migrationWarnings.jsx.map