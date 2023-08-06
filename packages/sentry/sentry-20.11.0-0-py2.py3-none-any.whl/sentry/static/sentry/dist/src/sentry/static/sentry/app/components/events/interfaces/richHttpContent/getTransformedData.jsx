import { defined } from 'app/utils';
function getTransformedData(data) {
    if (Array.isArray(data)) {
        return data
            .filter(function (dataValue) { return defined(dataValue); })
            .map(function (dataValue) {
            if (Array.isArray(dataValue)) {
                return dataValue;
            }
            if (typeof data === 'object') {
                return Object.keys(dataValue).flatMap(function (key) { return [key, dataValue[key]]; });
            }
            return dataValue;
        });
    }
    if (typeof data === 'object') {
        return Object.keys(data).map(function (key) { return [key, data[key]]; });
    }
    return [];
}
export default getTransformedData;
//# sourceMappingURL=getTransformedData.jsx.map