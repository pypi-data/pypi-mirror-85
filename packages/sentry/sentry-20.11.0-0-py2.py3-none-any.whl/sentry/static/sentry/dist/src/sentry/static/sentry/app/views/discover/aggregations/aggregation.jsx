import { __extends } from "tslib";
import React from 'react';
import { Value } from 'react-select-legacy';
import { t } from 'app/locale';
import SelectControl from 'app/components/forms/selectControl';
import { getInternal, getExternal } from './utils';
import { PlaceholderText } from '../styles';
import { ARRAY_FIELD_PREFIXES } from '../data';
var initialState = {
    inputValue: '',
    isOpen: false,
};
var AggregationRow = /** @class */ (function (_super) {
    __extends(AggregationRow, _super);
    function AggregationRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.filterOptions = function () {
            var input = _this.state.inputValue;
            var optionList = [
                { value: 'count', label: 'count' },
                { value: 'uniq', label: 'uniq(...)' },
                { value: 'avg', label: 'avg(...)' },
                { value: 'sum', label: 'sum(...)' },
            ];
            if (input.startsWith('uniq')) {
                optionList = _this.props.columns
                    .filter(function (_a) {
                    var name = _a.name;
                    return !ARRAY_FIELD_PREFIXES.some(function (prefix) { return name.startsWith(prefix); });
                })
                    .map(function (_a) {
                    var name = _a.name;
                    return ({
                        value: "uniq(" + name + ")",
                        label: "uniq(" + name + ")",
                    });
                });
            }
            if (input.startsWith('avg')) {
                optionList = _this.props.columns
                    .filter(function (_a) {
                    var type = _a.type;
                    return type === 'number';
                })
                    .map(function (_a) {
                    var name = _a.name;
                    return ({
                        value: "avg(" + name + ")",
                        label: "avg(" + name + ")",
                    });
                });
            }
            if (input.startsWith('sum')) {
                optionList = _this.props.columns
                    .filter(function (_a) {
                    var type = _a.type;
                    return type === 'number';
                })
                    .map(function (_a) {
                    var name = _a.name;
                    return ({
                        value: "sum(" + name + ")",
                        label: "sum(" + name + ")",
                    });
                });
            }
            return optionList.filter(function (_a) {
                var label = _a.label;
                return label.includes(input);
            });
        };
        _this.handleChange = function (option) {
            if (option.value === 'uniq' || option.value === 'avg' || option.value === 'sum') {
                _this.setState({ inputValue: option.value }, _this.focus);
            }
            else {
                _this.setState({ inputValue: option.value, isOpen: false });
                _this.props.onChange(getExternal(option.value));
            }
        };
        _this.handleOpen = function () {
            if (_this.state.inputValue === '') {
                _this.setState({
                    inputValue: getInternal(_this.props.value),
                    isOpen: true,
                });
            }
        };
        _this.inputRenderer = function (props) {
            var onChange = function (evt) {
                if (evt && evt.target && evt.target.value === '') {
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
            return (<input type="text" {...props} onChange={onChange} value={_this.state.inputValue} style={{ width: '100%', border: 0, backgroundColor: 'transparent' }}/>);
        };
        _this.valueComponent = function (props) {
            if (_this.state.isOpen) {
                return null;
            }
            return <Value {...props}/>;
        };
        _this.handleInputChange = function (value) {
            _this.setState({
                inputValue: value,
            });
        };
        return _this;
    }
    AggregationRow.prototype.getOptions = function () {
        var currentValue = getInternal(this.props.value);
        var shouldDisplayValue = currentValue || this.state.inputValue;
        return shouldDisplayValue ? [{ label: currentValue, value: currentValue }] : [];
    };
    AggregationRow.prototype.focus = function () {
        this.select.focus();
    };
    AggregationRow.prototype.render = function () {
        var _this = this;
        return (<div>
        <SelectControl deprecatedSelectControl ref={function (ref) { return (_this.select = ref); }} value={getInternal(this.props.value)} placeholder={<PlaceholderText>{t('Add aggregation function...')}</PlaceholderText>} options={this.getOptions()} filterOptions={this.filterOptions} onChange={this.handleChange} onOpen={this.handleOpen} closeOnSelect openOnFocus autoBlur clearable={false} backspaceRemoves={false} deleteRemoves={false} inputRenderer={this.inputRenderer} valueComponent={this.valueComponent} onInputChange={this.handleInputChange} disabled={this.props.disabled}/>
      </div>);
    };
    return AggregationRow;
}(React.Component));
export default AggregationRow;
//# sourceMappingURL=aggregation.jsx.map