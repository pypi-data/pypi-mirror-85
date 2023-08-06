import { __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { getDuration, getExactDuration } from 'app/utils/formatters';
var Duration = function (_a) {
    var seconds = _a.seconds, fixedDigits = _a.fixedDigits, abbreviation = _a.abbreviation, exact = _a.exact, props = __rest(_a, ["seconds", "fixedDigits", "abbreviation", "exact"]);
    return (<span {...props}>
    {exact
        ? getExactDuration(seconds, abbreviation)
        : getDuration(seconds, fixedDigits, abbreviation)}
  </span>);
};
Duration.propTypes = {
    seconds: PropTypes.number.isRequired,
    fixedDigits: PropTypes.number,
    abbreviation: PropTypes.bool,
    exact: PropTypes.bool,
};
export default Duration;
//# sourceMappingURL=duration.jsx.map