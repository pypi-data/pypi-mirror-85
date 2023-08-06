import { __assign, __values } from "tslib";
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getRuntimeKnownDataDetails from './getRuntimeKnownDataDetails';
function getRuntimeKnownData(data, runTimerKnownDataValues) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = runTimerKnownDataValues.filter(function (runTimerKnownDataValue) {
        return defined(data[runTimerKnownDataValue]);
    });
    try {
        for (var dataKeys_1 = __values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getRuntimeKnownDataDetails(data, key);
            knownData.push(__assign(__assign({ key: key }, knownDataDetails), { meta: getMeta(data, key) }));
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
export default getRuntimeKnownData;
//# sourceMappingURL=getRuntimeKnownData.jsx.map