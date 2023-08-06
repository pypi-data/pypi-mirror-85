import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import { defined } from 'app/utils';
/**
 * Displays a number count. If `max` is specified, then give representation
 * of count, i.e. "1000+"
 *
 * Render nothing by default if `count` is falsy.
 */
var QueryCount = function (_a) {
    var className = _a.className, count = _a.count, max = _a.max, _b = _a.hideIfEmpty, hideIfEmpty = _b === void 0 ? true : _b, _c = _a.inline, inline = _c === void 0 ? true : _c, _d = _a.hideParens, hideParens = _d === void 0 ? false : _d;
    var countOrMax = defined(count) && defined(max) && count >= max ? max + "+" : count;
    var cx = classNames('query-count', className, {
        inline: inline,
    });
    if (hideIfEmpty && !count) {
        return null;
    }
    return (<div className={cx}>
      {!hideParens && <span>(</span>}
      <span className="query-count-value">{countOrMax}</span>
      {!hideParens && <span>)</span>}
    </div>);
};
QueryCount.propTypes = {
    className: PropTypes.string,
    count: PropTypes.number,
    max: PropTypes.number,
    hideIfEmpty: PropTypes.bool,
    inline: PropTypes.bool,
    hideParens: PropTypes.bool,
};
export default QueryCount;
//# sourceMappingURL=queryCount.jsx.map