import { __read } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import SelectorItem from './selectorItem';
var RelativeSelector = function (_a) {
    var onClick = _a.onClick, selected = _a.selected, relativePeriods = _a.relativePeriods;
    return (<React.Fragment>
    {Object.entries(relativePeriods || DEFAULT_RELATIVE_PERIODS).map(function (_a) {
        var _b = __read(_a, 2), value = _b[0], label = _b[1];
        return (<SelectorItem key={value} onClick={onClick} value={value} label={label} selected={selected === value}/>);
    })}
  </React.Fragment>);
};
RelativeSelector.propTypes = {
    onClick: PropTypes.func,
    selected: PropTypes.string,
    relativePeriods: PropTypes.object,
};
export default RelativeSelector;
//# sourceMappingURL=relativeSelector.jsx.map