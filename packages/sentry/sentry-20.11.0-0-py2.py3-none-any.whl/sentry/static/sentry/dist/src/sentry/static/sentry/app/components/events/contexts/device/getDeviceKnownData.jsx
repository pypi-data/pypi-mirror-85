import { __assign, __values } from "tslib";
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getDeviceKnownDataDetails from './getDeviceKnownDataDetails';
function getOperatingSystemKnownData(data, deviceKnownDataValues) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = deviceKnownDataValues.filter(function (deviceKnownDataValue) {
        return defined(data[deviceKnownDataValue]);
    });
    try {
        for (var dataKeys_1 = __values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getDeviceKnownDataDetails(data, key);
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
export default getOperatingSystemKnownData;
//# sourceMappingURL=getDeviceKnownData.jsx.map