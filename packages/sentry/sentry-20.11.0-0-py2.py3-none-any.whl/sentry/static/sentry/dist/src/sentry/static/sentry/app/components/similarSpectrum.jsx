import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
function SimilarSpectrum(_a) {
    var className = _a.className;
    return (<div className={className}>
      <span>{t('Similar')}</span>
      <SpectrumItem colorIndex={4}/>
      <SpectrumItem colorIndex={3}/>
      <SpectrumItem colorIndex={2}/>
      <SpectrumItem colorIndex={1}/>
      <SpectrumItem colorIndex={0}/>
      <span>{t('Not Similar')}</span>
    </div>);
}
var StyledSimilarSpectrum = styled(SimilarSpectrum)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  font-size: ", ";\n"], ["\n  display: flex;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var SpectrumItem = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-radius: 2px;\n  margin: 5px;\n  width: 14px;\n  ", ";\n"], ["\n  border-radius: 2px;\n  margin: 5px;\n  width: 14px;\n  ", ";\n"])), function (p) { return "background-color: " + p.theme.similarity.colors[p.colorIndex] + ";"; });
export default StyledSimilarSpectrum;
var templateObject_1, templateObject_2;
//# sourceMappingURL=similarSpectrum.jsx.map