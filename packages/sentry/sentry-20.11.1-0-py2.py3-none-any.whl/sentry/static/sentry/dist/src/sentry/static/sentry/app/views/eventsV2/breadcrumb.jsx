import { __assign, __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import Breadcrumbs from 'app/components/breadcrumbs';
import { getDiscoverLandingUrl } from 'app/utils/discover/urls';
var DiscoverBreadcrumb = /** @class */ (function (_super) {
    __extends(DiscoverBreadcrumb, _super);
    function DiscoverBreadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DiscoverBreadcrumb.prototype.getCrumbs = function () {
        var crumbs = [];
        var _a = this.props, eventView = _a.eventView, event = _a.event, organization = _a.organization, location = _a.location;
        var discoverTarget = organization.features.includes('discover-query')
            ? {
                pathname: getDiscoverLandingUrl(organization),
                query: __assign(__assign(__assign({}, location.query), eventView.generateBlankQueryStringObject()), eventView.getGlobalSelectionQuery()),
            }
            : null;
        crumbs.push({
            to: discoverTarget,
            label: t('Discover'),
        });
        if (eventView && eventView.isValid()) {
            crumbs.push({
                to: eventView.getResultsViewUrlTarget(organization.slug),
                label: eventView.name || '',
            });
        }
        if (event) {
            crumbs.push({
                label: t('Event Detail'),
            });
        }
        return crumbs;
    };
    DiscoverBreadcrumb.prototype.render = function () {
        return <Breadcrumbs crumbs={this.getCrumbs()}/>;
    };
    DiscoverBreadcrumb.defaultProps = {
        event: undefined,
    };
    return DiscoverBreadcrumb;
}(React.Component));
export default DiscoverBreadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map