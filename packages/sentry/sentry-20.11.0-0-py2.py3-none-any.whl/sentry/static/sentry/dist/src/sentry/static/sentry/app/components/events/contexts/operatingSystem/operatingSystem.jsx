import { __read, __spread } from "tslib";
import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getOperatingSystemKnownData from './getOperatingSystemKnownData';
import { OperatingSystemKnownDataType, OperatingSystemIgnoredDataType, } from './types';
import getUnknownData from '../getUnknownData';
var operatingSystemKnownDataValues = [
    OperatingSystemKnownDataType.NAME,
    OperatingSystemKnownDataType.VERSION,
    OperatingSystemKnownDataType.KERNEL_VERSION,
    OperatingSystemKnownDataType.ROOTED,
];
var operatingSystemIgnoredDataValues = [OperatingSystemIgnoredDataType.BUILD];
var OperatingSystem = function (_a) {
    var data = _a.data;
    return (<React.Fragment>
    <ContextBlock data={getOperatingSystemKnownData(data, operatingSystemKnownDataValues)}/>
    <ContextBlock data={getUnknownData(data, __spread(operatingSystemKnownDataValues, operatingSystemIgnoredDataValues))}/>
  </React.Fragment>);
};
export default OperatingSystem;
//# sourceMappingURL=operatingSystem.jsx.map