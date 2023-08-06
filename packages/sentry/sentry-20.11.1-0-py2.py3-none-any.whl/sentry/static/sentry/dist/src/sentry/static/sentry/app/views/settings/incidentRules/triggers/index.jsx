import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { removeAtArrayIndex } from 'app/utils/removeAtArrayIndex';
import { replaceAtArrayIndex } from 'app/utils/replaceAtArrayIndex';
import { t } from 'app/locale';
import TriggerForm from 'app/views/settings/incidentRules/triggers/form';
import withProjects from 'app/utils/withProjects';
import ActionsPanel from 'app/views/settings/incidentRules/triggers/actionsPanel';
/**
 * A list of forms to add, edit, and delete triggers.
 */
var Triggers = /** @class */ (function (_super) {
    __extends(Triggers, _super);
    function Triggers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteTrigger = function (index) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var updatedTriggers = removeAtArrayIndex(triggers, index);
            onChange(updatedTriggers);
        };
        _this.handleChangeTrigger = function (triggerIndex, trigger, changeObj) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var updatedTriggers = replaceAtArrayIndex(triggers, triggerIndex, trigger);
            onChange(updatedTriggers, triggerIndex, changeObj);
        };
        _this.handleAddAction = function (triggerIndex, action) {
            var _a = _this.props, onChange = _a.onChange, triggers = _a.triggers;
            var trigger = triggers[triggerIndex];
            var actions = __spread(trigger.actions, [action]);
            var updatedTriggers = replaceAtArrayIndex(triggers, triggerIndex, __assign(__assign({}, trigger), { actions: actions }));
            onChange(updatedTriggers, triggerIndex, { actions: actions });
        };
        _this.handleChangeActions = function (triggerIndex, triggers, actions) {
            var onChange = _this.props.onChange;
            var trigger = triggers[triggerIndex];
            var updatedTriggers = replaceAtArrayIndex(triggers, triggerIndex, __assign(__assign({}, trigger), { actions: actions }));
            onChange(updatedTriggers, triggerIndex, { actions: actions });
        };
        return _this;
    }
    Triggers.prototype.render = function () {
        var _a = this.props, availableActions = _a.availableActions, currentProject = _a.currentProject, errors = _a.errors, organization = _a.organization, projects = _a.projects, triggers = _a.triggers, disabled = _a.disabled, thresholdType = _a.thresholdType, resolveThreshold = _a.resolveThreshold, onThresholdTypeChange = _a.onThresholdTypeChange, onResolveThresholdChange = _a.onResolveThresholdChange;
        // Note we only support 2 triggers max
        return (<React.Fragment>
        <Panel>
          <PanelHeader>{t('Set A Threshold')}</PanelHeader>
          <PanelBody>
            <TriggerForm disabled={disabled} errors={errors} organization={organization} projects={projects} triggers={triggers} resolveThreshold={resolveThreshold} thresholdType={thresholdType} onChange={this.handleChangeTrigger} onThresholdTypeChange={onThresholdTypeChange} onResolveThresholdChange={onResolveThresholdChange}/>
          </PanelBody>
        </Panel>

        <ActionsPanel disabled={disabled} loading={availableActions === null} error={false} availableActions={availableActions} currentProject={currentProject} organization={organization} projects={projects} triggers={triggers} onChange={this.handleChangeActions} onAdd={this.handleAddAction}/>
      </React.Fragment>);
    };
    return Triggers;
}(React.Component));
export default withProjects(Triggers);
//# sourceMappingURL=index.jsx.map