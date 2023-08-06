import { __assign, __values } from "tslib";
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getGpuKnownDataDetails from './getGPUKnownDataDetails';
function getGPUKnownData(data, gpuKnownDataValues) {
    var e_1, _a;
    var knownData = [];
    var dataKeys = gpuKnownDataValues.filter(function (gpuKnownDataValue) {
        return defined(data[gpuKnownDataValue]);
    });
    try {
        for (var dataKeys_1 = __values(dataKeys), dataKeys_1_1 = dataKeys_1.next(); !dataKeys_1_1.done; dataKeys_1_1 = dataKeys_1.next()) {
            var key = dataKeys_1_1.value;
            var knownDataDetails = getGpuKnownDataDetails(data, key);
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
export default getGPUKnownData;
//# sourceMappingURL=getGPUKnownData.jsx.map