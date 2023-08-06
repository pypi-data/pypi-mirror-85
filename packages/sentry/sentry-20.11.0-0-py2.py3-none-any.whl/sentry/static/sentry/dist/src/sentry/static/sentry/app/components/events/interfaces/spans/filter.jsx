import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { IconFilter } from 'app/icons';
import DropdownControl from 'app/components/dropdownControl';
import DropdownButton from 'app/components/dropdownButton';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import { pickSpanBarColour } from 'app/components/events/interfaces/spans/utils';
import overflowEllipsis from 'app/styles/overflowEllipsis';
export var noFilter = {
    type: 'no_filter',
};
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Filter.prototype.getOperationNames = function () {
        var parsedTrace = this.props.parsedTrace;
        var result = parsedTrace.spans.reduce(function (operationNames, span) {
            var operationName = span.op;
            if (typeof operationName === 'string' && operationName.length > 0) {
                if (!operationNames.includes(operationName)) {
                    operationNames.push(operationName);
                }
            }
            return operationNames;
        }, [parsedTrace.op]);
        // sort alphabetically using case insensitive comparison
        result.sort(function (a, b) { return a.localeCompare(b, undefined, { sensitivity: 'base' }); });
        return result;
    };
    Filter.prototype.isOperationNameActive = function (operationName) {
        var operationNameFilter = this.props.operationNameFilter;
        if (operationNameFilter.type === 'no_filter') {
            return false;
        }
        // invariant: operationNameFilter.type === 'active_filter'
        return operationNameFilter.operationNames.has(operationName);
    };
    Filter.prototype.getNumberOfActiveFilters = function () {
        var operationNameFilter = this.props.operationNameFilter;
        if (operationNameFilter.type === 'no_filter') {
            return 0;
        }
        return operationNameFilter.operationNames.size;
    };
    Filter.prototype.render = function () {
        var _this = this;
        var operationNames = this.getOperationNames();
        if (operationNames.length === 0) {
            return null;
        }
        var checkedQuantity = this.getNumberOfActiveFilters();
        var dropDownButtonProps = {
            children: (<React.Fragment>
          <IconFilter size="xs"/>
          <FilterLabel>{t('Filter')}</FilterLabel>
        </React.Fragment>),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = (<span>{tn('%s Active Filter', '%s Active Filters', checkedQuantity)}</span>);
            dropDownButtonProps.priority = 'primary';
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<Wrapper data-test-id="op-filter-dropdown">
        <DropdownControl menuWidth="240px" blendWithActor button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
              {dropDownButtonProps.children}
            </StyledDropdownButton>);
        }}>
          <MenuContent onClick={function (event) {
            // propagated clicks will dismiss the menu; we stop this here
            event.stopPropagation();
        }}>
            <Header>
              <span>{t('Operation')}</span>
              <CheckboxFancy isChecked={checkedQuantity > 0} isIndeterminate={checkedQuantity > 0 && checkedQuantity !== operationNames.length} onClick={function (event) {
            event.stopPropagation();
            _this.props.toggleAllOperationNameFilters(operationNames);
        }}/>
            </Header>
            <List>
              {operationNames.map(function (operationName) {
            var isActive = _this.isOperationNameActive(operationName);
            return (<ListItem key={operationName} isChecked={isActive}>
                    <OperationDot backgroundColor={pickSpanBarColour(operationName)}/>
                    <OperationName>{operationName}</OperationName>
                    <CheckboxFancy isChecked={isActive} onClick={function (event) {
                event.stopPropagation();
                _this.props.toggleOperationNameFilter(operationName);
            }}/>
                  </ListItem>);
        })}
            </List>
          </MenuContent>
        </DropdownControl>
      </Wrapper>);
    };
    return Filter;
}(React.Component));
var FilterLabel = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"], ["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"])), space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ",
    "\n  }\n\n  ",
    "\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n          border-bottom-color: " + p.theme.button.primary.border + ";\n        ";
}, function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n      border-bottom-color: " + p.theme.button.primary.border + ";\n    ";
});
var MenuContent = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  max-height: 250px;\n  overflow-y: auto;\n  border-top: 1px solid ", ";\n"], ["\n  max-height: 250px;\n  overflow-y: auto;\n  border-top: 1px solid ", ";\n"])), function (p) { return p.theme.gray200; });
var Header = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var List = styled('ul')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled('li')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.3); }, CheckboxFancy, function (p) { return p.theme.blue300; });
var OperationDot = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"], ["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"])), space(1), function (p) { return p.backgroundColor; });
var OperationName = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis);
export function toggleFilter(previousState, operationName) {
    if (previousState.type === 'no_filter') {
        return {
            type: 'active_filter',
            operationNames: new Set([operationName]),
        };
    }
    // invariant: previousState.type === 'active_filter'
    // invariant: previousState.operationNames.size >= 1
    var operationNames = previousState.operationNames;
    if (operationNames.has(operationName)) {
        operationNames.delete(operationName);
    }
    else {
        operationNames.add(operationName);
    }
    if (operationNames.size > 0) {
        return {
            type: 'active_filter',
            operationNames: operationNames,
        };
    }
    return {
        type: 'no_filter',
    };
}
export function toggleAllFilters(previousState, operationNames) {
    if (previousState.type === 'no_filter') {
        return {
            type: 'active_filter',
            operationNames: new Set(operationNames),
        };
    }
    // invariant: previousState.type === 'active_filter'
    if (previousState.operationNames.size === operationNames.length) {
        // all filters were selected, so the next state should un-select all filters
        return {
            type: 'no_filter',
        };
    }
    // not all filters were selected, so the next state is to select all the remaining filters
    return {
        type: 'active_filter',
        operationNames: new Set(operationNames),
    };
}
export default Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=filter.jsx.map