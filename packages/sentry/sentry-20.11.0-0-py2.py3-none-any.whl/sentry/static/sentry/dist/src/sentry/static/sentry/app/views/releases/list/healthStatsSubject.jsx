import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
var HealthStatsSubject = function (_a) {
    var location = _a.location, activeSubject = _a.activeSubject;
    var pathname = location.pathname, query = location.query;
    var subjects = [
        {
            key: 'sessions',
            label: t('Sessions'),
        },
        {
            key: 'users',
            label: t('Users'),
        },
    ];
    return (<Wrapper>
      {subjects.map(function (subject) { return (<Title key={subject.key} to={{
        pathname: pathname,
        query: __assign(__assign({}, query), { healthStat: subject.key }),
    }} selected={activeSubject === subject.key}>
          {subject.label}
        </Title>); })}
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  margin-right: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  margin-right: ", ";\n"])), space(0.75), space(0.25));
var Title = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); }, function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); });
export default HealthStatsSubject;
var templateObject_1, templateObject_2;
//# sourceMappingURL=healthStatsSubject.jsx.map