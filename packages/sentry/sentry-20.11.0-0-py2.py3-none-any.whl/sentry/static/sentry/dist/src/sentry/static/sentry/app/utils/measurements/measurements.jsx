import { __read } from "tslib";
import React from 'react';
import { WEB_VITAL_DETAILS } from 'app/views/performance/transactionVitals/constants';
var MEASUREMENTS = Object.fromEntries(Object.entries(WEB_VITAL_DETAILS).map(function (_a) {
    var _b = __read(_a, 2), key = _b[0], value = _b[1];
    var newValue = {
        name: value.name,
        key: key,
    };
    return [key, newValue];
}));
function Measurements(props) {
    return (<React.Fragment>
      {props.children({
        measurements: MEASUREMENTS,
    })}
    </React.Fragment>);
}
export default Measurements;
//# sourceMappingURL=measurements.jsx.map