import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import omit from 'lodash/omit';
import { Link } from 'react-router';
import classNames from 'classnames';
var ListLink = /** @class */ (function (_super) {
    __extends(ListLink, _super);
    function ListLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.isActive = function () {
            var _a = _this.props, isActive = _a.isActive, to = _a.to, query = _a.query, index = _a.index;
            return (isActive || _this.context.router.isActive)({ pathname: to, query: query }, index);
        };
        _this.getClassName = function () {
            var _classNames = {};
            var _a = _this.props, className = _a.className, activeClassName = _a.activeClassName;
            if (className) {
                _classNames[className] = true;
            }
            if (_this.isActive()) {
                _classNames[activeClassName] = true;
            }
            return classNames(_classNames);
        };
        return _this;
    }
    ListLink.prototype.render = function () {
        var _a = this.props, index = _a.index, children = _a.children;
        var carriedProps = omit(this.props, 'activeClassName', 'isActive', 'index');
        return (<li className={this.getClassName()}>
        <Link {...carriedProps} onlyActiveOnIndex={index}>
          {children}
        </Link>
      </li>);
    };
    ListLink.displayName = 'ListLink';
    ListLink.contextTypes = {
        router: PropTypes.object.isRequired,
    };
    ListLink.defaultProps = {
        activeClassName: 'active',
        index: false,
    };
    return ListLink;
}(React.Component));
export default ListLink;
//# sourceMappingURL=listLink.jsx.map