import { __makeTemplateObject } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import OptionSelector from 'app/components/charts/optionSelector';
import styled from 'app/styled';
import space from 'app/styles/space';
export var YAxis;
(function (YAxis) {
    YAxis["SESSIONS"] = "sessions";
    YAxis["USERS"] = "users";
    YAxis["CRASH_FREE"] = "crashFree";
    YAxis["SESSION_DURATION"] = "sessionDuration";
    YAxis["EVENTS"] = "events";
})(YAxis || (YAxis = {}));
var ReleaseChartControls = function (_a) {
    var summary = _a.summary, yAxis = _a.yAxis, onYAxisChange = _a.onYAxisChange, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover;
    var noHealthDataTooltip = !hasHealthData
        ? t('This view is only available with release health data.')
        : undefined;
    var noDiscoverTooltip = !hasDiscover
        ? t('This view is only available with Discover feature.')
        : undefined;
    var yAxisOptions = [
        {
            value: YAxis.SESSIONS,
            label: t('Session Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.SESSION_DURATION,
            label: t('Session Duration'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.USERS,
            label: t('User Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.CRASH_FREE,
            label: t('Crash Free Rate'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.EVENTS,
            label: t('Event Count'),
            disabled: !hasDiscover,
            tooltip: noDiscoverTooltip,
        },
    ];
    var getSummaryHeading = function () {
        switch (yAxis) {
            case YAxis.USERS:
                return t('Total Active Users');
            case YAxis.CRASH_FREE:
                return t('Average Rate');
            case YAxis.SESSION_DURATION:
                return t('Median Duration');
            case YAxis.EVENTS:
                return t('Total Events');
            case YAxis.SESSIONS:
            default:
                return t('Total Sessions');
        }
    };
    return (<StyledChartControls>
      <InlineContainer>
        <SectionHeading key="total-label">{getSummaryHeading()}</SectionHeading>
        <SectionValue key="total-value">{summary}</SectionValue>
      </InlineContainer>

      <OptionSelector title={t('Y-Axis')} selected={yAxis} options={yAxisOptions} onChange={onYAxisChange} menuWidth="150px"/>
    </StyledChartControls>);
};
var StyledChartControls = styled(ChartControls)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    padding-bottom: ", ";\n    button {\n      font-size: ", ";\n    }\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    padding-bottom: ", ";\n    button {\n      font-size: ", ";\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1), space(1.5), function (p) { return p.theme.fontSizeSmall; });
export default ReleaseChartControls;
var templateObject_1;
//# sourceMappingURL=releaseChartControls.jsx.map