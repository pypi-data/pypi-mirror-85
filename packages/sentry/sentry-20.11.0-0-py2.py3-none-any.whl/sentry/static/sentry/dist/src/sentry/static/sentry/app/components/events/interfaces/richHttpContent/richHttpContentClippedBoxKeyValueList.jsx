import { __read } from "tslib";
import React from 'react';
import ErrorBoundary from 'app/components/errorBoundary';
import ClippedBox from 'app/components/clippedBox';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueListV2';
import getTransformedData from './getTransformedData';
var RichHttpContentClippedBoxKeyValueList = function (_a) {
    var data = _a.data, title = _a.title, _b = _a.defaultCollapsed, defaultCollapsed = _b === void 0 ? false : _b, _c = _a.isContextData, isContextData = _c === void 0 ? false : _c, meta = _a.meta;
    var getContent = function (transformedData) {
        // Sentry API abbreviates long query string values, sometimes resulting in
        // an un-parsable querystring ... stay safe kids
        try {
            return (<KeyValueList data={transformedData.map(function (_a) {
                var _b = __read(_a, 2), key = _b[0], value = _b[1];
                return ({
                    key: key,
                    subject: key,
                    value: value,
                    meta: meta,
                });
            })} isContextData={isContextData}/>);
        }
        catch (_a) {
            return <pre>{data}</pre>;
        }
    };
    var transformedData = getTransformedData(data);
    if (transformedData.length === 0) {
        return null;
    }
    return (<ClippedBox title={title} defaultClipped={defaultCollapsed}>
      <ErrorBoundary mini>{getContent(transformedData)}</ErrorBoundary>
    </ClippedBox>);
};
export default RichHttpContentClippedBoxKeyValueList;
//# sourceMappingURL=richHttpContentClippedBoxKeyValueList.jsx.map