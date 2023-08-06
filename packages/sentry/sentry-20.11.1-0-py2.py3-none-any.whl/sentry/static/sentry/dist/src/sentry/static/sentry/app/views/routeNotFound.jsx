import { __extends } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import * as Sentry from '@sentry/react';
import Footer from 'app/components/footer';
import Sidebar from 'app/components/sidebar';
import NotFound from 'app/components/errors/notFound';
var RouteNotFound = /** @class */ (function (_super) {
    __extends(RouteNotFound, _super);
    function RouteNotFound() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getTitle = function () { return 'Page Not Found'; };
        return _this;
    }
    RouteNotFound.prototype.componentDidMount = function () {
        Sentry.withScope(function (scope) {
            scope.setFingerprint(['RouteNotFound']);
            Sentry.captureException(new Error('Route not found'));
        });
    };
    RouteNotFound.prototype.render = function () {
        // TODO(dcramer): show additional resource links
        return (<DocumentTitle title={this.getTitle()}>
        <div className="app">
          <Sidebar location={this.props.location}/>
          <div className="container">
            <div className="content">
              <section className="body">
                <NotFound />
              </section>
            </div>
          </div>
          <Footer />
        </div>
      </DocumentTitle>);
    };
    return RouteNotFound;
}(React.Component));
export default RouteNotFound;
//# sourceMappingURL=routeNotFound.jsx.map