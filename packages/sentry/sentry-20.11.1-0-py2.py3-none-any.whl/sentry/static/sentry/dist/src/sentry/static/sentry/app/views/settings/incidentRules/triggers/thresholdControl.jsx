import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { AlertRuleThresholdType, } from 'app/views/settings/incidentRules/types';
import { t, tct } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import NumberDragControl from 'app/components/numberDragControl';
import Tooltip from 'app/components/tooltip';
var ThresholdControl = /** @class */ (function (_super) {
    __extends(ThresholdControl, _super);
    function ThresholdControl() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            currentValue: null,
        };
        _this.handleThresholdChange = function (e) {
            var value = e.target.value;
            // Only allow number and partial number inputs
            if (!/^[0-9]*\.?[0-9]*$/.test(value)) {
                return;
            }
            var _a = _this.props, onChange = _a.onChange, thresholdType = _a.thresholdType;
            // Empty input
            if (value === '') {
                _this.setState({ currentValue: null });
                onChange({ thresholdType: thresholdType, threshold: '' }, e);
                return;
            }
            // Only call onChange if the new number is valid, and not partially typed
            // (eg writing out the decimal '5.')
            if (/\.+0*$/.test(value)) {
                _this.setState({ currentValue: value });
                return;
            }
            var numberValue = Number(value);
            _this.setState({ currentValue: null });
            onChange({ thresholdType: thresholdType, threshold: numberValue }, e);
        };
        /**
         * Coerce the currentValue to a number and trigger the onChange.
         */
        _this.handleThresholdBlur = function (e) {
            if (_this.state.currentValue === null) {
                return;
            }
            var _a = _this.props, onChange = _a.onChange, thresholdType = _a.thresholdType;
            onChange({ thresholdType: thresholdType, threshold: Number(_this.state.currentValue) }, e);
            _this.setState({ currentValue: null });
        };
        _this.handleTypeChange = function (_a, _) {
            var value = _a.value;
            var onThresholdTypeChange = _this.props.onThresholdTypeChange;
            onThresholdTypeChange(value);
        };
        _this.handleDragChange = function (delta, e) {
            var _a = _this.props, onChange = _a.onChange, thresholdType = _a.thresholdType, threshold = _a.threshold;
            var currentValue = threshold || 0;
            onChange({ thresholdType: thresholdType, threshold: currentValue + delta }, e);
        };
        return _this;
    }
    ThresholdControl.prototype.render = function () {
        var _a;
        var currentValue = this.state.currentValue;
        var _b = this.props, thresholdType = _b.thresholdType, threshold = _b.threshold, placeholder = _b.placeholder, type = _b.type, _ = _b.onChange, __ = _b.onThresholdTypeChange, disabled = _b.disabled, disableThresholdType = _b.disableThresholdType, props = __rest(_b, ["thresholdType", "threshold", "placeholder", "type", "onChange", "onThresholdTypeChange", "disabled", "disableThresholdType"]);
        return (<div {...props}>
        <SelectControl isDisabled={disabled || disableThresholdType} name={type + "ThresholdType"} value={thresholdType} options={[
            { value: AlertRuleThresholdType.BELOW, label: t('Below') },
            { value: AlertRuleThresholdType.ABOVE, label: t('Above') },
        ]} onChange={this.handleTypeChange}/>
        <Input disabled={disabled} name={type + "Threshold"} placeholder={placeholder} value={(_a = currentValue !== null && currentValue !== void 0 ? currentValue : threshold) !== null && _a !== void 0 ? _a : ''} onChange={this.handleThresholdChange} onBlur={this.handleThresholdBlur} 
        // Disable lastpass autocomplete
        data-lpignore="true"/>
        <DragContainer>
          <Tooltip title={tct('Drag to adjust threshold[break]You can hold shift to fine tune', {
            break: <br />,
        })}>
            <NumberDragControl step={5} axis="y" onChange={this.handleDragChange}/>
          </Tooltip>
        </DragContainer>
      </div>);
    };
    return ThresholdControl;
}(React.Component));
var DragContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: 6px;\n  right: 12px;\n"], ["\n  position: absolute;\n  top: 6px;\n  right: 12px;\n"])));
export default styled(ThresholdControl)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  display: grid;\n  align-items: center;\n  grid-template-columns: 1fr 3fr;\n  grid-gap: ", ";\n"], ["\n  position: relative;\n  display: grid;\n  align-items: center;\n  grid-template-columns: 1fr 3fr;\n  grid-gap: ", ";\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=thresholdControl.jsx.map