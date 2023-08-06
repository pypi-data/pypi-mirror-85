import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AutoComplete from 'app/components/autoComplete';
import DropdownBubble from 'app/components/dropdownBubble';
import Input from 'app/views/settings/components/forms/controls/input';
import LoadingIndicator from 'app/components/loadingIndicator';
import space from 'app/styles/space';
import List from './list';
import autoCompleteFilter from './autoCompleteFilter';
var Menu = function (_a) {
    var _b = _a.maxHeight, maxHeight = _b === void 0 ? 300 : _b, _c = _a.emptyMessage, emptyMessage = _c === void 0 ? t('No items') : _c, _d = _a.searchPlaceholder, searchPlaceholder = _d === void 0 ? t('Filter search') : _d, _e = _a.blendCorner, blendCorner = _e === void 0 ? true : _e, _f = _a.alignMenu, alignMenu = _f === void 0 ? 'left' : _f, _g = _a.hideInput, hideInput = _g === void 0 ? false : _g, _h = _a.busy, busy = _h === void 0 ? false : _h, _j = _a.busyItemsStillVisible, busyItemsStillVisible = _j === void 0 ? false : _j, _k = _a.menuWithArrow, menuWithArrow = _k === void 0 ? false : _k, _l = _a.disabled, disabled = _l === void 0 ? false : _l, itemSize = _a.itemSize, virtualizedHeight = _a.virtualizedHeight, virtualizedLabelHeight = _a.virtualizedLabelHeight, menuProps = _a.menuProps, noResultsMessage = _a.noResultsMessage, inputProps = _a.inputProps, children = _a.children, rootClassName = _a.rootClassName, className = _a.className, emptyHidesInput = _a.emptyHidesInput, menuHeader = _a.menuHeader, filterValue = _a.filterValue, items = _a.items, menuFooter = _a.menuFooter, style = _a.style, onScroll = _a.onScroll, inputActions = _a.inputActions, onChange = _a.onChange, onSelect = _a.onSelect, onOpen = _a.onOpen, onClose = _a.onClose, css = _a.css, closeOnSelect = _a.closeOnSelect, props = __rest(_a, ["maxHeight", "emptyMessage", "searchPlaceholder", "blendCorner", "alignMenu", "hideInput", "busy", "busyItemsStillVisible", "menuWithArrow", "disabled", "itemSize", "virtualizedHeight", "virtualizedLabelHeight", "menuProps", "noResultsMessage", "inputProps", "children", "rootClassName", "className", "emptyHidesInput", "menuHeader", "filterValue", "items", "menuFooter", "style", "onScroll", "inputActions", "onChange", "onSelect", "onOpen", "onClose", "css", "closeOnSelect"]);
    return (<AutoComplete itemToString={function () { return ''; }} onSelect={onSelect} inputIsActor={false} onOpen={onOpen} onClose={onClose} disabled={disabled} closeOnSelect={closeOnSelect} resetInputOnClose {...props}>
    {function (_a) {
        var getActorProps = _a.getActorProps, getRootProps = _a.getRootProps, getInputProps = _a.getInputProps, getMenuProps = _a.getMenuProps, getItemProps = _a.getItemProps, inputValue = _a.inputValue, selectedItem = _a.selectedItem, highlightedIndex = _a.highlightedIndex, isOpen = _a.isOpen, actions = _a.actions;
        // This is the value to use to filter (default to value in filter input)
        var filterValueOrInput = filterValue !== null && filterValue !== void 0 ? filterValue : inputValue;
        // Can't search if there are no items
        var hasItems = items && !!items.length;
        // Only filter results if menu is open and there are items
        var autoCompleteResults = (isOpen && hasItems && autoCompleteFilter(items, filterValueOrInput)) || [];
        // Items are loading if null
        var itemsLoading = items === null;
        // Has filtered results
        var hasResults = !!autoCompleteResults.length;
        // No items to display
        var showNoItems = !busy && !filterValueOrInput && !hasItems;
        // Results mean there was an attempt to search
        var showNoResultsMessage = !busy && !busyItemsStillVisible && filterValueOrInput && !hasResults;
        // Hide the input when we have no items to filter, only if
        // emptyHidesInput is set to true.
        var showInput = !hideInput && (hasItems || !emptyHidesInput);
        // When virtualization is turned on, we need to pass in the number of
        // selecteable items for arrow-key limits
        var itemCount = virtualizedHeight && autoCompleteResults.filter(function (i) { return !i.groupLabel; }).length;
        var renderedFooter = typeof menuFooter === 'function' ? menuFooter({ actions: actions }) : menuFooter;
        return (<AutoCompleteRoot {...getRootProps()} className={rootClassName}>
          {children({
            getInputProps: getInputProps,
            getActorProps: getActorProps,
            actions: actions,
            isOpen: isOpen,
            selectedItem: selectedItem,
        })}
          {isOpen && (<BubbleWithMinWidth className={className} {...getMenuProps(__assign(__assign({}, menuProps), { style: style,
            css: css,
            itemCount: itemCount,
            blendCorner: blendCorner,
            alignMenu: alignMenu,
            menuWithArrow: menuWithArrow }))}>
              {itemsLoading && <LoadingIndicator mini/>}
              {showInput && (<InputWrapper>
                  <StyledInput autoFocus placeholder={searchPlaceholder} {...getInputProps(__assign(__assign({}, inputProps), { onChange: onChange }))}/>
                  <InputLoadingWrapper>
                    {(busy || busyItemsStillVisible) && (<LoadingIndicator size={16} mini/>)}
                  </InputLoadingWrapper>
                  {inputActions}
                </InputWrapper>)}
              <div>
                {menuHeader && <LabelWithPadding>{menuHeader}</LabelWithPadding>}
                <ItemList data-test-id="autocomplete-list" maxHeight={maxHeight}>
                  {showNoItems && <EmptyMessage>{emptyMessage}</EmptyMessage>}
                  {showNoResultsMessage && (<EmptyMessage>
                      {noResultsMessage !== null && noResultsMessage !== void 0 ? noResultsMessage : emptyMessage + " " + t('found')}
                    </EmptyMessage>)}
                  {busy && (<BusyMessage>
                      <EmptyMessage>{t('Searching\u2026')}</EmptyMessage>
                    </BusyMessage>)}
                  {!busy && (<List items={autoCompleteResults} maxHeight={maxHeight} highlightedIndex={highlightedIndex} inputValue={inputValue} onScroll={onScroll} getItemProps={getItemProps} virtualizedLabelHeight={virtualizedLabelHeight} virtualizedHeight={virtualizedHeight} itemSize={itemSize}/>)}
                </ItemList>
                {renderedFooter && <LabelWithPadding>{renderedFooter}</LabelWithPadding>}
              </div>
            </BubbleWithMinWidth>)}
        </AutoCompleteRoot>);
    }}
  </AutoComplete>);
};
export default Menu;
var StyledInput = styled(Input)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  border: 1px solid transparent;\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    border: 0;\n    box-shadow: none;\n    font-size: 13px;\n    padding: ", ";\n    font-weight: normal;\n    color: ", ";\n  }\n"], ["\n  flex: 1;\n  border: 1px solid transparent;\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    border: 0;\n    box-shadow: none;\n    font-size: 13px;\n    padding: ", ";\n    font-weight: normal;\n    color: ", ";\n  }\n"])), space(1), function (p) { return p.theme.gray300; });
var InputLoadingWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  background: ", ";\n  align-items: center;\n  flex-shrink: 0;\n  width: 30px;\n  .loading.mini {\n    height: 16px;\n    margin: 0;\n  }\n"], ["\n  display: flex;\n  background: ", ";\n  align-items: center;\n  flex-shrink: 0;\n  width: 30px;\n  .loading.mini {\n    height: 16px;\n    margin: 0;\n  }\n"])), function (p) { return p.theme.background; });
var EmptyMessage = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", ";\n  text-align: center;\n  text-transform: none;\n"], ["\n  color: ", ";\n  padding: ", ";\n  text-align: center;\n  text-transform: none;\n"])), function (p) { return p.theme.gray200; }, space(2));
export var AutoCompleteRoot = styled(function (_a) {
    var _isOpen = _a.isOpen, props = __rest(_a, ["isOpen"]);
    return (<div {...props}/>);
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  display: inline-block;\n"], ["\n  position: relative;\n  display: inline-block;\n"])));
var BubbleWithMinWidth = styled(DropdownBubble)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  min-width: 250px;\n"], ["\n  min-width: 250px;\n"])));
var InputWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  border-radius: ", ";\n  align-items: center;\n"], ["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  border-radius: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.borderRadius + " " + p.theme.borderRadius + " 0 0"; });
var LabelWithPadding = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  border-width: 1px 0;\n  color: ", ";\n  font-size: ", ";\n  &:first-child {\n    border-top: none;\n  }\n  &:last-child {\n    border-bottom: none;\n  }\n  padding: ", " ", ";\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  border-width: 1px 0;\n  color: ", ";\n  font-size: ", ";\n  &:first-child {\n    border-top: none;\n  }\n  &:last-child {\n    border-bottom: none;\n  }\n  padding: ", " ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(0.25), space(1));
var ItemList = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  max-height: ", ";\n  overflow-y: auto;\n"], ["\n  max-height: ", ";\n  overflow-y: auto;\n"])), function (p) { return p.maxHeight + "px"; });
var BusyMessage = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=menu.jsx.map