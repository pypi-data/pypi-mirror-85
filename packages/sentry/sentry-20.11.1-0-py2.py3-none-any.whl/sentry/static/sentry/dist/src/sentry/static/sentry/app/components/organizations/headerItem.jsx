import { __extends, __makeTemplateObject, __rest } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import PropTypes from 'prop-types';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { IconClose, IconLock, IconChevron, IconInfo, IconSettings } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var HeaderItem = /** @class */ (function (_super) {
    __extends(HeaderItem, _super);
    function HeaderItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClear = function (e) {
            var _a, _b;
            e.stopPropagation();
            (_b = (_a = _this.props).onClear) === null || _b === void 0 ? void 0 : _b.call(_a);
        };
        return _this;
    }
    HeaderItem.prototype.render = function () {
        var _a = this.props, children = _a.children, isOpen = _a.isOpen, hasSelected = _a.hasSelected, allowClear = _a.allowClear, icon = _a.icon, locked = _a.locked, lockedMessage = _a.lockedMessage, settingsLink = _a.settingsLink, hint = _a.hint, loading = _a.loading, forwardRef = _a.forwardRef, props = __rest(_a, ["children", "isOpen", "hasSelected", "allowClear", "icon", "locked", "lockedMessage", "settingsLink", "hint", "loading", "forwardRef"]);
        var textColorProps = {
            locked: locked,
            isOpen: isOpen,
            hasSelected: hasSelected,
        };
        return (<StyledHeaderItem ref={forwardRef} loading={loading} {...omit(props, 'onClear')} {...textColorProps}>
        <IconContainer {...textColorProps}>{icon}</IconContainer>
        <Content>{children}</Content>
        {hint && (<Hint>
            <Tooltip title={hint} position="bottom">
              <IconInfo size="sm"/>
            </Tooltip>
          </Hint>)}
        {hasSelected && !locked && allowClear && (<StyledClose {...textColorProps} onClick={this.handleClear}/>)}
        {settingsLink && (<SettingsIconLink to={settingsLink}>
            <IconSettings />
          </SettingsIconLink>)}
        {!locked && !loading && (<StyledChevron isOpen={isOpen}>
            <IconChevron direction="down" color={isOpen ? 'gray500' : 'gray300'} size="sm"/>
          </StyledChevron>)}
        {locked && (<Tooltip title={lockedMessage || 'This selection is locked'} position="bottom">
            <StyledLock color="gray300"/>
          </Tooltip>)}
      </StyledHeaderItem>);
    };
    HeaderItem.propTypes = {
        icon: PropTypes.element,
        onClear: PropTypes.func,
        hasChanges: PropTypes.bool,
        hasSelected: PropTypes.bool,
        isOpen: PropTypes.bool,
        locked: PropTypes.bool,
        lockedMessage: PropTypes.element,
        settingsLink: PropTypes.string,
        hint: PropTypes.string,
    };
    HeaderItem.defaultProps = {
        allowClear: true,
    };
    return HeaderItem;
}(React.Component));
// Infer props here because of styled/theme
var getColor = function (p) {
    if (p.locked) {
        return p.theme.gray300;
    }
    return p.isOpen || p.hasSelected ? p.theme.textColor : p.theme.gray300;
};
var StyledHeaderItem = styled('div', {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'loading'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  padding: 0 ", ";\n  align-items: center;\n  cursor: ", ";\n  color: ", ";\n  transition: 0.1s color;\n  user-select: none;\n"], ["\n  display: flex;\n  padding: 0 ", ";\n  align-items: center;\n  cursor: ", ";\n  color: ", ";\n  transition: 0.1s color;\n  user-select: none;\n"])), space(4), function (p) { return (p.loading ? 'progress' : p.locked ? 'text' : 'pointer'); }, getColor);
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n  ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n  ", ";\n"])), space(1.5), overflowEllipsis);
var IconContainer = styled('span', { shouldForwardProp: isPropValid })(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin-right: ", ";\n  display: flex;\n  font-size: ", ";\n"], ["\n  color: ", ";\n  margin-right: ", ";\n  display: flex;\n  font-size: ", ";\n"])), getColor, space(1.5), function (p) { return p.theme.fontSizeMedium; });
var Hint = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  top: ", ";\n  margin-right: ", ";\n"], ["\n  position: relative;\n  top: ", ";\n  margin-right: ", ";\n"])), space(0.25), space(1));
var StyledClose = styled(IconClose, { shouldForwardProp: isPropValid })(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  height: ", ";\n  width: ", ";\n  stroke-width: 1.5;\n  padding: ", ";\n  box-sizing: content-box;\n  margin: -", " 0px -", " -", ";\n"], ["\n  color: ", ";\n  height: ", ";\n  width: ", ";\n  stroke-width: 1.5;\n  padding: ", ";\n  box-sizing: content-box;\n  margin: -", " 0px -", " -", ";\n"])), getColor, space(1.5), space(1.5), space(1), space(1), space(1), space(1));
var StyledChevron = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  transform: rotate(", ");\n  transition: 0.1s all;\n  width: ", ";\n  height: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  transform: rotate(", ");\n  transition: 0.1s all;\n  width: ", ";\n  height: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return (p.isOpen ? '180deg' : '0deg'); }, space(2), space(2));
var SettingsIconLink = styled(Link)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n  transition: 0.5s opacity ease-out;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n  transition: 0.5s opacity ease-out;\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, space(1), function (p) { return p.theme.textColor; });
var StyledLock = styled(IconLock)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-top: ", ";\n  stroke-width: 1.5;\n"], ["\n  margin-top: ", ";\n  stroke-width: 1.5;\n"])), space(0.75));
export default React.forwardRef(function (props, ref) { return (<HeaderItem forwardRef={ref} {...props}/>); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=headerItem.jsx.map