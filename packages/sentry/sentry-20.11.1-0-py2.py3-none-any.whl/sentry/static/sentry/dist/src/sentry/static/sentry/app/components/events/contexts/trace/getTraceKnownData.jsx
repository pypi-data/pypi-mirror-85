import { __assign, __values } from "tslib";
import { defined } from 'app/utils';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { TraceKnownDataType } from './types';
import getUserKnownDataDetails from './getTraceKnownDataDetails';
function getTraceKnownData(data, traceKnownDataValues, event, organization) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = traceKnownDataValues.filter(function (traceKnownDataValue) {
        if (traceKnownDataValue === TraceKnownDataType.TRANSACTION_NAME) {
            return event === null || event === void 0 ? void 0 : event.tags.find(function (tag) {
                return tag.key === 'transaction';
            });
        }
        return data[traceKnownDataValue];
    });
    try {
        for (var dataKeys_1 = __values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getUserKnownDataDetails(data, key, event, organization);
            if ((knownDataDetails && !defined(knownDataDetails.value)) || !knownDataDetails) {
                continue;
            }
            knownData.push(__assign(__assign({ key: key }, knownDataDetails), { meta: getMeta(data, key), subjectDataTestId: "trace-context-" + key.toLowerCase() + "-value" }));
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (dataKeys_1_1 && !dataKeys_1_1.done && (_a = dataKeys_1.return)) _a.call(dataKeys_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return knownData;
}
export default getTraceKnownData;
//# sourceMappingURL=getTraceKnownData.jsx.map