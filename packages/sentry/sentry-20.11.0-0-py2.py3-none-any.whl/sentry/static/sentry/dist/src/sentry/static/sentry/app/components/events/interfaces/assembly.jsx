import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { IconReturn } from 'app/icons/iconReturn';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
var Assembly = function (_a) {
    var name = _a.name, version = _a.version, culture = _a.culture, publicKeyToken = _a.publicKeyToken, filePath = _a.filePath;
    return (<AssemblyWrapper>
    <StyledIconReturn />
    <AssemblyInfo>
      <Caption>Assembly:</Caption>
      {name || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{t('Version')}:</Caption>
      {version || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{t('Culture')}:</Caption>
      {culture || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>PublicKeyToken:</Caption>
      {publicKeyToken || '-'}
    </AssemblyInfo>

    {filePath && (<FilePathInfo>
        <Caption>{t('Path')}:</Caption>
        <TextCopyInput rtl>{filePath}</TextCopyInput>
      </FilePathInfo>)}
  </AssemblyWrapper>);
};
// TODO(ts): we should be able to delete these after disabling react/prop-types rule in tsx functional components
Assembly.propTypes = {
    name: PropTypes.string.isRequired,
    version: PropTypes.string.isRequired,
    culture: PropTypes.string.isRequired,
    publicKeyToken: PropTypes.string.isRequired,
    filePath: PropTypes.string,
};
var AssemblyWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 80%;\n  display: flex;\n  flex-wrap: wrap;\n  color: ", ";\n  text-align: center;\n  position: relative;\n  padding: 0 ", " 0 50px;\n"], ["\n  font-size: 80%;\n  display: flex;\n  flex-wrap: wrap;\n  color: ", ";\n  text-align: center;\n  position: relative;\n  padding: 0 ", " 0 50px;\n"])), function (p) { return p.theme.textColor; }, space(3));
var StyledIconReturn = styled(IconReturn)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  transform: scaleX(-1);\n  position: absolute;\n  top: 4px;\n  left: 25px;\n"], ["\n  transform: scaleX(-1);\n  position: absolute;\n  top: 4px;\n  left: 25px;\n"])));
var AssemblyInfo = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: 15px;\n  margin-bottom: 5px;\n"], ["\n  margin-right: 15px;\n  margin-bottom: 5px;\n"])));
var Caption = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: 5px;\n  font-weight: bold;\n"], ["\n  margin-right: 5px;\n  font-weight: bold;\n"])));
var FilePathInfo = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: 5px;\n  input {\n    width: 250px;\n    padding-top: 0;\n    padding-bottom: 0;\n    line-height: 1.5;\n    @media (max-width: ", ") {\n      width: auto;\n    }\n  }\n  button > span {\n    padding: 2px 5px;\n  }\n  svg {\n    width: 0.9em;\n    height: 0.9em;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: 5px;\n  input {\n    width: 250px;\n    padding-top: 0;\n    padding-bottom: 0;\n    line-height: 1.5;\n    @media (max-width: ", ") {\n      width: auto;\n    }\n  }\n  button > span {\n    padding: 2px 5px;\n  }\n  svg {\n    width: 0.9em;\n    height: 0.9em;\n  }\n"])), theme.breakpoints[1]);
export { Assembly };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=assembly.jsx.map