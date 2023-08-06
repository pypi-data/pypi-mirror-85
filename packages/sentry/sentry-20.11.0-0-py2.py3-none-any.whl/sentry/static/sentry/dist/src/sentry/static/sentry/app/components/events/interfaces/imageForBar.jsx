import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import FunctionName from 'app/components/events/interfaces/frame/functionName';
import space from 'app/styles/space';
import { t } from 'app/locale';
var ImageForBar = function (_a) {
    var frame = _a.frame, onShowAllImages = _a.onShowAllImages;
    var handleShowAllImages = function () {
        onShowAllImages('');
    };
    return (<Wrapper>
      <MatchedFunctionWrapper>
        <MatchedFunctionCaption>{t('Image for: ')}</MatchedFunctionCaption>
        <FunctionName frame={frame}/>
      </MatchedFunctionWrapper>
      <ResetAddressFilterCaption onClick={handleShowAllImages}>
        {t('Show all images')}
      </ResetAddressFilterCaption>
    </Wrapper>);
};
ImageForBar.propTypes = {
    frame: PropTypes.object.isRequired,
    onShowAllImages: PropTypes.func.isRequired,
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: baseline;\n  justify-content: space-between;\n  padding: ", " ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  font-weight: 700;\n  code {\n    color: ", ";\n    font-size: ", ";\n    background: ", ";\n  }\n  a {\n    color: ", ";\n    &:hover {\n      text-decoration: underline;\n    }\n  }\n"], ["\n  display: flex;\n  align-items: baseline;\n  justify-content: space-between;\n  padding: ", " ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  font-weight: 700;\n  code {\n    color: ", ";\n    font-size: ", ";\n    background: ", ";\n  }\n  a {\n    color: ", ";\n    &:hover {\n      text-decoration: underline;\n    }\n  }\n"])), space(0.5), space(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.blue300; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.blue300; });
var MatchedFunctionWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: baseline;\n"], ["\n  display: flex;\n  align-items: baseline;\n"])));
var MatchedFunctionCaption = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  flex-shrink: 0;\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  flex-shrink: 0;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var ResetAddressFilterCaption = styled('a')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n  padding-left: ", ";\n  font-size: ", ";\n  font-weight: 400;\n  color: ", " !important;\n  &:hover {\n    color: ", " !important;\n  }\n"], ["\n  display: flex;\n  flex-shrink: 0;\n  padding-left: ", ";\n  font-size: ", ";\n  font-weight: 400;\n  color: ", " !important;\n  &:hover {\n    color: ", " !important;\n  }\n"])), space(0.5), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray300; });
export default ImageForBar;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=imageForBar.jsx.map