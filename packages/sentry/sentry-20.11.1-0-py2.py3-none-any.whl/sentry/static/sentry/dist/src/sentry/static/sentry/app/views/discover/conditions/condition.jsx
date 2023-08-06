import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Value } from 'react-select-legacy';
import { t } from 'app/locale';
import space from 'app/styles/space';
import SelectControl from 'app/components/forms/selectControl';
import { getInternal, getExternal, isValidCondition, ignoreCase } from './utils';
import { CONDITION_OPERATORS, ARRAY_FIELD_PREFIXES } from '../data';
import { PlaceholderText } from '../styles';
var ConditionRow = /** @class */ (function (_super) {
    __extends(ConditionRow, _super);
    function ConditionRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            inputValue: '',
            isOpen: false,
        };
        _this.selectRef = React.createRef();
        _this.handleChange = function (option) {
            var external = getExternal(option.value, _this.props.columns);
            if (isValidCondition(external, _this.props.columns)) {
                _this.setState({
                    inputValue: '',
                    isOpen: false,
                }, function () {
                    _this.props.onChange(external);
                });
                return;
            }
            _this.setState({
                inputValue: option.value,
            }, _this.focus);
        };
        _this.handleOpen = function () {
            if (_this.state.inputValue === '') {
                _this.setState({
                    inputValue: getInternal(_this.props.value),
                    isOpen: true,
                });
            }
        };
        _this.filterOptions = function (options) {
            var input = _this.state.inputValue;
            var optionList = options;
            var external = getExternal(input, _this.props.columns);
            var isValid = isValidCondition(external, _this.props.columns);
            if (isValid) {
                return [];
            }
            var hasSelectedColumn = external[0] !== null;
            var hasSelectedOperator = external[1] !== null;
            if (!hasSelectedColumn) {
                optionList = _this.props.columns.map(function (_a) {
                    var name = _a.name;
                    return ({
                        value: "" + name,
                        label: name + "...",
                    });
                });
            }
            if (hasSelectedColumn && !hasSelectedOperator) {
                var selectedColumn_1 = "" + external[0];
                optionList = _this.getConditionsForColumn(selectedColumn_1).map(function (op) {
                    var value = selectedColumn_1 + " " + op;
                    return {
                        value: value,
                        label: value,
                    };
                });
            }
            return optionList.filter(function (_a) {
                var label = _a.label;
                return label.includes(input);
            });
        };
        _this.isValidNewOption = function (_a) {
            var label = _a.label;
            label = ignoreCase(label);
            return isValidCondition(getExternal(label, _this.props.columns), _this.props.columns);
        };
        _this.inputRenderer = function (props) {
            var onChange = function (evt) {
                if (evt.target && evt.target.value === '') {
                    evt.persist();
                    // React select won't trigger an onChange event when a value is completely
                    // cleared, so we'll force this before calling onChange
                    _this.setState({ inputValue: evt.target.value }, function () {
                        props.onChange(evt);
                    });
                }
                else {
                    props.onChange(evt);
                }
            };
            return (<input type="text" {...props} onChange={onChange} value={_this.state.inputValue} style={{ width: '100%', border: 0, zIndex: 1000, backgroundColor: 'transparent' }}/>);
        };
        _this.valueComponent = function (props) {
            if (_this.state.inputValue) {
                return null;
            }
            return <Value {...props}/>;
        };
        _this.shouldKeyDownEventCreateNewOption = function (keyCode) {
            var createKeyCodes = new Set([13, 9]); // ENTER, TAB
            return createKeyCodes.has(keyCode);
        };
        _this.handleInputChange = function (value) {
            _this.setState({
                inputValue: ignoreCase(value),
            });
            return value;
        };
        _this.handleBlur = function (evt) {
            var external = getExternal(evt.target.value, _this.props.columns);
            var isValid = isValidCondition(external, _this.props.columns);
            if (isValid) {
                _this.setState({
                    inputValue: '',
                }, function () {
                    _this.props.onChange(external);
                });
            }
        };
        _this.newOptionCreator = function (_a) {
            var _b;
            var label = _a.label, labelKey = _a.labelKey, valueKey = _a.valueKey;
            label = ignoreCase(label);
            return _b = {},
                _b[valueKey] = label,
                _b[labelKey] = label,
                _b;
        };
        return _this;
    }
    ConditionRow.prototype.focus = function () {
        if (this.selectRef.current) {
            this.selectRef.current.focus();
        }
    };
    ConditionRow.prototype.getOptions = function () {
        var currentValue = getInternal(this.props.value);
        var shouldDisplayValue = currentValue || this.state.inputValue;
        return shouldDisplayValue ? [{ label: currentValue, value: currentValue }] : [];
    };
    ConditionRow.prototype.getConditionsForColumn = function (colName) {
        var column = this.props.columns.find(function (_a) {
            var name = _a.name;
            return name === colName;
        });
        var colType = column ? column.type : 'string';
        var numberOnlyOperators = new Set(['>', '<', '>=', '<=']);
        var stringOnlyOperators = new Set(['LIKE', 'NOT LIKE']);
        return CONDITION_OPERATORS.filter(function (operator) {
            if (colType === 'number' || colType === 'datetime') {
                return !stringOnlyOperators.has(operator);
            }
            // We currently only support =, !=, LIKE and NOT LIKE on array fields
            if (ARRAY_FIELD_PREFIXES.some(function (prefix) { return colName.startsWith(prefix); })) {
                return ['=', '!=', 'LIKE', 'NOT LIKE'].includes(operator);
            }
            // Treat everything else like a string
            return !numberOnlyOperators.has(operator);
        });
    };
    ConditionRow.prototype.render = function () {
        return (<Box>
        <SelectControl deprecatedSelectControl ref={this.selectRef} value={getInternal(this.props.value)} placeholder={<PlaceholderText>{t('Add condition...')}</PlaceholderText>} options={this.getOptions()} filterOptions={this.filterOptions} onChange={this.handleChange} onOpen={this.handleOpen} closeOnSelect openOnFocus autoBlur clearable={false} backspaceRemoves={false} deleteRemoves={false} isValidNewOption={this.isValidNewOption} inputRenderer={this.inputRenderer} valueComponent={this.valueComponent} onInputChange={this.handleInputChange} onBlur={this.handleBlur} creatable promptTextCreator={function (text) { return text; }} shouldKeyDownEventCreateNewOption={this.shouldKeyDownEventCreateNewOption} disabled={this.props.disabled} newOptionCreator={this.newOptionCreator}/>
      </Box>);
    };
    return ConditionRow;
}(React.Component));
export default ConditionRow;
var Box = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  margin-right: ", ";\n"], ["\n  width: 100%;\n  margin-right: ", ";\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=condition.jsx.map