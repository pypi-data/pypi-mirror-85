import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
var defaultprops = {
    maxVisibleItems: 4,
    fadeHeight: 46,
};
var WRAPPER_DEFAULT_HEIGHT = defaultprops.fadeHeight * defaultprops.maxVisibleItems;
// TODO(matej): refactor to reusable component
var clippedHealthRows = /** @class */ (function (_super) {
    __extends(clippedHealthRows, _super);
    function clippedHealthRows() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isCollapsed: true,
        };
        _this.reveal = function () {
            _this.setState({ isCollapsed: false });
        };
        _this.collapse = function () {
            _this.setState({ isCollapsed: true });
        };
        return _this;
    }
    clippedHealthRows.prototype.renderShowMoreButton = function () {
        var _a = this.props, children = _a.children, maxVisibleItems = _a.maxVisibleItems;
        var showMoreBtnProps = {
            onClick: this.reveal,
            priority: 'primary',
            size: 'xsmall',
            'data-test-id': 'show-more',
        };
        return (<ShowMoreWrapper key="show-more">
        <SmallerDevicesShowMoreButton {...showMoreBtnProps}>
          {tct('Show [numberOfFrames] More', {
            numberOfFrames: children.length - defaultprops.maxVisibleItems,
        })}
        </SmallerDevicesShowMoreButton>
        <LargerDevicesShowMoreButton {...showMoreBtnProps}>
          {tct('Show [numberOfFrames] More', {
            numberOfFrames: children.length - maxVisibleItems,
        })}
        </LargerDevicesShowMoreButton>
      </ShowMoreWrapper>);
    };
    clippedHealthRows.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, maxVisibleItems = _a.maxVisibleItems, fadeHeight = _a.fadeHeight, className = _a.className;
        var isCollapsed = this.state.isCollapsed;
        var displayCollapsedButton = !isCollapsed && children.length > maxVisibleItems;
        return (<Wrapper className={className} fadeHeight={fadeHeight} displayCollapsedButton={displayCollapsedButton} height={isCollapsed && children.length > maxVisibleItems
            ? WRAPPER_DEFAULT_HEIGHT
            : undefined}>
        {children.map(function (item, index) {
            if (!isCollapsed || index < maxVisibleItems) {
                return item;
            }
            if (index === maxVisibleItems) {
                return _this.renderShowMoreButton();
            }
            return null;
        })}

        {displayCollapsedButton && (<CollapseWrapper>
            <Button onClick={this.collapse} priority="primary" size="xsmall" data-test-id="collapse">
              {t('Collapse')}
            </Button>
          </CollapseWrapper>)}
      </Wrapper>);
    };
    clippedHealthRows.defaultProps = defaultprops;
    return clippedHealthRows;
}(React.Component));
var absoluteButtonStyle = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  position: absolute;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var ShowMoreWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  background-image: linear-gradient(\n    180deg,\n    hsla(0, 0%, 100%, 0.15) 0,\n    ", "\n  );\n  background-repeat: repeat-x;\n  border-bottom: ", " solid ", ";\n  border-top: ", " solid transparent;\n"], ["\n  ", ";\n  background-image: linear-gradient(\n    180deg,\n    hsla(0, 0%, 100%, 0.15) 0,\n    ", "\n  );\n  background-repeat: repeat-x;\n  border-bottom: ", " solid ", ";\n  border-top: ", " solid transparent;\n"])), absoluteButtonStyle, function (p) { return p.theme.white; }, space(1), function (p) { return p.theme.white; }, space(1));
var CollapseWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), absoluteButtonStyle);
var Wrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  ", " {\n    height: ", "px;\n  }\n  ", " {\n    height: ", "px;\n  }\n  ", "\n\n  ", "\n"], ["\n  position: relative;\n  ", " {\n    height: ", "px;\n  }\n  ", " {\n    height: ", "px;\n  }\n  ", "\n\n  ",
    "\n"])), ShowMoreWrapper, function (p) { return p.fadeHeight; }, CollapseWrapper, function (p) { return p.fadeHeight; }, function (p) { return p.displayCollapsedButton && "padding-bottom: " + p.fadeHeight + "px;"; }, function (p) {
    return p.height &&
        "\n      height: " + p.height + "px;\n      @media (min-width: " + p.theme.breakpoints[0] + ") {\n        height: auto;\n      }\n  ";
});
var SmallerDevicesShowMoreButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: block;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: block;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var LargerDevicesShowMoreButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default clippedHealthRows;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=clippedHealthRows.jsx.map