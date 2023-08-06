import React from 'react';
import isNil from 'lodash/isNil';
import { getMeta } from 'app/components/events/meta/metaProxy';
import ErrorBoundary from 'app/components/errorBoundary';
/**
 * Retrieves metadata from an object (object should be a proxy that
 * has been decorated using `app/components/events/meta/metaProxy/withMeta`
 */
var MetaData = function (_a) {
    var children = _a.children, object = _a.object, prop = _a.prop, required = _a.required;
    var value = object[prop];
    var meta = getMeta(object, prop);
    if (required && isNil(value) && !meta) {
        return null;
    }
    return <ErrorBoundary mini>{children(value, meta)}</ErrorBoundary>;
};
export default MetaData;
//# sourceMappingURL=metaData.jsx.map