import { __extends } from "tslib";
import React from 'react';
import RouteError from 'app/views/routeError';
export default function errorHandler(Component) {
    var ErrorHandler = /** @class */ (function (_super) {
        __extends(ErrorHandler, _super);
        function ErrorHandler() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                // we are explicit if an error has been thrown since errors thrown are not guaranteed
                // to be truthy (e.g. throw null).
                hasError: false,
                error: undefined,
            };
            return _this;
        }
        ErrorHandler.getDerivedStateFromError = function (error) {
            // Update state so the next render will show the fallback UI.
            return {
                hasError: true,
                error: error,
            };
        };
        ErrorHandler.prototype.componentDidCatch = function (_error, info) {
            // eslint-disable-next-line no-console
            console.error('Component stack trace caught in <ErrorHandler />:', info.componentStack);
        };
        ErrorHandler.prototype.render = function () {
            if (this.state.hasError) {
                return <RouteError error={this.state.error}/>;
            }
            return <Component {...this.props}/>;
        };
        return ErrorHandler;
    }(React.Component));
    return ErrorHandler;
}
//# sourceMappingURL=errorHandler.jsx.map