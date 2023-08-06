import { __assign, __values } from "tslib";
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getUserKnownDataDetails from './getUserKnownDataDetails';
function getUserKnownData(data, userKnownDataValues) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = userKnownDataValues.filter(function (userKnownDataValue) {
        return defined(data[userKnownDataValue]);
    });
    try {
        for (var dataKeys_1 = __values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getUserKnownDataDetails(data, key);
            if ((knownDataDetails && !defined(knownDataDetails.value)) || !knownDataDetails) {
                continue;
            }
            knownData.push(__assign(__assign({ key: key }, knownDataDetails), { meta: getMeta(data, key), subjectDataTestId: "user-context-" + key.toLowerCase() + "-value" }));
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
export default getUserKnownData;
//# sourceMappingURL=getUserKnownData.jsx.map