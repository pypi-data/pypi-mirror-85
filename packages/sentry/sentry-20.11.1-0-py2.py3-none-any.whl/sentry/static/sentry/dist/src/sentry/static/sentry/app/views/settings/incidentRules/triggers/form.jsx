import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { fetchOrgMembers } from 'app/actionCreators/members';
import { t, tct } from 'app/locale';
import CircleIndicator from 'app/components/circleIndicator';
import Field from 'app/views/settings/components/forms/field';
import ThresholdControl from 'app/views/settings/incidentRules/triggers/thresholdControl';
import withApi from 'app/utils/withApi';
import withConfig from 'app/utils/withConfig';
import space from 'app/styles/space';
var TriggerForm = /** @class */ (function (_super) {
    __extends(TriggerForm, _super);
    function TriggerForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Handler for threshold changes coming from slider or chart.
         * Needs to sync state with the form.
         */
        _this.handleChangeThreshold = function (value) {
            var _a = _this.props, onChange = _a.onChange, trigger = _a.trigger;
            onChange(__assign(__assign({}, trigger), { alertThreshold: value.threshold }), { alertThreshold: value.threshold });
        };
        return _this;
    }
    TriggerForm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, error = _a.error, trigger = _a.trigger, isCritical = _a.isCritical, thresholdType = _a.thresholdType, fieldHelp = _a.fieldHelp, triggerLabel = _a.triggerLabel, placeholder = _a.placeholder, onThresholdTypeChange = _a.onThresholdTypeChange;
        return (<Field label={triggerLabel} help={fieldHelp} required={isCritical} error={error && error.alertThreshold}>
        <ThresholdControl disabled={disabled} disableThresholdType={!isCritical} type={trigger.label} thresholdType={thresholdType} threshold={trigger.alertThreshold} placeholder={placeholder} onChange={this.handleChangeThreshold} onThresholdTypeChange={onThresholdTypeChange}/>
      </Field>);
    };
    return TriggerForm;
}(React.PureComponent));
var TriggerFormContainer = /** @class */ (function (_super) {
    __extends(TriggerFormContainer, _super);
    function TriggerFormContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeTrigger = function (triggerIndex) { return function (trigger, changeObj) {
            var onChange = _this.props.onChange;
            onChange(triggerIndex, trigger, changeObj);
        }; };
        _this.handleChangeResolveTrigger = function (trigger, _) {
            var onResolveThresholdChange = _this.props.onResolveThresholdChange;
            onResolveThresholdChange(trigger.alertThreshold);
        };
        return _this;
    }
    TriggerFormContainer.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization;
        fetchOrgMembers(api, organization.slug);
    };
    TriggerFormContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, config = _a.config, disabled = _a.disabled, errors = _a.errors, organization = _a.organization, triggers = _a.triggers, thresholdType = _a.thresholdType, resolveThreshold = _a.resolveThreshold, projects = _a.projects, onThresholdTypeChange = _a.onThresholdTypeChange;
        var resolveTrigger = {
            label: 'resolve',
            alertThreshold: resolveThreshold,
            actions: [],
        };
        return (<React.Fragment>
        {triggers.map(function (trigger, index) {
            var isCritical = index === 0;
            // eslint-disable-next-line no-use-before-define
            var TriggerIndicator = isCritical ? CriticalIndicator : WarningIndicator;
            return (<TriggerForm key={index} api={api} config={config} disabled={disabled} error={errors && errors.get(index)} trigger={trigger} thresholdType={thresholdType} resolveThreshold={resolveThreshold} organization={organization} projects={projects} triggerIndex={index} isCritical={isCritical} fieldHelp={tct('The threshold that will activate the [severity] status.', {
                severity: isCritical ? t('critical') : t('warning'),
            })} triggerLabel={<React.Fragment>
                  <TriggerIndicator size={12}/>
                  {isCritical ? t('Critical Status') : t('Warning Status')}
                </React.Fragment>} placeholder={isCritical ? '300' : t('None')} onChange={_this.handleChangeTrigger(index)} onThresholdTypeChange={onThresholdTypeChange}/>);
        })}
        <TriggerForm api={api} config={config} disabled={disabled} error={errors && errors.get(2)} trigger={resolveTrigger} 
        // Flip rule thresholdType to opposite
        thresholdType={+!thresholdType} resolveThreshold={resolveThreshold} organization={organization} projects={projects} triggerIndex={2} isCritical={false} fieldHelp={t('The threshold that will activate the resolved status.')} triggerLabel={<React.Fragment>
              <ResolvedIndicator size={12}/>
              {t('Resolved Status')}
            </React.Fragment>} placeholder={t('Automatic')} onChange={this.handleChangeResolveTrigger} onThresholdTypeChange={onThresholdTypeChange}/>
      </React.Fragment>);
    };
    return TriggerFormContainer;
}(React.Component));
var CriticalIndicator = styled(CircleIndicator)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: ", ";\n  margin-right: ", ";\n"], ["\n  background: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.red300; }, space(1));
var WarningIndicator = styled(CircleIndicator)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  margin-right: ", ";\n"], ["\n  background: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.yellow300; }, space(1));
var ResolvedIndicator = styled(CircleIndicator)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n  margin-right: ", ";\n"], ["\n  background: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.green300; }, space(1));
export default withConfig(withApi(TriggerFormContainer));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=form.jsx.map