import { __extends, __makeTemplateObject } from "tslib";
import { withRouter } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import * as Sentry from '@sentry/react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import { t, tct } from 'app/locale';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import { IconWarning } from 'app/icons';
import space from 'app/styles/space';
var RouteError = /** @class */ (function (_super) {
    __extends(RouteError, _super);
    function RouteError() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RouteError.prototype.UNSAFE_componentWillMount = function () {
        var error = this.props.error;
        var _a = this.props, disableLogSentry = _a.disableLogSentry, disableReport = _a.disableReport, routes = _a.routes;
        var _b = this.context, organization = _b.organization, project = _b.project;
        if (disableLogSentry) {
            return;
        }
        if (!error) {
            return;
        }
        var route = getRouteStringFromRoutes(routes);
        var enrichScopeContext = function (scope) {
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            return scope;
        };
        if (route) {
            /**
             * Unexpectedly, error.message would sometimes not have a setter property, causing another exception to be thrown,
             * and losing the original error in the process. Wrapping the mutation in a try-catch in an attempt to preserve
             * the original error for logging.
             * See https://github.com/getsentry/sentry/issues/16314 for more details.
             */
            try {
                error.message = error.message + ": " + route;
            }
            catch (e) {
                Sentry.withScope(function (scope) {
                    enrichScopeContext(scope);
                    Sentry.captureException(e);
                });
            }
        }
        // TODO(dcramer): show something in addition to embed (that contains it?)
        // throw this in a timeout so if it errors we dont fall over
        this._timeout = window.setTimeout(function () {
            Sentry.withScope(function (scope) {
                enrichScopeContext(scope);
                Sentry.captureException(error);
            });
            if (!disableReport) {
                Sentry.showReportDialog();
            }
        });
    };
    RouteError.prototype.componentWillUnmount = function () {
        var _a;
        if (this._timeout) {
            window.clearTimeout(this._timeout);
        }
        (_a = document.querySelector('.sentry-error-embed-wrapper')) === null || _a === void 0 ? void 0 : _a.remove();
    };
    RouteError.prototype.render = function () {
        // TODO(dcramer): show additional resource links
        return (<Alert icon={<IconWarning size="md"/>} type="error">
        <Heading>
          <span>{t('Oops! Something went wrong')}</span>
        </Heading>
        <p>
          {t("\n          It looks like you've hit an issue in our client application. Don't worry though!\n          We use Sentry to monitor Sentry and it's likely we're already looking into this!\n          ")}
        </p>
        <p>{t("If you're daring, you may want to try the following:")}</p>
        <ul>
          {window && window.adblockSuspected && (<li>
              {t("We detected something AdBlock-like. Try disabling it, as it's known to cause issues.")}
            </li>)}
          <li>
            {tct("Give it a few seconds and [link:reload the page].", {
            link: (<a onClick={function () {
                window.location.href = window.location.href;
            }}/>),
        })}
          </li>
          <li>
            {tct("If all else fails, [link:contact us] with more details.", {
            link: <a href="https://github.com/getsentry/sentry/issues/new/choose"/>,
        })}
          </li>
        </ul>
      </Alert>);
    };
    RouteError.propTypes = {
        disableLogSentry: PropTypes.bool,
        disableReport: PropTypes.bool,
        error: PropTypes.instanceOf(Error),
    };
    RouteError.contextTypes = {
        organization: PropTypes.object,
        project: PropTypes.object,
    };
    return RouteError;
}(React.Component));
var Heading = styled('h3')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  font-weight: normal;\n\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  font-weight: normal;\n\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, space(1.5));
export default withRouter(RouteError);
export { RouteError };
var templateObject_1;
//# sourceMappingURL=routeError.jsx.map