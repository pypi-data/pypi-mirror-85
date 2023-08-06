import { __extends, __makeTemplateObject, __rest } from "tslib";
import { Link } from 'react-router';
import { css } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import Tooltip from 'app/components/tooltip';
var Button = /** @class */ (function (_super) {
    __extends(Button, _super);
    function Button() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Intercept onClick and propagate
        _this.handleClick = function (e) {
            var _a = _this.props, disabled = _a.disabled, busy = _a.busy, onClick = _a.onClick;
            // Don't allow clicks when disabled or busy
            if (disabled || busy) {
                e.preventDefault();
                e.stopPropagation();
                return;
            }
            if (typeof onClick !== 'function') {
                return;
            }
            onClick(e);
        };
        _this.getUrl = function (prop) {
            return _this.props.disabled ? undefined : prop;
        };
        return _this;
    }
    Button.prototype.render = function () {
        var _a = this.props, size = _a.size, to = _a.to, href = _a.href, title = _a.title, icon = _a.icon, children = _a.children, label = _a.label, borderless = _a.borderless, align = _a.align, priority = _a.priority, disabled = _a.disabled, tooltipProps = _a.tooltipProps, 
        // destructure from `buttonProps`
        // not necessary, but just in case someone re-orders props
        _onClick = _a.onClick, buttonProps = __rest(_a, ["size", "to", "href", "title", "icon", "children", "label", "borderless", "align", "priority", "disabled", "tooltipProps", "onClick"]);
        // For `aria-label`
        var screenReaderLabel = label || (typeof children === 'string' ? children : undefined);
        // Buttons come in 4 flavors: <Link>, <ExternalLink>, <a>, and <button>.
        // Let's use props to determine which to serve up, so we don't have to think about it.
        // *Note* you must still handle tabindex manually.
        var button = (<StyledButton aria-label={screenReaderLabel} aria-disabled={disabled} disabled={disabled} to={this.getUrl(to)} href={this.getUrl(href)} size={size} priority={priority} borderless={borderless} {...buttonProps} onClick={this.handleClick} role="button">
        <ButtonLabel align={align} size={size} priority={priority} borderless={borderless}>
          {icon && (<Icon size={size} hasChildren={!!children}>
              {icon}
            </Icon>)}
          {children}
        </ButtonLabel>
      </StyledButton>);
        // Doing this instead of using `Tooltip`'s `disabled` prop so that we can minimize snapshot nesting
        if (title) {
            return (<Tooltip {...tooltipProps} title={title}>
          {button}
        </Tooltip>);
        }
        return button;
    };
    Button.propTypes = {
        priority: PropTypes.oneOf(['default', 'primary', 'danger', 'link', 'success']),
        size: PropTypes.oneOf(['zero', 'xsmall', 'small']),
        disabled: PropTypes.bool,
        busy: PropTypes.bool,
        /**
         * Use this prop if button is a react-router link
         */
        to: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
        /**
         * Use this prop if button should use a normal (non-react-router) link
         */
        href: PropTypes.string,
        /**
         * A react node to use as the icons. Generally pulled from app/icons
         */
        icon: PropTypes.node,
        /**
         * Tooltip text
         */
        title: PropTypes.string,
        /**
         * Is an external link? (Will open in new tab)
         */
        external: PropTypes.bool,
        /**
         * Button with a border
         */
        borderless: PropTypes.bool,
        /**
         * Text aligment, takes justify-content properties.
         */
        align: PropTypes.oneOf(['center', 'left', 'right']),
        /**
         * Label for screen-readers (`aria-label`).
         * `children` will be used by default (only if it is a string), but this property takes priority.
         */
        label: PropTypes.string,
        /**
         * Passed down to built-in tooltip component
         */
        tooltipProps: PropTypes.object,
        onClick: PropTypes.func,
        forwardRef: PropTypes.any,
    };
    Button.defaultProps = {
        disabled: false,
        align: 'center',
    };
    return Button;
}(React.Component));
var ButtonForwardRef = React.forwardRef(function (props, ref) { return (<Button forwardRef={ref} {...props}/>); });
// Some components use Button's propTypes
ButtonForwardRef.propTypes = Button.propTypes;
ButtonForwardRef.displayName = 'forwardRef<Button>';
export default ButtonForwardRef;
var getFontSize = function (_a) {
    var size = _a.size, theme = _a.theme;
    switch (size) {
        case 'xsmall':
        case 'small':
            return theme.fontSizeSmall;
        default:
            return theme.fontSizeMedium;
    }
};
var getFontWeight = function (_a) {
    var priority = _a.priority, borderless = _a.borderless;
    return "font-weight: " + (priority === 'link' || borderless ? 400 : 600) + ";";
};
var getBoxShadow = function (active) { return function (_a) {
    var priority = _a.priority, borderless = _a.borderless, disabled = _a.disabled;
    if (disabled || borderless || priority === 'link') {
        return 'box-shadow: none';
    }
    return "box-shadow: " + (active ? 'inset' : '') + " 0 2px rgba(0, 0, 0, 0.05)";
}; };
var getColors = function (_a) {
    var priority = _a.priority, disabled = _a.disabled, borderless = _a.borderless, theme = _a.theme;
    var themeName = disabled ? 'disabled' : priority || 'default';
    var _b = theme.button[themeName], color = _b.color, colorActive = _b.colorActive, background = _b.background, backgroundActive = _b.backgroundActive, border = _b.border, borderActive = _b.borderActive, focusShadow = _b.focusShadow;
    return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    color: ", ";\n    background-color: ", ";\n    border: 1px solid ", ";\n\n    &:hover {\n      color: ", ";\n    }\n\n    &:hover,\n    &:focus,\n    &:active {\n      color: ", ";\n      background: ", ";\n      border-color: ", ";\n    }\n\n    &.focus-visible {\n      ", "\n    }\n  "], ["\n    color: ", ";\n    background-color: ", ";\n    border: 1px solid ", ";\n\n    &:hover {\n      color: ", ";\n    }\n\n    &:hover,\n    &:focus,\n    &:active {\n      color: ", ";\n      background: ", ";\n      border-color: ",
        ";\n    }\n\n    &.focus-visible {\n      ", "\n    }\n  "])), color, background, !borderless && !!border ? border : 'transparent', color, colorActive || color, backgroundActive, !borderless && (borderActive || border)
        ? borderActive || border
        : 'transparent', focusShadow && "box-shadow: " + focusShadow + " 0 0 0 3px;");
};
var StyledButton = styled(function (_a) {
    var forwardRef = _a.forwardRef, external = _a.external, props = __rest(_a, ["forwardRef", "external"]);
    // Get component to use based on existence of `to` or `href` properties
    // Can be react-router `Link`, `a`, or `button`
    if (props.to) {
        return <Link ref={forwardRef} {...props}/>;
    }
    if (!props.href) {
        return <button ref={forwardRef} {...props}/>;
    }
    if (external && props.href) {
        return <ExternalLink ref={forwardRef} {...props}/>;
    }
    return <a ref={forwardRef} {...props}/>;
}, {
    shouldForwardProp: function (prop) {
        return prop === 'forwardRef' ||
            prop === 'external' ||
            (isPropValid(prop) && prop !== 'disabled');
    },
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n  line-height: 1;\n  border-radius: ", ";\n  padding: 0;\n  text-transform: none;\n  ", ";\n  font-size: ", ";\n  ", ";\n  ", ";\n  cursor: ", ";\n  opacity: ", ";\n\n  &:active {\n    ", ";\n  }\n  &:focus {\n    outline: none;\n  }\n\n  ", ";\n"], ["\n  display: inline-block;\n  line-height: 1;\n  border-radius: ", ";\n  padding: 0;\n  text-transform: none;\n  ", ";\n  font-size: ", ";\n  ", ";\n  ", ";\n  cursor: ", ";\n  opacity: ", ";\n\n  &:active {\n    ", ";\n  }\n  &:focus {\n    outline: none;\n  }\n\n  ", ";\n"])), function (p) { return p.theme.button.borderRadius; }, getFontWeight, getFontSize, getColors, getBoxShadow(false), function (p) { return (p.disabled ? 'not-allowed' : 'pointer'); }, function (p) { return (p.busy || p.disabled) && '0.65'; }, getBoxShadow(true), function (p) { return (p.borderless || p.priority === 'link') && 'border-color: transparent'; });
/**
 * Get label padding determined by size
 */
var getLabelPadding = function (_a) {
    var size = _a.size, priority = _a.priority;
    if (priority === 'link') {
        return '0';
    }
    switch (size) {
        case 'zero':
            return '0';
        case 'xsmall':
            return '5px 8px';
        case 'small':
            return '9px 12px';
        default:
            return '12px 16px';
    }
};
var buttonLabelPropKeys = ['size', 'priority', 'borderless', 'align'];
var ButtonLabel = styled('span', {
    shouldForwardProp: function (prop) { return isPropValid(prop) && !buttonLabelPropKeys.includes(prop); },
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  justify-content: ", ";\n  padding: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  justify-content: ", ";\n  padding: ", ";\n"])), function (p) { return p.align; }, getLabelPadding);
var getIconMargin = function (_a) {
    var size = _a.size, hasChildren = _a.hasChildren;
    // If button is only an icon, then it shouldn't have margin
    if (!hasChildren) {
        return '0';
    }
    return size && size.endsWith('small') ? '6px' : '8px';
};
var Icon = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n  height: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n  height: ", ";\n"])), getIconMargin, getFontSize);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=button.jsx.map