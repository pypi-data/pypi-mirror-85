import { __values } from "tslib";
import React from 'react';
import { getMeta } from 'app/components/events/meta/metaProxy';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueListV2';
var FrameVariables = function (_a) {
    var data = _a.data;
    // make sure that clicking on the variables does not actually do
    // anything on the containing element.
    var handlePreventToggling = function () { return function (event) {
        event.stopPropagation();
    }; };
    var getTransformedData = function () {
        var e_1, _a;
        var transformedData = [];
        var dataKeys = Object.keys(data).reverse();
        try {
            for (var dataKeys_1 = __values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
                var key = dataKeys_1_1.value;
                transformedData.push({
                    key: key,
                    subject: key,
                    value: data[key],
                    meta: getMeta(data, key),
                });
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (dataKeys_1_1 && !dataKeys_1_1.done && (_a = dataKeys_1.return)) _a.call(dataKeys_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return transformedData;
    };
    var transformedData = getTransformedData();
    return (<KeyValueList data={transformedData} onClick={handlePreventToggling} isContextData/>);
};
export default FrameVariables;
//# sourceMappingURL=frameVariables.jsx.map