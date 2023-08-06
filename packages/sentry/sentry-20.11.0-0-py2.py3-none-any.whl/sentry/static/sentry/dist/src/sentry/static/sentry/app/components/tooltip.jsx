import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Manager, Reference, Popper } from 'react-popper';
import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import { domId } from 'app/utils/domId';
import { IS_ACCEPTANCE_TEST } from 'app/constants';
var IS_HOVERABLE_DELAY = 50; // used if isHoverable is true (for hiding AND showing)
var Tooltip = /** @class */ (function (_super) {
    __extends(Tooltip, _super);
    function Tooltip() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
            usesGlobalPortal: true,
        };
        _this.tooltipId = domId('tooltip-');
        _this.delayTimeout = null;
        _this.delayHideTimeout = null;
        _this.getPortal = memoize(function (usesGlobalPortal) {
            if (usesGlobalPortal) {
                var portal_1 = document.getElementById('tooltip-portal');
                if (!portal_1) {
                    portal_1 = document.createElement('div');
                    portal_1.setAttribute('id', 'tooltip-portal');
                    document.body.appendChild(portal_1);
                }
                return portal_1;
            }
            var portal = document.createElement('div');
            document.body.appendChild(portal);
            return portal;
        });
        _this.setOpen = function () {
            _this.setState({ isOpen: true });
        };
        _this.setClose = function () {
            _this.setState({ isOpen: false });
        };
        _this.handleOpen = function () {
            var _a = _this.props, delay = _a.delay, isHoverable = _a.isHoverable;
            if (_this.delayHideTimeout) {
                window.clearTimeout(_this.delayHideTimeout);
                _this.delayHideTimeout = null;
            }
            if (delay || isHoverable) {
                _this.delayTimeout = window.setTimeout(_this.setOpen, delay || IS_HOVERABLE_DELAY);
            }
            else {
                _this.setOpen();
            }
        };
        _this.handleClose = function () {
            var isHoverable = _this.props.isHoverable;
            if (_this.delayTimeout) {
                window.clearTimeout(_this.delayTimeout);
                _this.delayTimeout = null;
            }
            if (isHoverable) {
                _this.delayHideTimeout = window.setTimeout(_this.setClose, IS_HOVERABLE_DELAY);
            }
            else {
                _this.setClose();
            }
        };
        return _this;
    }
    Tooltip.prototype.componentDidMount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var TooltipStore;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!IS_ACCEPTANCE_TEST) return [3 /*break*/, 2];
                        return [4 /*yield*/, import(/* webpackChunkName: "TooltipStore" */ 'app/stores/tooltipStore')];
                    case 1:
                        TooltipStore = (_a.sent()).default;
                        TooltipStore.addTooltip(this);
                        _a.label = 2;
                    case 2: return [2 /*return*/];
                }
            });
        });
    };
    Tooltip.prototype.componentWillUnmount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var usesGlobalPortal, TooltipStore;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        usesGlobalPortal = this.state.usesGlobalPortal;
                        if (!IS_ACCEPTANCE_TEST) return [3 /*break*/, 2];
                        return [4 /*yield*/, import(/* webpackChunkName: "TooltipStore" */ 'app/stores/tooltipStore')];
                    case 1:
                        TooltipStore = (_a.sent()).default;
                        TooltipStore.removeTooltip(this);
                        _a.label = 2;
                    case 2:
                        if (!usesGlobalPortal) {
                            document.body.removeChild(this.getPortal(usesGlobalPortal));
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    Tooltip.prototype.renderTrigger = function (children, ref) {
        var propList = {
            'aria-describedby': this.tooltipId,
            onFocus: this.handleOpen,
            onBlur: this.handleClose,
            onMouseEnter: this.handleOpen,
            onMouseLeave: this.handleClose,
        };
        // Use the `type` property of the react instance to detect whether we
        // have a basic element (type=string) or a class/function component (type=function or object)
        // Because we can't rely on the child element implementing forwardRefs we wrap
        // it with a span tag so that popper has ref
        if (React.isValidElement(children) &&
            (this.props.skipWrapper || typeof children.type === 'string')) {
            // Basic DOM nodes can be cloned and have more props applied.
            return React.cloneElement(children, __assign(__assign({}, propList), { ref: ref }));
        }
        propList.containerDisplayMode = this.props.containerDisplayMode;
        return (<Container {...propList} className={this.props.className} ref={ref}>
        {children}
      </Container>);
    };
    Tooltip.prototype.render = function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, children = _a.children, title = _a.title, position = _a.position, popperStyle = _a.popperStyle, isHoverable = _a.isHoverable;
        var _b = this.state, isOpen = _b.isOpen, usesGlobalPortal = _b.usesGlobalPortal;
        if (disabled) {
            return children;
        }
        var tip = null;
        var modifiers = {
            hide: { enabled: false },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        if (isOpen) {
            tip = ReactDOM.createPortal(<Popper placement={position} modifiers={modifiers}>
          {function (_a) {
                var _b;
                var ref = _a.ref, style = _a.style, placement = _a.placement, arrowProps = _a.arrowProps;
                return (<TooltipContent id={_this.tooltipId} className="tooltip-content" aria-hidden={!isOpen} ref={ref} style={style} hide={!title} data-placement={placement} popperStyle={popperStyle} onMouseEnter={function () { return isHoverable && _this.handleOpen(); }} onMouseLeave={function () { return isHoverable && _this.handleClose(); }}>
              {title}
              <TooltipArrow ref={arrowProps.ref} data-placement={placement} style={arrowProps.style} background={((_b = popperStyle) === null || _b === void 0 ? void 0 : _b.background) || '#000'}/>
            </TooltipContent>);
            }}
        </Popper>, this.getPortal(usesGlobalPortal));
        }
        return (<Manager>
        <Reference>{function (_a) {
            var ref = _a.ref;
            return _this.renderTrigger(children, ref);
        }}</Reference>
        {tip}
      </Manager>);
    };
    Tooltip.propTypes = {
        disabled: PropTypes.bool,
        title: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
        position: PropTypes.oneOf([
            'bottom',
            'top',
            'left',
            'right',
            'bottom-start',
            'bottom-end',
            'top-start',
            'top-end',
            'left-start',
            'left-end',
            'right-start',
            'right-end',
            'auto',
        ]),
        popperStyle: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
        containerDisplayMode: PropTypes.string,
        delay: PropTypes.number,
        isHoverable: PropTypes.bool,
        skipWrapper: PropTypes.bool,
    };
    Tooltip.defaultProps = {
        position: 'top',
        containerDisplayMode: 'inline-block',
    };
    return Tooltip;
}(React.Component));
// Using an inline-block solves the container being smaller
// than the elements it is wrapping
var Container = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  max-width: 100%;\n"], ["\n  ", ";\n  max-width: 100%;\n"])), function (p) { return p.containerDisplayMode && "display: " + p.containerDisplayMode; });
var TooltipContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  background: #000;\n  opacity: 0.9;\n  padding: 5px 10px;\n  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);\n  border-radius: ", ";\n  overflow-wrap: break-word;\n  max-width: 225px;\n  z-index: ", ";\n\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1.4;\n\n  margin: 6px;\n  text-align: center;\n  ", ";\n  ", ";\n"], ["\n  color: ", ";\n  background: #000;\n  opacity: 0.9;\n  padding: 5px 10px;\n  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);\n  border-radius: ", ";\n  overflow-wrap: break-word;\n  max-width: 225px;\n  z-index: ", ";\n\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1.4;\n\n  margin: 6px;\n  text-align: center;\n  ", ";\n  ", ";\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.zIndex.tooltip; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.popperStyle; }, function (p) { return p.hide && "display: none"; });
var TooltipArrow = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  width: 10px;\n  height: 5px;\n\n  &[data-placement*='bottom'] {\n    top: 0;\n    left: 0;\n    margin-top: -5px;\n    &::before {\n      border-width: 0 5px 5px 5px;\n      border-color: transparent transparent ", " transparent;\n    }\n  }\n\n  &[data-placement*='top'] {\n    bottom: 0;\n    left: 0;\n    margin-bottom: -5px;\n    &::before {\n      border-width: 5px 5px 0 5px;\n      border-color: ", " transparent transparent transparent;\n    }\n  }\n\n  &[data-placement*='right'] {\n    left: 0;\n    margin-left: -5px;\n    &::before {\n      border-width: 5px 5px 5px 0;\n      border-color: transparent ", " transparent transparent;\n    }\n  }\n\n  &[data-placement*='left'] {\n    right: 0;\n    margin-right: -5px;\n    &::before {\n      border-width: 5px 0 5px 5px;\n      border-color: transparent transparent transparent ", ";\n    }\n  }\n\n  &::before {\n    content: '';\n    margin: auto;\n    display: block;\n    width: 0;\n    height: 0;\n    border-style: solid;\n  }\n"], ["\n  position: absolute;\n  width: 10px;\n  height: 5px;\n\n  &[data-placement*='bottom'] {\n    top: 0;\n    left: 0;\n    margin-top: -5px;\n    &::before {\n      border-width: 0 5px 5px 5px;\n      border-color: transparent transparent ", " transparent;\n    }\n  }\n\n  &[data-placement*='top'] {\n    bottom: 0;\n    left: 0;\n    margin-bottom: -5px;\n    &::before {\n      border-width: 5px 5px 0 5px;\n      border-color: ", " transparent transparent transparent;\n    }\n  }\n\n  &[data-placement*='right'] {\n    left: 0;\n    margin-left: -5px;\n    &::before {\n      border-width: 5px 5px 5px 0;\n      border-color: transparent ", " transparent transparent;\n    }\n  }\n\n  &[data-placement*='left'] {\n    right: 0;\n    margin-right: -5px;\n    &::before {\n      border-width: 5px 0 5px 5px;\n      border-color: transparent transparent transparent ", ";\n    }\n  }\n\n  &::before {\n    content: '';\n    margin: auto;\n    display: block;\n    width: 0;\n    height: 0;\n    border-style: solid;\n  }\n"])), function (p) { return p.background; }, function (p) { return p.background; }, function (p) { return p.background; }, function (p) { return p.background; });
export default Tooltip;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=tooltip.jsx.map