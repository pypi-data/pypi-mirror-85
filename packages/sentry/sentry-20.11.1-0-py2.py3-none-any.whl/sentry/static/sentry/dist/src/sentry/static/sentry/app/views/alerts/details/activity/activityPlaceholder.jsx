import { __makeTemplateObject } from "tslib";
import { withTheme } from 'emotion-theming';
import React from 'react';
import styled from '@emotion/styled';
import ActivityItem from 'app/components/activity/item';
import space from 'app/styles/space';
export default withTheme(function ActivityPlaceholder(props) {
    return (<ActivityItem bubbleProps={{
        backgroundColor: props.theme.backgroundSecondary,
        borderColor: props.theme.backgroundSecondary,
    }}>
      {function () { return <Placeholder />; }}
    </ActivityItem>);
});
var Placeholder = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(4));
var templateObject_1;
//# sourceMappingURL=activityPlaceholder.jsx.map