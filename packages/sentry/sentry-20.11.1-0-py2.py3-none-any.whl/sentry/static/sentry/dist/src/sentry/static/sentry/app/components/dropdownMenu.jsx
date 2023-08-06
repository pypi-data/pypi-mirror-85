import { __assign, __awaiter, __extends, __generator, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import * as Sentry from '@sentry/react';
import { MENU_CLOSE_DELAY } from 'app/constants';
var DropdownMenu = /** @class */ (function (_super) {
    __extends(DropdownMenu, _super);
    function DropdownMenu() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.dropdownMenu = null;
        _this.dropdownActor = null;
        _this.mouseLeaveId = null;
        _this.mouseEnterId = null;
        // Gets open state from props or local state when appropriate
        _this.isOpen = function () {
            var isOpen = _this.props.isOpen;
            var isControlled = typeof isOpen !== 'undefined';
            return (isControlled && isOpen) || _this.state.isOpen;
        };
        // Checks if click happens inside of dropdown menu (or its button)
        // Closes dropdownmenu if it is "outside"
        _this.checkClickOutside = function (e) { return __awaiter(_this, void 0, void 0, function () {
            var _a, onClickOutside, shouldIgnoreClickOutside;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, onClickOutside = _a.onClickOutside, shouldIgnoreClickOutside = _a.shouldIgnoreClickOutside;
                        if (!this.dropdownMenu) {
                            return [2 /*return*/];
                        }
                        if (!(e.target instanceof Element)) {
                            return [2 /*return*/];
                        }
                        // Dropdown menu itself
                        if (this.dropdownMenu.contains(e.target)) {
                            return [2 /*return*/];
                        }
                        if (!this.dropdownActor) {
                            // Log an error, should be lower priority
                            Sentry.withScope(function (scope) {
                                scope.setLevel(Sentry.Severity.Warning);
                                Sentry.captureException(new Error('DropdownMenu does not have "Actor" attached'));
                            });
                        }
                        // Button that controls visibility of dropdown menu
                        if (this.dropdownActor && this.dropdownActor.contains(e.target)) {
                            return [2 /*return*/];
                        }
                        if (typeof shouldIgnoreClickOutside === 'function' && shouldIgnoreClickOutside(e)) {
                            return [2 /*return*/];
                        }
                        if (typeof onClickOutside === 'function') {
                            onClickOutside(e);
                        }
                        // Wait until the current macrotask completes, in the case that the click
                        // happened on a hovercard or some other element rendered outside of the
                        // dropdown, but controlled by the existence of the dropdown, we need to
                        // ensure any click handlers are run.
                        return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve); })];
                    case 1:
                        // Wait until the current macrotask completes, in the case that the click
                        // happened on a hovercard or some other element rendered outside of the
                        // dropdown, but controlled by the existence of the dropdown, we need to
                        // ensure any click handlers are run.
                        _b.sent();
                        this.handleClose(null);
                        return [2 /*return*/];
                }
            });
        }); };
        // Opens dropdown menu
        _this.handleOpen = function (e) {
            var _a = _this.props, onOpen = _a.onOpen, isOpen = _a.isOpen, alwaysRenderMenu = _a.alwaysRenderMenu;
            var isControlled = typeof isOpen !== 'undefined';
            if (!isControlled) {
                _this.setState({
                    isOpen: true,
                });
            }
            if (_this.mouseLeaveId) {
                window.clearTimeout(_this.mouseLeaveId);
            }
            // If we always render menu (e.g. DropdownLink), then add the check click outside handlers when we open the menu
            // instead of when the menu component mounts. Otherwise we will have many click handlers attached on initial load.
            if (alwaysRenderMenu) {
                document.addEventListener('click', _this.checkClickOutside, true);
            }
            if (typeof onOpen === 'function') {
                onOpen(e);
            }
        };
        // Decide whether dropdown should be closed when mouse leaves element
        // Only for nested dropdowns
        _this.handleMouseLeave = function (e) {
            var isNestedDropdown = _this.props.isNestedDropdown;
            if (!isNestedDropdown) {
                return;
            }
            var toElement = e.relatedTarget;
            try {
                if (_this.dropdownMenu &&
                    (!(toElement instanceof Element) || !_this.dropdownMenu.contains(toElement))) {
                    _this.mouseLeaveId = window.setTimeout(function () {
                        _this.handleClose(e);
                    }, MENU_CLOSE_DELAY);
                }
            }
            catch (err) {
                Sentry.withScope(function (scope) {
                    scope.setExtra('event', e);
                    scope.setExtra('relatedTarget', e.relatedTarget);
                    Sentry.captureException(err);
                });
            }
        };
        // Closes dropdown menu
        _this.handleClose = function (e) {
            var _a = _this.props, onClose = _a.onClose, isOpen = _a.isOpen, alwaysRenderMenu = _a.alwaysRenderMenu;
            var isControlled = typeof isOpen !== 'undefined';
            if (!isControlled) {
                _this.setState({ isOpen: false });
            }
            // Clean up click handlers when the menu is closed for menus that are always rendered,
            // otherwise the click handlers get cleaned up when menu is unmounted
            if (alwaysRenderMenu) {
                document.removeEventListener('click', _this.checkClickOutside, true);
            }
            if (typeof onClose === 'function') {
                onClose(e);
            }
        };
        // When dropdown menu is displayed and mounted to DOM,
        // bind a click handler to `document` to listen for clicks outside of
        // this component and close menu if so
        _this.handleMenuMount = function (ref) {
            if (ref && !(ref instanceof Element)) {
                return;
            }
            var alwaysRenderMenu = _this.props.alwaysRenderMenu;
            _this.dropdownMenu = ref;
            // Don't add document event listeners here if we are always rendering menu
            // Instead add when menu is opened
            if (alwaysRenderMenu) {
                return;
            }
            if (_this.dropdownMenu) {
                // 3rd arg = useCapture = so event capturing vs event bubbling
                document.addEventListener('click', _this.checkClickOutside, true);
            }
            else {
                document.removeEventListener('click', _this.checkClickOutside, true);
            }
        };
        _this.handleActorMount = function (ref) {
            if (ref && !(ref instanceof Element)) {
                return;
            }
            _this.dropdownActor = ref;
        };
        _this.handleToggle = function (e) {
            if (_this.isOpen()) {
                _this.handleClose(e);
            }
            else {
                _this.handleOpen(e);
            }
        };
        // Control whether we should hide dropdown menu when it is clicked
        _this.handleDropdownMenuClick = function (e) {
            if (_this.props.keepMenuOpen) {
                return;
            }
            _this.handleClose(e);
        };
        // Actor is the component that will open the dropdown menu
        _this.getActorProps = function (_a) {
            if (_a === void 0) { _a = {}; }
            var onClick = _a.onClick, onMouseEnter = _a.onMouseEnter, onMouseLeave = _a.onMouseLeave, onKeyDown = _a.onKeyDown, _b = _a.style, style = _b === void 0 ? {} : _b, props = __rest(_a, ["onClick", "onMouseEnter", "onMouseLeave", "onKeyDown", "style"]);
            var _c = _this.props, isNestedDropdown = _c.isNestedDropdown, closeOnEscape = _c.closeOnEscape;
            var refProps = { ref: _this.handleActorMount };
            // Props that the actor needs to have <DropdownMenu> work
            return __assign(__assign(__assign({}, props), refProps), { style: __assign(__assign({}, style), { outline: 'none' }), onKeyDown: function (e) {
                    if (typeof onKeyDown === 'function') {
                        onKeyDown(e);
                    }
                    if (e.key === 'Escape' && closeOnEscape) {
                        _this.handleClose(e);
                    }
                }, onMouseEnter: function (e) {
                    if (typeof onMouseEnter === 'function') {
                        onMouseEnter(e);
                    }
                    // Only handle mouse enter for nested dropdowns
                    if (!isNestedDropdown) {
                        return;
                    }
                    if (_this.mouseLeaveId) {
                        window.clearTimeout(_this.mouseLeaveId);
                    }
                    _this.mouseEnterId = window.setTimeout(function () {
                        _this.handleOpen(e);
                    }, MENU_CLOSE_DELAY);
                }, onMouseLeave: function (e) {
                    if (typeof onMouseLeave === 'function') {
                        onMouseLeave(e);
                    }
                    if (_this.mouseEnterId) {
                        window.clearTimeout(_this.mouseEnterId);
                    }
                    _this.handleMouseLeave(e);
                }, onClick: function (e) {
                    // If we are a nested dropdown, clicking the actor
                    // should be a no-op so that the menu doesn't close.
                    if (isNestedDropdown) {
                        e.preventDefault();
                        e.stopPropagation();
                        return;
                    }
                    _this.handleToggle(e);
                    if (typeof onClick === 'function') {
                        onClick(e);
                    }
                } });
        };
        // Menu is the menu component that <DropdownMenu> will control
        _this.getMenuProps = function (_a) {
            if (_a === void 0) { _a = {}; }
            var onClick = _a.onClick, onMouseLeave = _a.onMouseLeave, onMouseEnter = _a.onMouseEnter, props = __rest(_a, ["onClick", "onMouseLeave", "onMouseEnter"]);
            var refProps = { ref: _this.handleMenuMount };
            // Props that the menu needs to have <DropdownMenu> work
            return __assign(__assign(__assign({}, props), refProps), { onMouseEnter: function (e) {
                    if (typeof onMouseEnter === 'function') {
                        onMouseEnter(e);
                    }
                    // There is a delay before closing a menu on mouse leave, cancel this action if mouse enters menu again
                    if (_this.mouseLeaveId) {
                        window.clearTimeout(_this.mouseLeaveId);
                    }
                }, onMouseLeave: function (e) {
                    if (typeof onMouseLeave === 'function') {
                        onMouseLeave(e);
                    }
                    _this.handleMouseLeave(e);
                }, onClick: function (e) {
                    _this.handleDropdownMenuClick(e);
                    if (typeof onClick === 'function') {
                        onClick(e);
                    }
                } });
        };
        return _this;
    }
    DropdownMenu.prototype.componentWillUnmount = function () {
        document.removeEventListener('click', this.checkClickOutside, true);
    };
    DropdownMenu.prototype.getRootProps = function (props) {
        return props;
    };
    DropdownMenu.prototype.render = function () {
        var children = this.props.children;
        // Default anchor = left
        var shouldShowDropdown = this.isOpen();
        return children({
            isOpen: shouldShowDropdown,
            getRootProps: this.getRootProps,
            getActorProps: this.getActorProps,
            getMenuProps: this.getMenuProps,
            actions: {
                open: this.handleOpen,
                close: this.handleClose,
            },
        });
    };
    DropdownMenu.propTypes = {
        onOpen: PropTypes.func,
        onClose: PropTypes.func,
        onClickOutside: PropTypes.func,
        shouldIgnoreClickOutside: PropTypes.func,
        isOpen: PropTypes.bool,
        keepMenuOpen: PropTypes.bool,
        alwaysRenderMenu: PropTypes.bool,
        closeOnEscape: PropTypes.bool,
        isNestedDropdown: PropTypes.bool,
    };
    DropdownMenu.defaultProps = {
        keepMenuOpen: false,
        closeOnEscape: true,
    };
    return DropdownMenu;
}(React.Component));
export default DropdownMenu;
//# sourceMappingURL=dropdownMenu.jsx.map