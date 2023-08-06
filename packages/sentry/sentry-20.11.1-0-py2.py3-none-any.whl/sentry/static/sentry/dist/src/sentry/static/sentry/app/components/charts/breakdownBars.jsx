import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { formatPercentage } from 'app/utils/formatters';
import space from 'app/styles/space';
function BreakdownBars(_a) {
    var data = _a.data;
    var total = data.reduce(function (sum, point) { return point.value + sum; }, 0);
    return (<BreakdownGrid>
      {data.map(function (point, i) { return (<React.Fragment key={i + ":" + point.label}>
          <Percentage>{formatPercentage(point.value / total, 0)}</Percentage>
          <BarContainer>
            <Bar style={{ width: ((point.value / total) * 100).toFixed(2) + "%" }}/>
            <Label>{point.label}</Label>
          </BarContainer>
        </React.Fragment>); })}
    </BreakdownGrid>);
}
export default BreakdownBars;
var BreakdownGrid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content auto;\n  column-gap: ", ";\n  row-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: min-content auto;\n  column-gap: ", ";\n  row-gap: ", ";\n"])), space(1), space(1));
var Percentage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  text-align: right;\n"], ["\n  font-size: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var BarContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-left: ", ";\n  padding-right: ", ";\n  position: relative;\n"], ["\n  padding-left: ", ";\n  padding-right: ", ";\n  position: relative;\n"])), space(1), space(1));
var Label = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  color: ", ";\n  z-index: 2;\n  font-size: ", ";\n"], ["\n  position: relative;\n  color: ", ";\n  z-index: 2;\n  font-size: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeSmall; });
var Bar = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-radius: 2px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n  height: 100%;\n  width: 0%;\n"], ["\n  border-radius: 2px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n  height: 100%;\n  width: 0%;\n"])), function (p) { return p.theme.gray100; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=breakdownBars.jsx.map