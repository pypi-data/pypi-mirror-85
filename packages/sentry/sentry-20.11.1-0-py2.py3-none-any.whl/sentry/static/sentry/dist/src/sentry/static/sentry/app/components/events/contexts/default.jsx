import { __read } from "tslib";
import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
function getKnownData(data) {
    return Object.entries(data)
        .filter(function (_a) {
        var _b = __read(_a, 1), k = _b[0];
        return k !== 'type' && k !== 'title';
    })
        .map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        return ({
            key: key,
            subject: key,
            value: value,
        });
    });
}
var DefaultContextType = function (_a) {
    var data = _a.data;
    return <ContextBlock data={getKnownData(data)}/>;
};
export default DefaultContextType;
//# sourceMappingURL=default.jsx.map