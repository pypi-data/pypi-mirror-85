import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
var HealthStatsPeriod = function (_a) {
    var location = _a.location, activePeriod = _a.activePeriod;
    var pathname = location.pathname, query = location.query;
    var periods = [
        {
            key: '24h',
            label: t('24h'),
        },
        {
            key: '14d',
            label: t('14d'),
        },
    ];
    return (<Wrapper>
      {periods.map(function (period) { return (<Period key={period.key} to={{
        pathname: pathname,
        query: __assign(__assign({}, query), { healthStatsPeriod: period.key }),
    }} selected={activePeriod === period.key}>
          {period.label}
        </Period>); })}
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  flex: 1;\n  justify-content: flex-end;\n  text-align: right;\n  margin-left: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  flex: 1;\n  justify-content: flex-end;\n  text-align: right;\n  margin-left: ", ";\n"])), space(0.75), space(0.5));
var Period = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); }, function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); });
export default HealthStatsPeriod;
var templateObject_1, templateObject_2;
//# sourceMappingURL=healthStatsPeriod.jsx.map