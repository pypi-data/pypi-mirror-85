import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
// eslint import checks can't find types in the flow code.
// eslint-disable-next-line import/named
import { components } from 'react-select';
import Input from 'app/views/settings/components/forms/controls/input';
import SelectControl from 'app/components/forms/selectControl';
import { t } from 'app/locale';
import Badge from 'app/components/badge';
import space from 'app/styles/space';
import { FieldValueKind } from './types';
var QueryField = /** @class */ (function (_super) {
    __extends(QueryField, _super);
    function QueryField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (_a) {
            var value = _a.value;
            var current = _this.props.fieldValue;
            var fieldValue = cloneDeep(_this.props.fieldValue);
            switch (value.kind) {
                case FieldValueKind.TAG:
                case FieldValueKind.MEASUREMENT:
                case FieldValueKind.FIELD:
                    fieldValue = { kind: 'field', field: value.meta.name };
                    break;
                case FieldValueKind.FUNCTION:
                    if (current.kind === 'field') {
                        fieldValue = { kind: 'function', function: [value.meta.name, '', undefined] };
                    }
                    else if (current.kind === 'function') {
                        fieldValue = {
                            kind: 'function',
                            function: [value.meta.name, current.function[1], current.function[2]],
                        };
                    }
                    break;
                default:
                    throw new Error('Invalid field type found in column picker');
            }
            if (value.kind === FieldValueKind.FUNCTION) {
                value.meta.parameters.forEach(function (param, i) {
                    if (fieldValue.kind !== 'function') {
                        return;
                    }
                    if (param.kind === 'column') {
                        var field = _this.getFieldOrTagOrMeasurementValue(fieldValue.function[i + 1]);
                        if (field === null) {
                            fieldValue.function[i + 1] = param.defaultValue || '';
                        }
                        else if ((field.kind === FieldValueKind.FIELD || field.kind === FieldValueKind.TAG) &&
                            validateColumnTypes(param.columnTypes, field)) {
                            // New function accepts current field.
                            fieldValue.function[i + 1] = field.meta.name;
                        }
                        else {
                            // field does not fit within new function requirements, use the default.
                            fieldValue.function[i + 1] = param.defaultValue || '';
                            fieldValue.function[i + 2] = undefined;
                        }
                    }
                    if (param.kind === 'value') {
                        fieldValue.function[i + 1] = param.defaultValue || '';
                    }
                });
                if (fieldValue.kind === 'function') {
                    if (value.meta.parameters.length === 0) {
                        fieldValue.function = [fieldValue.function[0], '', undefined];
                    }
                    else if (value.meta.parameters.length === 1) {
                        fieldValue.function[2] = undefined;
                    }
                }
            }
            _this.triggerChange(fieldValue);
        };
        _this.handleFieldParameterChange = function (_a) {
            var value = _a.value;
            var newColumn = cloneDeep(_this.props.fieldValue);
            if (newColumn.kind === 'function') {
                newColumn.function[1] = value.meta.name;
            }
            _this.triggerChange(newColumn);
        };
        _this.handleScalarParameterChange = function (value) {
            var newColumn = cloneDeep(_this.props.fieldValue);
            if (newColumn.kind === 'function') {
                newColumn.function[1] = value;
            }
            _this.triggerChange(newColumn);
        };
        _this.handleRefinementChange = function (value) {
            var newColumn = cloneDeep(_this.props.fieldValue);
            if (newColumn.kind === 'function') {
                newColumn.function[2] = value;
            }
            _this.triggerChange(newColumn);
        };
        return _this;
    }
    QueryField.prototype.triggerChange = function (fieldValue) {
        this.props.onChange(fieldValue);
    };
    QueryField.prototype.getFieldOrTagOrMeasurementValue = function (name) {
        var fieldOptions = this.props.fieldOptions;
        if (name === undefined) {
            return null;
        }
        var fieldName = "field:" + name;
        if (fieldOptions[fieldName]) {
            return fieldOptions[fieldName].value;
        }
        var measurementName = "measurement:" + name;
        if (fieldOptions[measurementName]) {
            return fieldOptions[measurementName].value;
        }
        var tagName = name.indexOf('tags[') === 0
            ? "tag:" + name.replace(/tags\[(.*?)\]/, '$1')
            : "tag:" + name;
        if (fieldOptions[tagName]) {
            return fieldOptions[tagName].value;
        }
        // Likely a tag that was deleted but left behind in a saved query
        // Cook up a tag option so select control works.
        if (name.length > 0) {
            return {
                kind: FieldValueKind.TAG,
                meta: {
                    name: name,
                    dataType: 'string',
                    unknown: true,
                },
            };
        }
        return null;
    };
    QueryField.prototype.getFieldData = function () {
        var _this = this;
        var field = null;
        var fieldValue = this.props.fieldValue;
        var fieldOptions = this.props.fieldOptions;
        if (fieldValue.kind === 'function') {
            var funcName = "function:" + fieldValue.function[0];
            if (fieldOptions[funcName] !== undefined) {
                field = fieldOptions[funcName].value;
            }
        }
        if (fieldValue.kind === 'field') {
            field = this.getFieldOrTagOrMeasurementValue(fieldValue.field);
            fieldOptions = this.appendFieldIfUnknown(fieldOptions, field);
        }
        var parameterDescriptions = [];
        // Generate options and values for each parameter.
        if (field &&
            field.kind === FieldValueKind.FUNCTION &&
            field.meta.parameters.length > 0 &&
            fieldValue.kind === FieldValueKind.FUNCTION) {
            parameterDescriptions = field.meta.parameters.map(function (param, index) {
                if (param.kind === 'column') {
                    var fieldParameter = _this.getFieldOrTagOrMeasurementValue(fieldValue.function[1]);
                    fieldOptions = _this.appendFieldIfUnknown(fieldOptions, fieldParameter);
                    return {
                        kind: 'column',
                        value: fieldParameter,
                        required: param.required,
                        options: Object.values(fieldOptions).filter(function (_a) {
                            var value = _a.value;
                            return (value.kind === FieldValueKind.FIELD ||
                                value.kind === FieldValueKind.TAG ||
                                value.kind === FieldValueKind.MEASUREMENT) &&
                                validateColumnTypes(param.columnTypes, value);
                        }),
                    };
                }
                return {
                    kind: 'value',
                    value: (fieldValue.kind === 'function' && fieldValue.function[index + 1]) ||
                        param.defaultValue ||
                        '',
                    dataType: param.dataType,
                    required: param.required,
                };
            });
        }
        return { field: field, fieldOptions: fieldOptions, parameterDescriptions: parameterDescriptions };
    };
    QueryField.prototype.appendFieldIfUnknown = function (fieldOptions, field) {
        if (!field) {
            return fieldOptions;
        }
        if (field && field.kind === FieldValueKind.TAG && field.meta.unknown) {
            // Clone the options so we don't mutate other rows.
            fieldOptions = Object.assign({}, fieldOptions);
            fieldOptions[field.meta.name] = { label: field.meta.name, value: field };
        }
        return fieldOptions;
    };
    QueryField.prototype.renderParameterInputs = function (parameters) {
        var _this = this;
        var inputs = parameters.map(function (descriptor, index) {
            if (descriptor.kind === 'column' && descriptor.options.length > 0) {
                return (<SelectControl key="select" name="parameter" placeholder={t('Select value')} options={descriptor.options} value={descriptor.value} required={descriptor.required} onChange={_this.handleFieldParameterChange}/>);
            }
            if (descriptor.kind === 'value') {
                var handler = index === 0 ? _this.handleScalarParameterChange : _this.handleRefinementChange;
                var inputProps = {
                    required: descriptor.required,
                    value: descriptor.value,
                    onUpdate: handler,
                };
                switch (descriptor.dataType) {
                    case 'number':
                        return (<BufferedInput name="refinement" key="parameter:number" type="text" inputMode="numeric" pattern="[0-9]*(\.[0-9]*)?" {...inputProps}/>);
                    case 'integer':
                        return (<BufferedInput name="refinement" key="parameter:integer" type="text" inputMode="numeric" pattern="[0-9]*" {...inputProps}/>);
                    default:
                        return (<BufferedInput name="refinement" key="parameter:text" type="text" {...inputProps}/>);
                }
            }
            throw new Error("Unknown parameter type encountered for " + _this.props.fieldValue);
        });
        // Add enough disabled inputs to fill the grid up.
        // We always have 1 input.
        var gridColumns = this.props.gridColumns;
        var requiredInputs = (gridColumns !== null && gridColumns !== void 0 ? gridColumns : inputs.length + 1) - inputs.length - 1;
        if (gridColumns !== undefined && requiredInputs > 0) {
            for (var i = 0; i < requiredInputs; i++) {
                inputs.push(<BlankSpace key={i}/>);
            }
        }
        return inputs;
    };
    QueryField.prototype.render = function () {
        var _a = this.props, className = _a.className, takeFocus = _a.takeFocus, filterPrimaryOptions = _a.filterPrimaryOptions;
        var _b = this.getFieldData(), field = _b.field, fieldOptions = _b.fieldOptions, parameterDescriptions = _b.parameterDescriptions;
        var allFieldOptions = filterPrimaryOptions
            ? Object.values(fieldOptions).filter(filterPrimaryOptions)
            : Object.values(fieldOptions);
        var selectProps = {
            name: 'field',
            options: Object.values(allFieldOptions),
            placeholder: t('(Required)'),
            value: field,
            onChange: this.handleFieldChange,
        };
        if (takeFocus && field === null) {
            selectProps.autoFocus = true;
        }
        var styles = {
            singleValue: function (provided) {
                var custom = {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: 'calc(100% - 10px)',
                };
                return __assign(__assign({}, provided), custom);
            },
            option: function (provided) {
                var custom = {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: '100%',
                };
                return __assign(__assign({}, provided), custom);
            },
        };
        var parameters = this.renderParameterInputs(parameterDescriptions);
        return (<Container className={className} gridColumns={parameters.length + 1}>
        <SelectControl {...selectProps} styles={styles} components={{
            Option: function (_a) {
                var label = _a.label, data = _a.data, props = __rest(_a, ["label", "data"]);
                return (<components.Option label={label} {...props}>
                <span data-test-id="label">{label}</span>
                {data.value.kind === FieldValueKind.TAG && <Badge text="tag"/>}
              </components.Option>);
            },
            SingleValue: function (_a) {
                var data = _a.data, props = __rest(_a, ["data"]);
                return (<components.SingleValue data={data} {...props}>
                <span data-test-id="label">{data.label}</span>
                {data.value.kind === FieldValueKind.TAG && <Badge text="tag"/>}
              </components.SingleValue>);
            },
        }}/>
        {parameters}
      </Container>);
    };
    return QueryField;
}(React.Component));
function validateColumnTypes(columnTypes, input) {
    if (typeof columnTypes === 'function') {
        return columnTypes({ name: input.meta.name, dataType: input.meta.dataType });
    }
    return columnTypes.includes(input.meta.dataType);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-column-gap: ", ";\n  align-items: center;\n\n  flex-grow: 1;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-column-gap: ", ";\n  align-items: center;\n\n  flex-grow: 1;\n"])), function (p) { return p.gridColumns; }, space(1));
/**
 * Because controlled inputs fire onChange on every key stroke,
 * we can't update the QueryField that often as it would re-render
 * the input elements causing focus to be lost.
 *
 * Using a buffered input lets us throttle rendering and enforce data
 * constraints better.
 */
var BufferedInput = /** @class */ (function (_super) {
    __extends(BufferedInput, _super);
    function BufferedInput(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            value: _this.props.value,
        };
        _this.handleBlur = function () {
            if (_this.isValid) {
                _this.props.onUpdate(_this.state.value);
            }
            else {
                _this.setState({ value: _this.props.value });
            }
        };
        _this.handleChange = function (event) {
            if (_this.isValid) {
                _this.setState({ value: event.target.value });
            }
        };
        _this.input = React.createRef();
        return _this;
    }
    Object.defineProperty(BufferedInput.prototype, "isValid", {
        get: function () {
            if (!this.input.current) {
                return true;
            }
            return this.input.current.validity.valid;
        },
        enumerable: false,
        configurable: true
    });
    BufferedInput.prototype.render = function () {
        var _a = this.props, _ = _a.onUpdate, props = __rest(_a, ["onUpdate"]);
        return (<StyledInput {...props} ref={this.input} className="form-control" value={this.state.value} onChange={this.handleChange} onBlur={this.handleBlur}/>);
    };
    return BufferedInput;
}(React.Component));
// Set a min-width to allow shrinkage in grid.
var StyledInput = styled(Input)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  /* Match the height of the select boxes */\n  height: 37px;\n  min-width: 50px;\n"], ["\n  /* Match the height of the select boxes */\n  height: 37px;\n  min-width: 50px;\n"])));
var BlankSpace = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* Match the height of the select boxes */\n  height: 37px;\n  min-width: 50px;\n  background: ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n\n  &:after {\n    content: '", "';\n    color: ", ";\n  }\n"], ["\n  /* Match the height of the select boxes */\n  height: 37px;\n  min-width: 50px;\n  background: ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n\n  &:after {\n    content: '", "';\n    color: ", ";\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, t('No parameter'), function (p) { return p.theme.gray300; });
export { QueryField };
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=queryField.jsx.map