import React from 'react';
import { defined } from 'app/utils';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getEventExtraDataKnownData from './getEventExtraDataKnownData';
var EventDataContent = function (_a) {
    var data = _a.data, raw = _a.raw;
    if (!defined(data)) {
        return null;
    }
    return <ContextBlock data={getEventExtraDataKnownData(data)} raw={raw}/>;
};
export default EventDataContent;
//# sourceMappingURL=eventDataContent.jsx.map