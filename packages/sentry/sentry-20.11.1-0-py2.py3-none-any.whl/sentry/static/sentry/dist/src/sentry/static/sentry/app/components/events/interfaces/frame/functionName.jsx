import React from 'react';
import { t } from 'app/locale';
import { getMeta } from 'app/components/events/meta/metaProxy';
import AnnotatedText from 'app/components/events/meta/annotatedText';
var FunctionName = function (_a) {
    var frame = _a.frame, showCompleteFunctionName = _a.showCompleteFunctionName, hasHiddenDetails = _a.hasHiddenDetails, className = _a.className;
    var getValueOutput = function () {
        if (hasHiddenDetails && showCompleteFunctionName && frame.rawFunction) {
            return {
                value: frame.rawFunction,
                meta: getMeta(frame, 'rawFunction'),
            };
        }
        if (frame.function) {
            return {
                value: frame.function,
                meta: getMeta(frame, 'function'),
            };
        }
        if (frame.rawFunction) {
            return {
                value: frame.rawFunction,
                meta: getMeta(frame, 'rawFunction'),
            };
        }
        return undefined;
    };
    var valueOutput = getValueOutput();
    return (<code className={className}>
      {!valueOutput ? (t('<unknown>')) : (<AnnotatedText value={valueOutput.value} meta={valueOutput.meta}/>)}
    </code>);
};
export default FunctionName;
//# sourceMappingURL=functionName.jsx.map