import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import flatten from 'lodash/flatten';
import { defined, objectIsEmpty } from 'app/utils';
import { t } from 'app/locale';
import Button from 'app/components/button';
import Input from 'app/views/settings/components/forms/controls/input';
import InputField from 'app/views/settings/components/forms/inputField';
import space from 'app/styles/space';
import { IconAdd, IconDelete } from 'app/icons';
import Confirm from 'app/components/confirm';
import Alert from 'app/components/alert';
import { singleLineRenderer } from 'app/utils/marked';
var defaultProps = {
    /**
     * Text used for the 'add' button. An empty string can be used
     * to just render the "+" icon.
     */
    addButtonText: t('Add Item'),
    /**
     * Automatically save even if fields are empty
     */
    allowEmpty: false,
};
var TableField = /** @class */ (function (_super) {
    __extends(TableField, _super);
    function TableField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasValue = function (value) { return defined(value) && !objectIsEmpty(value); };
        _this.renderField = function (props) {
            var onChange = props.onChange, onBlur = props.onBlur, addButtonText = props.addButtonText, columnLabels = props.columnLabels, columnKeys = props.columnKeys, rawDisabled = props.disabled, allowEmpty = props.allowEmpty, confirmDeleteMessage = props.confirmDeleteMessage;
            var mappedKeys = columnKeys || [];
            var emptyValue = mappedKeys.reduce(function (a, v) {
                var _a;
                return (__assign(__assign({}, a), (_a = {}, _a[v] = null, _a)));
            }, { id: '' });
            var valueIsEmpty = _this.hasValue(props.value);
            var value = valueIsEmpty ? props.value : [];
            var saveChanges = function (nextValue) {
                onChange === null || onChange === void 0 ? void 0 : onChange(nextValue, []);
                //nextValue is an array of ObservableObjectAdministration objects
                var validValues = !flatten(Object.values(nextValue).map(Object.entries)).some(function (_a) {
                    var _b = __read(_a, 2), key = _b[0], val = _b[1];
                    return key !== 'id' && !val;
                } //don't allow empty values except if it's the ID field
                );
                if (allowEmpty || validValues) {
                    //TOOD: add debouncing or use a form save button
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur(nextValue, []);
                }
            };
            var addRow = function () {
                saveChanges(__spread(value, [emptyValue]));
            };
            var removeRow = function (rowIndex) {
                var newValue = __spread(value);
                newValue.splice(rowIndex, 1);
                saveChanges(newValue);
            };
            var setValue = function (rowIndex, fieldKey, fieldValue) {
                var newValue = __spread(value);
                newValue[rowIndex][fieldKey] = fieldValue.currentTarget
                    ? fieldValue.currentTarget.value
                    : null;
                saveChanges(newValue);
            };
            //should not be a function for this component
            var disabled = typeof rawDisabled === 'function' ? false : rawDisabled;
            var button = (<Button icon={<IconAdd size="xs" isCircled/>} onClick={addRow} size="xsmall" disabled={disabled}>
        {addButtonText}
      </Button>);
            // The field will be set to inline when there is no value set for the
            // field, just show the button.
            if (!valueIsEmpty) {
                return <div>{button}</div>;
            }
            var renderConfirmMessage = function () {
                return (<React.Fragment>
          <Alert type="error">
            <span dangerouslySetInnerHTML={{
                    __html: singleLineRenderer(confirmDeleteMessage || t('Are you sure you want to delete this item?')),
                }}/>
          </Alert>
        </React.Fragment>);
            };
            return (<React.Fragment>
        <HeaderContainer>
          {mappedKeys.map(function (fieldKey, i) { return (<Header key={fieldKey}>
              <HeaderLabel>{columnLabels === null || columnLabels === void 0 ? void 0 : columnLabels[fieldKey]}</HeaderLabel>
              {i === mappedKeys.length - 1 && button}
            </Header>); })}
        </HeaderContainer>
        {value.map(function (row, rowIndex) { return (<RowContainer data-test-id="field-row" key={rowIndex}>
            {mappedKeys.map(function (fieldKey, i) { return (<Row key={fieldKey}>
                <RowInput>
                  <Input onChange={function (v) { return setValue(rowIndex, fieldKey, v); }} value={!defined(row[fieldKey]) ? '' : row[fieldKey]}/>
                </RowInput>
                {i === mappedKeys.length - 1 && (<Confirm priority="danger" disabled={disabled} onConfirm={function () { return removeRow(rowIndex); }} message={renderConfirmMessage()}>
                    <RemoveButton>
                      <Button icon={<IconDelete />} size="small" disabled={disabled} label={t('delete')}/>
                    </RemoveButton>
                  </Confirm>)}
              </Row>); })}
          </RowContainer>); })}
      </React.Fragment>);
        };
        return _this;
    }
    TableField.prototype.render = function () {
        var _this = this;
        //We need formatMessageValue=false since we're saving an object
        // and there isn't a great way to render the
        // change within the toast. Just turn off displaying the from/to portion of
        // the message
        return (<InputField {...this.props} formatMessageValue={false} inline={function (_a) {
            var model = _a.model;
            return !_this.hasValue(model.getValue(_this.props.name));
        }} field={this.renderField}/>);
    };
    TableField.defaultProps = defaultProps;
    return TableField;
}(React.Component));
export default TableField;
var HeaderLabel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"], ["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var HeaderContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var Header = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"])));
var RowContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-top: ", ";\n"])), space(1));
var Row = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  margin-top: ", ";\n"])), space(1));
var RowInput = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n"])), space(1));
var RemoveButton = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=tableField.jsx.map