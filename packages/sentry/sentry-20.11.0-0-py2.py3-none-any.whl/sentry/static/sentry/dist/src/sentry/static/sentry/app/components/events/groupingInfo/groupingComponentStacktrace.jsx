import React from 'react';
import GroupingComponent from './groupingComponent';
import { groupingComponentFilter } from './utils';
import GroupingComponentFrames from './groupingComponentFrames';
var GroupingComponentStacktrace = function (_a) {
    var component = _a.component, showNonContributing = _a.showNonContributing;
    var getFrameGroups = function () {
        var frameGroups = [];
        component.values
            .filter(function (value) { return groupingComponentFilter(value, showNonContributing); })
            .forEach(function (value) {
            var key = value.values
                .filter(function (v) { return groupingComponentFilter(v, showNonContributing); })
                .map(function (v) { return v.id; })
                .sort(function (a, b) { return a.localeCompare(b); })
                .join('');
            var lastGroup = frameGroups[frameGroups.length - 1];
            if ((lastGroup === null || lastGroup === void 0 ? void 0 : lastGroup.key) === key) {
                lastGroup.data.push(value);
            }
            else {
                frameGroups.push({ key: key, data: [value] });
            }
        });
        return frameGroups;
    };
    return (<React.Fragment>
      {getFrameGroups().map(function (group, index) { return (<GroupingComponentFrames key={index} items={group.data.map(function (v, idx) { return (<GroupingComponent key={idx} component={v} showNonContributing={showNonContributing}/>); })}/>); })}
    </React.Fragment>);
};
export default GroupingComponentStacktrace;
//# sourceMappingURL=groupingComponentStacktrace.jsx.map