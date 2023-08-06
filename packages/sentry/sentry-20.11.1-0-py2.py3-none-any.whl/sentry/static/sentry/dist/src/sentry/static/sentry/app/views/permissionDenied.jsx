import { __extends } from "tslib";
import { withRouter } from 'react-router';
import DocumentTitle from 'react-document-title';
import PropTypes from 'prop-types';
import React from 'react';
import * as Sentry from '@sentry/react';
import { t, tct } from 'app/locale';
import ExternalLink from 'app/components/links/externalLink';
import { PageContent } from 'app/styles/organization';
import LoadingError from 'app/components/loadingError';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
var ERROR_NAME = 'Permission Denied';
var PermissionDenied = /** @class */ (function (_super) {
    __extends(PermissionDenied, _super);
    function PermissionDenied() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PermissionDenied.prototype.componentDidMount = function () {
        var routes = this.props.routes;
        var _a = this.context, organization = _a.organization, project = _a.project;
        var route = getRouteStringFromRoutes(routes);
        Sentry.withScope(function (scope) {
            scope.setFingerprint([ERROR_NAME, route]);
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            Sentry.captureException(new Error("" + ERROR_NAME + (route ? " : " + route : '')));
        });
    };
    PermissionDenied.prototype.render = function () {
        return (<DocumentTitle title={t('Permission Denied')}>
        <PageContent>
          <LoadingError message={tct("Your role does not have the necessary permissions to access this\n               resource, please read more about [link:organizational roles]", {
            link: <ExternalLink href="https://docs.sentry.io/learn/membership/"/>,
        })}/>
        </PageContent>
      </DocumentTitle>);
    };
    PermissionDenied.contextTypes = {
        organization: PropTypes.object,
        project: PropTypes.object,
    };
    return PermissionDenied;
}(React.Component));
export default withRouter(PermissionDenied);
//# sourceMappingURL=permissionDenied.jsx.map