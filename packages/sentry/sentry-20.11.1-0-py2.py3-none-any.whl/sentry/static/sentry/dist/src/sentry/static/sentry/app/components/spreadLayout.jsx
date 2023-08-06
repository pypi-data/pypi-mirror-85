import { __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
// Flexbox container whose children will have `justify-content: space-between`
//
// Intended for children.length === 2
// "responsive" will change flex-direction to be column on small widths
var SpreadLayout = function (_a) {
    var _b = _a.responsive, responsive = _b === void 0 ? false : _b, _c = _a.center, center = _c === void 0 ? true : _c, children = _a.children, className = _a.className, props = __rest(_a, ["responsive", "center", "children", "className"]);
    var cx = classNames('spread-layout', className, {
        center: center,
        'allow-responsive': responsive,
    });
    return (<div {...props} className={cx}>
      {children}
    </div>);
};
SpreadLayout.propTypes = {
    responsive: PropTypes.bool,
    center: PropTypes.bool,
    children: PropTypes.node,
    style: PropTypes.object,
};
export default SpreadLayout;
//# sourceMappingURL=spreadLayout.jsx.map