import React from 'react';
import Version from 'app/components/version';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import DeviceName from 'app/components/deviceName';
import Link from 'app/components/links/link';
import { defined } from 'app/utils';
var EventTagsPillValue = function (_a) {
    var _b;
    var _c = _a.tag, key = _c.key, value = _c.value, meta = _a.meta, isRelease = _a.isRelease, streamPath = _a.streamPath, locationSearch = _a.locationSearch;
    var getContent = function () {
        return isRelease ? (<Version version={String(value)} anchor={false} tooltipRawVersion truncate/>) : (<AnnotatedText value={defined(value) && <DeviceName value={String(value)}/>} meta={meta}/>);
    };
    var content = getContent();
    if (!((_b = meta === null || meta === void 0 ? void 0 : meta.err) === null || _b === void 0 ? void 0 : _b.length) && defined(key)) {
        return <Link to={{ pathname: streamPath, search: locationSearch }}>{content}</Link>;
    }
    return content;
};
export default EventTagsPillValue;
//# sourceMappingURL=eventTagsPillValue.jsx.map