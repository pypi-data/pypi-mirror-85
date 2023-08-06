import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import styled from '@emotion/styled';
import { Manager, Reference, Popper } from 'react-popper';
import { t } from 'app/locale';
import { IconEllipsis } from 'app/icons';
import space from 'app/styles/space';
import { getAggregateAlias } from 'app/utils/discover/fields';
export var Actions;
(function (Actions) {
    Actions["ADD"] = "add";
    Actions["EXCLUDE"] = "exclude";
    Actions["SHOW_GREATER_THAN"] = "show_greater_than";
    Actions["SHOW_LESS_THAN"] = "show_less_than";
    Actions["TRANSACTION"] = "transaction";
    Actions["RELEASE"] = "release";
    Actions["DRILLDOWN"] = "drilldown";
})(Actions || (Actions = {}));
export function updateQuery(results, action, key, value) {
    switch (action) {
        case Actions.ADD:
            // If the value is null/undefined create a has !has condition.
            if (value === null || value === undefined) {
                // Adding a null value is the same as excluding truthy values.
                // Remove inclusion if it exists.
                results.removeTagValue('has', key);
                results.addTagValues('!has', [key]);
            }
            else {
                // Remove exclusion if it exists.
                results.removeTag("!" + key).setTagValues(key, ["" + value]);
            }
            break;
        case Actions.EXCLUDE:
            if (value === null || value === undefined) {
                // Excluding a null value is the same as including truthy values.
                // Remove exclusion if it exists.
                results.removeTagValue('!has', key);
                results.addTagValues('has', [key]);
            }
            else {
                // Remove positive if it exists.
                results.removeTag(key);
                // Negations should stack up.
                var negation = "!" + key;
                results.addTagValues(negation, ["" + value]);
            }
            break;
        case Actions.SHOW_GREATER_THAN: {
            // Remove query token if it already exists
            results.setTagValues(key, [">" + value]);
            break;
        }
        case Actions.SHOW_LESS_THAN: {
            // Remove query token if it already exists
            results.setTagValues(key, ["<" + value]);
            break;
        }
        // these actions do not modify the query in any way,
        // instead they have side effects
        case Actions.TRANSACTION:
        case Actions.RELEASE:
        case Actions.DRILLDOWN:
            break;
        default:
            throw new Error("Unknown action type. " + action);
    }
}
var CellAction = /** @class */ (function (_super) {
    __extends(CellAction, _super);
    function CellAction(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isHovering: false,
            isOpen: false,
        };
        _this.handleClickOutside = function (event) {
            if (!_this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (_this.menuEl.contains(event.target)) {
                return;
            }
            _this.setState({ isOpen: false, isHovering: false });
        };
        _this.handleMouseEnter = function () {
            _this.setState({ isHovering: true });
        };
        _this.handleMouseLeave = function () {
            _this.setState(function (state) {
                // Don't hide the button if the menu is open.
                if (state.isOpen) {
                    return state;
                }
                return __assign(__assign({}, state), { isHovering: false });
            });
        };
        _this.handleMenuToggle = function (event) {
            event.preventDefault();
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        var portal = document.getElementById('cell-action-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'cell-action-portal');
            document.body.appendChild(portal);
        }
        _this.portalEl = portal;
        _this.menuEl = null;
        return _this;
    }
    CellAction.prototype.componentDidUpdate = function (_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    };
    CellAction.prototype.componentWillUnmount = function () {
        document.removeEventListener('click', this.handleClickOutside, true);
    };
    CellAction.prototype.renderMenuButtons = function () {
        var _a = this.props, dataRow = _a.dataRow, column = _a.column, handleCellAction = _a.handleCellAction, allowActions = _a.allowActions;
        var fieldAlias = getAggregateAlias(column.name);
        // Slice out the last element from array values as that is the value
        // we show. See utils/discover/fieldRenderers.tsx and how
        // strings and error.handled are rendered.
        var value = dataRow[fieldAlias];
        if (Array.isArray(value)) {
            value = value.slice(-1)[0];
        }
        // error.handled is a strange field where null = true.
        if (value === null &&
            column.column.kind === 'field' &&
            column.column.field === 'error.handled') {
            value = 1;
        }
        var actions = [];
        function addMenuItem(action, menuItem) {
            if ((Array.isArray(allowActions) && allowActions.includes(action)) ||
                !allowActions) {
                actions.push(menuItem);
            }
        }
        if (!['duration', 'number', 'percentage'].includes(column.type) ||
            (value === null && column.column.kind === 'field')) {
            addMenuItem(Actions.ADD, <ActionItem key="add-to-filter" data-test-id="add-to-filter" onClick={function () { return handleCellAction(Actions.ADD, value); }}>
          {t('Add to filter')}
        </ActionItem>);
            if (column.type !== 'date') {
                addMenuItem(Actions.EXCLUDE, <ActionItem key="exclude-from-filter" data-test-id="exclude-from-filter" onClick={function () { return handleCellAction(Actions.EXCLUDE, value); }}>
            {t('Exclude from filter')}
          </ActionItem>);
            }
        }
        if (['date', 'duration', 'integer', 'number', 'percentage'].includes(column.type) &&
            value !== null) {
            addMenuItem(Actions.SHOW_GREATER_THAN, <ActionItem key="show-values-greater-than" data-test-id="show-values-greater-than" onClick={function () { return handleCellAction(Actions.SHOW_GREATER_THAN, value); }}>
          {t('Show values greater than')}
        </ActionItem>);
            addMenuItem(Actions.SHOW_LESS_THAN, <ActionItem key="show-values-less-than" data-test-id="show-values-less-than" onClick={function () { return handleCellAction(Actions.SHOW_LESS_THAN, value); }}>
          {t('Show values less than')}
        </ActionItem>);
        }
        if (column.column.kind === 'field' && column.column.field === 'transaction') {
            addMenuItem(Actions.TRANSACTION, <ActionItem key="transaction-summary" data-test-id="transaction-summary" onClick={function () { return handleCellAction(Actions.TRANSACTION, value); }}>
          {t('Go to summary')}
        </ActionItem>);
        }
        if (column.column.kind === 'field' && column.column.field === 'release' && value) {
            addMenuItem(Actions.RELEASE, <ActionItem key="release" data-test-id="release" onClick={function () { return handleCellAction(Actions.RELEASE, value); }}>
          {t('Go to release')}
        </ActionItem>);
        }
        if (column.column.kind === 'function' &&
            column.column.function[0] === 'count_unique') {
            addMenuItem(Actions.DRILLDOWN, <ActionItem key="drilldown" data-test-id="per-cell-drilldown" onClick={function () { return handleCellAction(Actions.DRILLDOWN, value); }}>
          {t('View Stacks')}
        </ActionItem>);
        }
        if (actions.length === 0) {
            return null;
        }
        return (<MenuButtons onClick={function (event) {
            // prevent clicks from propagating further
            event.stopPropagation();
        }}>
        {actions}
      </MenuButtons>);
    };
    CellAction.prototype.renderMenu = function () {
        var _this = this;
        var isOpen = this.state.isOpen;
        var menuButtons = this.renderMenuButtons();
        if (menuButtons === null) {
            // do not render the menu if there are no per cell actions
            return null;
        }
        var modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        var menu = null;
        if (isOpen) {
            menu = ReactDOM.createPortal(<Popper placement="top" modifiers={modifiers}>
          {function (_a) {
                var popperRef = _a.ref, style = _a.style, placement = _a.placement, arrowProps = _a.arrowProps;
                return (<Menu ref={function (ref) {
                    popperRef(ref);
                    _this.menuEl = ref;
                }} style={style}>
              <MenuArrow ref={arrowProps.ref} data-placement={placement} style={arrowProps.style}/>
              {menuButtons}
            </Menu>);
            }}
        </Popper>, this.portalEl);
        }
        return (<MenuRoot>
        <Manager>
          <Reference>
            {function (_a) {
            var ref = _a.ref;
            return (<MenuButton ref={ref} onClick={_this.handleMenuToggle}>
                <IconEllipsis size="sm" data-test-id="cell-action" color="blue300"/>
              </MenuButton>);
        }}
          </Reference>
          {menu}
        </Manager>
      </MenuRoot>);
    };
    CellAction.prototype.render = function () {
        var children = this.props.children;
        var isHovering = this.state.isHovering;
        return (<Container onMouseEnter={this.handleMouseEnter} onMouseLeave={this.handleMouseLeave}>
        {children}
        {isHovering && this.renderMenu()}
      </Container>);
    };
    return CellAction;
}(React.Component));
export default CellAction;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  height: 100%;\n"], ["\n  position: relative;\n  width: 100%;\n  height: 100%;\n"])));
var MenuRoot = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n"])));
var Menu = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: ", " 0;\n\n  z-index: ", ";\n"], ["\n  margin: ", " 0;\n\n  z-index: ", ";\n"])), space(1), function (p) { return p.theme.zIndex.tooltip; });
var MenuButtons = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  overflow: hidden;\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  overflow: hidden;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowHeavy; });
var MenuArrow = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  width: 18px;\n  height: 9px;\n  /* left and top set by popper */\n\n  &[data-placement*='bottom'] {\n    margin-top: -9px;\n    &::before {\n      border-width: 0 9px 9px 9px;\n      border-color: transparent transparent ", " transparent;\n    }\n    &::after {\n      top: 1px;\n      left: 1px;\n      border-width: 0 8px 8px 8px;\n      border-color: transparent transparent ", " transparent;\n    }\n  }\n  &[data-placement*='top'] {\n    margin-bottom: -8px;\n    bottom: 0;\n    &::before {\n      border-width: 9px 9px 0 9px;\n      border-color: ", " transparent transparent transparent;\n    }\n    &::after {\n      bottom: 1px;\n      left: 1px;\n      border-width: 8px 8px 0 8px;\n      border-color: ", " transparent transparent transparent;\n    }\n  }\n\n  &::before,\n  &::after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    border-style: solid;\n  }\n"], ["\n  position: absolute;\n  width: 18px;\n  height: 9px;\n  /* left and top set by popper */\n\n  &[data-placement*='bottom'] {\n    margin-top: -9px;\n    &::before {\n      border-width: 0 9px 9px 9px;\n      border-color: transparent transparent ", " transparent;\n    }\n    &::after {\n      top: 1px;\n      left: 1px;\n      border-width: 0 8px 8px 8px;\n      border-color: transparent transparent ", " transparent;\n    }\n  }\n  &[data-placement*='top'] {\n    margin-bottom: -8px;\n    bottom: 0;\n    &::before {\n      border-width: 9px 9px 0 9px;\n      border-color: ", " transparent transparent transparent;\n    }\n    &::after {\n      bottom: 1px;\n      left: 1px;\n      border-width: 8px 8px 0 8px;\n      border-color: ", " transparent transparent transparent;\n    }\n  }\n\n  &::before,\n  &::after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    border-style: solid;\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; });
var ActionItem = styled('button')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  padding: ", " ", ";\n  background: transparent;\n\n  outline: none;\n  border: 0;\n  border-bottom: 1px solid ", ";\n\n  font-size: ", ";\n  text-align: left;\n  line-height: 1.2;\n\n  &:hover {\n    background: ", ";\n  }\n\n  &:last-child {\n    border-bottom: 0;\n  }\n"], ["\n  display: block;\n  width: 100%;\n  padding: ", " ", ";\n  background: transparent;\n\n  outline: none;\n  border: 0;\n  border-bottom: 1px solid ", ";\n\n  font-size: ", ";\n  text-align: left;\n  line-height: 1.2;\n\n  &:hover {\n    background: ", ";\n  }\n\n  &:last-child {\n    border-bottom: 0;\n  }\n"])), space(1), space(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.backgroundSecondary; });
var MenuButton = styled('button')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  width: 24px;\n  height: 24px;\n  padding: 0;\n  justify-content: center;\n  align-items: center;\n\n  background: rgba(255, 255, 255, 0.85);\n  border-radius: ", ";\n  border: 1px solid ", ";\n  cursor: pointer;\n  outline: none;\n"], ["\n  display: flex;\n  width: 24px;\n  height: 24px;\n  padding: 0;\n  justify-content: center;\n  align-items: center;\n\n  background: rgba(255, 255, 255, 0.85);\n  border-radius: ", ";\n  border: 1px solid ", ";\n  cursor: pointer;\n  outline: none;\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.border; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=cellAction.jsx.map