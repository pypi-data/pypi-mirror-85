import { __assign, __awaiter, __generator } from "tslib";
import React from 'react';
import sortBy from 'lodash/sortBy';
import { mountWithTheme } from 'sentry-test/enzyme';
import GlobalModal from 'app/components/globalModal';
import { openModal } from 'app/actionCreators/modal';
import Edit from 'app/views/settings/components/dataScrubbing/modals/edit';
import convertRelayPiiConfig from 'app/views/settings/components/dataScrubbing/convertRelayPiiConfig';
import { MethodType, RuleType } from 'app/views/settings/components/dataScrubbing/types';
import { getMethodLabel, getRuleLabel, valueSuggestions, } from 'app/views/settings/components/dataScrubbing/utils';
import submitRules from 'app/views/settings/components/dataScrubbing/submitRules';
// @ts-expect-error
var relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
var stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
var organizationSlug = 'sentry';
var convertedRules = convertRelayPiiConfig(stringRelayPiiConfig);
var rules = convertedRules;
var rule = rules[2];
var successfullySaved = jest.fn();
var projectId = 'foo';
var endpoint = "/projects/" + organizationSlug + "/" + projectId + "/";
// @ts-expect-error
var api = new MockApiClient();
jest.mock('app/views/settings/components/dataScrubbing/submitRules');
function renderComponent() {
    return __awaiter(this, void 0, void 0, function () {
        var wrapper;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    wrapper = mountWithTheme(<GlobalModal />);
                    openModal(function (modalProps) { return (<Edit {...modalProps} projectId={projectId} savedRules={rules} api={api} endpoint={endpoint} orgSlug={organizationSlug} onSubmitSuccess={successfullySaved} rule={rule}/>); });
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 1:
                    // @ts-expect-error
                    _a.sent();
                    wrapper.update();
                    return [2 /*return*/, wrapper];
            }
        });
    });
}
describe('Edit Modal', function () {
    it('open Edit Rule Modal', function () { return __awaiter(void 0, void 0, void 0, function () {
        var wrapper, fieldGroup, methodGroup, methodField, methodFieldHelp, methodFieldSelect, methodFieldSelectProps, methodFieldSelectOptions, placeholderField, placeholderFieldHelp, placeholderInput, typeGroup, typeField, typeFieldHelp, typeFieldSelect, typeFieldSelectProps, typeFieldSelectOptions, regexField, regexFieldHelp, regexFieldInput, sourceGroup, sourceField, sourceFieldHelp, sourceFieldInput, cancelButton;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, renderComponent()];
                case 1:
                    wrapper = _a.sent();
                    expect(wrapper.find('[data-test-id="modal-title"]').text()).toEqual('Edit an advanced data scrubbing rule');
                    fieldGroup = wrapper.find('FieldGroup');
                    expect(fieldGroup).toHaveLength(2);
                    methodGroup = fieldGroup.at(0).find('Field');
                    methodField = methodGroup.at(0);
                    expect(methodField.find('FieldLabel').text()).toEqual('Method');
                    methodFieldHelp = 'What to do';
                    expect(methodField.find('QuestionTooltip').prop('title')).toEqual(methodFieldHelp);
                    expect(methodField.find('Tooltip').prop('title')).toEqual(methodFieldHelp);
                    methodFieldSelect = methodField.find('SelectField');
                    expect(methodFieldSelect.exists()).toBe(true);
                    methodFieldSelectProps = methodFieldSelect.props();
                    expect(methodFieldSelectProps.value).toEqual(MethodType.REPLACE);
                    methodFieldSelectOptions = sortBy(Object.values(MethodType)).map(function (value) { return (__assign(__assign({}, getMethodLabel(value)), { value: value })); });
                    expect(methodFieldSelectProps.options).toEqual(methodFieldSelectOptions);
                    placeholderField = methodGroup.at(1);
                    expect(placeholderField.find('FieldLabel').text()).toEqual('Custom Placeholder (Optional)');
                    placeholderFieldHelp = 'It will replace the default placeholder [Filtered]';
                    expect(placeholderField.find('QuestionTooltip').prop('title')).toEqual(placeholderFieldHelp);
                    expect(placeholderField.find('Tooltip').prop('title')).toEqual(placeholderFieldHelp);
                    if (rule.method === MethodType.REPLACE) {
                        placeholderInput = placeholderField.find('input');
                        expect(placeholderInput.prop('value')).toEqual(rule.placeholder);
                    }
                    typeGroup = fieldGroup.at(1).find('Field');
                    typeField = typeGroup.at(0);
                    expect(typeField.find('FieldLabel').text()).toEqual('Data Type');
                    typeFieldHelp = 'What to look for. Use an existing pattern or define your own using regular expressions.';
                    expect(typeField.find('QuestionTooltip').prop('title')).toEqual(typeFieldHelp);
                    expect(typeField.find('Tooltip').prop('title')).toEqual(typeFieldHelp);
                    typeFieldSelect = typeField.find('SelectField');
                    expect(typeFieldSelect.exists()).toBe(true);
                    typeFieldSelectProps = typeFieldSelect.props();
                    expect(typeFieldSelectProps.value).toEqual(RuleType.PATTERN);
                    typeFieldSelectOptions = sortBy(Object.values(RuleType)).map(function (value) { return ({
                        label: getRuleLabel(value),
                        value: value,
                    }); });
                    expect(typeFieldSelectProps.options).toEqual(typeFieldSelectOptions);
                    regexField = typeGroup.at(1);
                    expect(regexField.find('FieldLabel').text()).toEqual('Regex matches');
                    regexFieldHelp = 'Custom regular expression (see documentation)';
                    expect(regexField.find('QuestionTooltip').prop('title')).toEqual(regexFieldHelp);
                    expect(regexField.find('Tooltip').prop('title')).toEqual(regexFieldHelp);
                    if (rule.type === RuleType.PATTERN) {
                        regexFieldInput = regexField.find('input');
                        expect(regexFieldInput.prop('value')).toEqual(rule.pattern);
                    }
                    // Event ID
                    expect(wrapper.find('Toggle').text()).toEqual('Use event ID for auto-completion');
                    sourceGroup = wrapper.find('SourceGroup');
                    expect(sourceGroup.exists()).toBe(true);
                    expect(sourceGroup.find('EventIdField')).toHaveLength(0);
                    sourceField = sourceGroup.find('Field');
                    expect(sourceField.find('FieldLabel').text()).toEqual('Source');
                    sourceFieldHelp = 'Where to look. In the simplest case this can be an attribute name.';
                    expect(sourceField.find('QuestionTooltip').prop('title')).toEqual(sourceFieldHelp);
                    expect(sourceField.find('Tooltip').prop('title')).toEqual(sourceFieldHelp);
                    sourceFieldInput = sourceField.find('input');
                    expect(sourceFieldInput.prop('value')).toEqual(rule.source);
                    cancelButton = wrapper.find('[aria-label="Cancel"]').hostNodes();
                    expect(cancelButton.exists()).toBe(true);
                    cancelButton.simulate('click');
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 2:
                    // @ts-expect-error
                    _a.sent();
                    wrapper.update();
                    expect(wrapper.find('[data-test-id="modal-title"]')).toHaveLength(0);
                    return [2 /*return*/];
            }
        });
    }); });
    it('edit Rule Modal', function () { return __awaiter(void 0, void 0, void 0, function () {
        var wrapper, methodField, methodFieldInput, methodFieldMenuOptions, maskOption, placeholderField, typeField, typeFieldInput, typeFieldMenuOptions, anythingOption, regexField, sourceField, sourceFieldInput, saveButton;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, renderComponent()];
                case 1:
                    wrapper = _a.sent();
                    methodField = wrapper.find('[data-test-id="method-field"]');
                    methodFieldInput = methodField.find('input').at(0);
                    methodFieldInput.simulate('keyDown', { key: 'ArrowDown' });
                    methodFieldMenuOptions = wrapper.find('[data-test-id="method-field"] MenuList Option Wrapper');
                    maskOption = methodFieldMenuOptions.at(1);
                    maskOption.simulate('click');
                    placeholderField = wrapper.find('[data-test-id="placeholder-field"]');
                    expect(placeholderField).toHaveLength(0);
                    typeField = wrapper.find('[data-test-id="type-field"]');
                    typeFieldInput = typeField.find('input').at(0);
                    typeFieldInput.simulate('keyDown', { key: 'ArrowDown' });
                    typeFieldMenuOptions = wrapper.find('[data-test-id="type-field"] MenuList Option Wrapper');
                    anythingOption = typeFieldMenuOptions.at(0);
                    anythingOption.simulate('click');
                    regexField = wrapper.find('[data-test-id="regex-field"]');
                    expect(regexField).toHaveLength(0);
                    sourceField = wrapper.find('[data-test-id="source-field"]');
                    sourceFieldInput = sourceField.find('input');
                    sourceFieldInput.simulate('change', { target: { value: valueSuggestions[2].value } });
                    saveButton = wrapper.find('[aria-label="Save Rule"]').hostNodes();
                    expect(saveButton.exists()).toBe(true);
                    saveButton.simulate('click');
                    expect(submitRules).toHaveBeenCalled();
                    expect(submitRules).toHaveBeenCalledWith(api, endpoint, [
                        {
                            id: 0,
                            method: 'replace',
                            type: 'password',
                            source: 'password',
                            placeholder: 'Scrubbed',
                        },
                        { id: 1, method: 'mask', type: 'creditcard', source: '$message' },
                        {
                            id: 2,
                            method: 'mask',
                            pattern: '',
                            placeholder: '',
                            type: 'anything',
                            source: '$error.value',
                        },
                    ]);
                    return [2 /*return*/];
            }
        });
    }); });
});
//# sourceMappingURL=editModal.spec.jsx.map