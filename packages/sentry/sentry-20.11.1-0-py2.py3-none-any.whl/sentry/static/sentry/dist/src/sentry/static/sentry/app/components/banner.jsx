import { __extends, __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import React from 'react';
import styled from '@emotion/styled';
import { IconClose } from 'app/icons/iconClose';
import { t } from 'app/locale';
import space from 'app/styles/space';
var Banner = /** @class */ (function (_super) {
    __extends(Banner, _super);
    function Banner() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Banner.prototype.render = function () {
        var _a = this.props, title = _a.title, subtitle = _a.subtitle, isDismissable = _a.isDismissable, onCloseClick = _a.onCloseClick, children = _a.children, backgroundImg = _a.backgroundImg, backgroundComponent = _a.backgroundComponent, className = _a.className;
        return (<BannerWrapper backgroundComponent={backgroundComponent} backgroundImg={backgroundImg} className={className}>
        {backgroundComponent}
        {isDismissable ? (<StyledIconClose aria-label={t('Close')} onClick={onCloseClick}/>) : null}
        <BannerContent>
          <BannerTitle>{title}</BannerTitle>
          <BannerSubtitle>{subtitle}</BannerSubtitle>
          <BannerActions>{children}</BannerActions>
        </BannerContent>
      </BannerWrapper>);
    };
    Banner.defaultProps = {
        isDismissable: true,
    };
    return Banner;
}(React.Component));
var BannerWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n\n  ", "\n  position: relative;\n  margin-bottom: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  color: ", ";\n"], ["\n  ",
    "\n\n  ",
    "\n  position: relative;\n  margin-bottom: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  color: ", ";\n"])), function (p) {
    return p.backgroundImg
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n          background: url(", ");\n          background-repeat: no-repeat;\n          background-size: cover;\n          background-position: center center;\n        "], ["\n          background: url(", ");\n          background-repeat: no-repeat;\n          background-size: cover;\n          background-position: center center;\n        "])), p.backgroundImg) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n          background: ", ";\n        "], ["\n          background: ", ";\n        "])), p.theme.gray500);
}, function (p) {
    return p.backgroundComponent && css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n      display: flex;\n      flex-direction: column;\n      overflow: hidden;\n    "], ["\n      display: flex;\n      flex-direction: column;\n      overflow: hidden;\n    "])));
}, space(3), function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.white; });
var BannerContent = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  width: 100%;\n  height: 100%;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  text-align: center;\n  padding: ", ";\n\n  @media (max-width: ", ") {\n    padding: ", ";\n  }\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  width: 100%;\n  height: 100%;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  text-align: center;\n  padding: ", ";\n\n  @media (max-width: ", ") {\n    padding: ", ";\n  }\n"])), space(4), function (p) { return p.theme.breakpoints[0]; }, space(0));
var BannerTitle = styled('h1')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    font-size: 24px;\n  }\n\n  @media (min-width: ", ") {\n    margin-top: ", ";\n    margin-bottom: ", ";\n    font-size: 42px;\n  }\n"], ["\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    font-size: 24px;\n  }\n\n  @media (min-width: ", ") {\n    margin-top: ", ";\n    margin-bottom: ", ";\n    font-size: 42px;\n  }\n"])), space(0.25), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, space(2), space(0.5));
var BannerSubtitle = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n\n  @media (max-width: ", ") {\n    font-size: ", ";\n  }\n  @media (min-width: ", ") {\n    font-size: ", ";\n    margin-bottom: ", ";\n    flex-direction: row;\n    min-width: 650px;\n  }\n"], ["\n  font-size: ", ";\n\n  @media (max-width: ", ") {\n    font-size: ", ";\n  }\n  @media (min-width: ", ") {\n    font-size: ", ";\n    margin-bottom: ", ";\n    flex-direction: row;\n    min-width: 650px;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var BannerActions = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    width: auto;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    width: auto;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledIconClose = styled(IconClose)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: absolute;\n  display: block;\n  top: ", ";\n  right: ", ";\n  color: ", ";\n  cursor: pointer;\n  z-index: 1;\n"], ["\n  position: absolute;\n  display: block;\n  top: ", ";\n  right: ", ";\n  color: ", ";\n  cursor: pointer;\n  z-index: 1;\n"])), space(2), space(2), function (p) { return p.theme.white; });
export default Banner;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=banner.jsx.map