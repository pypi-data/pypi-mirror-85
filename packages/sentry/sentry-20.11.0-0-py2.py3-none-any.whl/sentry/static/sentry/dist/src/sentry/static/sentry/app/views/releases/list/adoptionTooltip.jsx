import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Count from 'app/components/count';
var AdoptionTooltip = function (_a) {
    var totalUsers = _a.totalUsers, totalUsers24h = _a.totalUsers24h, totalSessions = _a.totalSessions, totalSessions24h = _a.totalSessions24h;
    return (<Wrapper>
      <Row>
        <Title>{t('Last 24h')}:</Title>
        <Value>
          <Count value={totalUsers24h !== null && totalUsers24h !== void 0 ? totalUsers24h : 0}/>
        </Value>
      </Row>
      <Row>
        <Title>{t('Total Users')}:</Title>
        <Value>
          <Count value={totalUsers}/>
        </Value>
      </Row>
      <Divider />

      <Row>
        <Title>{t('Last 24h')}:</Title>
        <Value>
          <Count value={totalSessions24h !== null && totalSessions24h !== void 0 ? totalSessions24h : 0}/>
        </Value>
      </Row>
      <Row>
        <Title>{t('Total Sessions')}:</Title>
        <Value>
          <Count value={totalSessions}/>
        </Value>
      </Row>
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(0.75));
var Row = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  justify-content: space-between;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  justify-content: space-between;\n  padding-bottom: ", ";\n"])), space(4), space(0.25));
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var Value = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  text-align: right;\n"], ["\n  color: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.gray300; });
var Divider = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin: ", " -", " ", ";\n"], ["\n  border-top: 1px solid ", ";\n  margin: ", " -", " ", ";\n"])), function (p) { return p.theme.gray500; }, space(0.75), space(2), space(1));
export default AdoptionTooltip;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=adoptionTooltip.jsx.map