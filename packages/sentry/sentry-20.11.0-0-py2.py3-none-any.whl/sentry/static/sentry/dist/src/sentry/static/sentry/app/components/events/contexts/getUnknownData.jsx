import { __read } from "tslib";
import { getMeta } from 'app/components/events/meta/metaProxy';
function getUnknownData(allData, knownKeys) {
    return Object.entries(allData)
        .filter(function (_a) {
        var _b = __read(_a, 1), key = _b[0];
        return key !== 'type' && key !== 'title';
    })
        .filter(function (_a) {
        var _b = __read(_a, 1), key = _b[0];
        return !knownKeys.includes(key);
    })
        .map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        return ({
            key: key,
            value: value,
            subject: key,
            meta: getMeta(allData, key),
        });
    });
}
export default getUnknownData;
//# sourceMappingURL=getUnknownData.jsx.map