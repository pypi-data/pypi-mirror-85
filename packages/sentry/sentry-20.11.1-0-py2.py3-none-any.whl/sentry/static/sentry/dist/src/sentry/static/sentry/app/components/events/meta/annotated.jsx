import React from 'react';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import MetaData from 'app/components/events/meta/metaData';
import { isFunction } from 'app/utils';
/**
 * Returns the value of `object[prop]` and returns an annotated component if
 * there is meta data
 */
var Annotated = function (_a) {
    var children = _a.children, object = _a.object, objectKey = _a.objectKey, _b = _a.required, required = _b === void 0 ? false : _b;
    return (<MetaData object={object} prop={objectKey} required={required}>
      {function (value, meta) {
        var toBeReturned = <AnnotatedText value={value} meta={meta}/>;
        return isFunction(children) ? children(toBeReturned) : toBeReturned;
    }}
    </MetaData>);
};
export default Annotated;
//# sourceMappingURL=annotated.jsx.map