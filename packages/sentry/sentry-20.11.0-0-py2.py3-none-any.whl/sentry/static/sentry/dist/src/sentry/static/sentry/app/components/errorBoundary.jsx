import { __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import Alert from 'app/components/alert';
import DetailedError from 'app/components/errors/detailedError';
import { IconFlag } from 'app/icons';
import getDynamicText from 'app/utils/getDynamicText';
var exclamation = ['Raspberries', 'Snap', 'Frig', 'Welp', 'Uhhhh', 'Hmmm'];
function getExclamation() {
    return exclamation[Math.floor(Math.random() * exclamation.length)];
}
var ErrorBoundary = /** @class */ (function (_super) {
    __extends(ErrorBoundary, _super);
    function ErrorBoundary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: null,
        };
        _this._isMounted = false;
        return _this;
    }
    ErrorBoundary.prototype.componentDidMount = function () {
        var _this = this;
        this._isMounted = true;
        // Listen for route changes so we can clear error
        this.unlistenBrowserHistory = browserHistory.listen(function () {
            // Prevent race between component unmount and browserHistory change
            // Setting state on a component that is being unmounted throws an error
            if (_this._isMounted) {
                _this.setState({ error: null });
            }
        });
    };
    ErrorBoundary.prototype.componentDidCatch = function (error, errorInfo) {
        var errorTag = this.props.errorTag;
        this.setState({ error: error });
        Sentry.withScope(function (scope) {
            if (errorTag) {
                Object.keys(errorTag).forEach(function (tag) { return scope.setTag(tag, errorTag[tag]); });
            }
            scope.setExtra('errorInfo', errorInfo);
            Sentry.captureException(error);
        });
    };
    ErrorBoundary.prototype.componentWillUnmount = function () {
        this._isMounted = false;
        if (this.unlistenBrowserHistory) {
            this.unlistenBrowserHistory();
        }
    };
    ErrorBoundary.prototype.render = function () {
        var error = this.state.error;
        if (!error) {
            // when there's not an error, render children untouched
            return this.props.children;
        }
        var _a = this.props, customComponent = _a.customComponent, mini = _a.mini, message = _a.message, className = _a.className;
        if (customComponent) {
            return customComponent;
        }
        if (mini) {
            return (<Alert type="error" icon={<IconFlag size="md"/>} className={className}>
          {message || t('There was a problem rendering this component')}
        </Alert>);
        }
        return (<Wrapper>
        <DetailedError heading={getDynamicText({
            value: getExclamation(),
            fixed: exclamation[0],
        })} message={t("Something went horribly wrong rendering this page.\nWe use a decent error reporting service so this will probably be fixed soon. Unless our error reporting service is also broken. That would be awkward.\nAnyway, we apologize for the inconvenience.")}/>
        <StackTrace>{error.toString()}</StackTrace>
      </Wrapper>);
    };
    ErrorBoundary.propTypes = {
        mini: PropTypes.bool,
        message: PropTypes.node,
        customComponent: PropTypes.node,
    };
    ErrorBoundary.defaultProps = {
        mini: false,
    };
    return ErrorBoundary;
}(React.Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", "px;\n  max-width: 1000px;\n  margin: auto;\n"], ["\n  color: ", ";\n  padding: ", "px;\n  max-width: 1000px;\n  margin: auto;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.grid * 3; });
var StackTrace = styled('pre')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  white-space: pre-wrap;\n  margin: 32px;\n  margin-left: 85px;\n  margin-right: 18px;\n"], ["\n  white-space: pre-wrap;\n  margin: 32px;\n  margin-left: 85px;\n  margin-right: 18px;\n"])));
export default ErrorBoundary;
var templateObject_1, templateObject_2;
//# sourceMappingURL=errorBoundary.jsx.map