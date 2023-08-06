import { __assign, __awaiter, __generator } from "tslib";
import React from 'react';
import sortBy from 'lodash/sortBy';
import { mountWithTheme } from 'sentry-test/enzyme';
import GlobalModal from 'app/components/globalModal';
import { openModal } from 'app/actionCreators/modal';
import Add from 'app/views/settings/components/dataScrubbing/modals/add';
import convertRelayPiiConfig from 'app/views/settings/components/dataScrubbing/convertRelayPiiConfig';
import { MethodType, RuleType } from 'app/views/settings/components/dataScrubbing/types';
import { getMethodLabel, getRuleLabel, } from 'app/views/settings/components/dataScrubbing/utils';
// @ts-expect-error
var relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
var stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
var organizationSlug = 'sentry';
var convertedRules = convertRelayPiiConfig(stringRelayPiiConfig);
var rules = convertedRules;
var successfullySaved = jest.fn();
var projectId = 'foo';
var endpoint = "/projects/" + organizationSlug + "/" + projectId + "/";
// @ts-expect-error
var api = new MockApiClient();
function renderComponent() {
    return __awaiter(this, void 0, void 0, function () {
        var wrapper;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    wrapper = mountWithTheme(<GlobalModal />);
                    openModal(function (modalProps) { return (<Add {...modalProps} projectId={projectId} savedRules={rules} api={api} endpoint={endpoint} orgSlug={organizationSlug} onSubmitSuccess={successfullySaved}/>); });
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
describe('Add Modal', function () {
    it('open Add Rule Modal', function () { return __awaiter(void 0, void 0, void 0, function () {
        var wrapper, fieldGroup, methodGroup, methodFieldHelp, methodField, methodFieldProps, methodFieldOptions, typeGroup, typeFieldHelp, typeField, typeFieldProps, typeFieldOptions, sourceGroup, sourceField, sourceFieldHelp, cancelButton;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, renderComponent()];
                case 1:
                    wrapper = _a.sent();
                    expect(wrapper.find('[data-test-id="modal-title"]').text()).toEqual('Add an advanced data scrubbing rule');
                    fieldGroup = wrapper.find('FieldGroup');
                    expect(fieldGroup).toHaveLength(2);
                    methodGroup = fieldGroup.at(0).find('Field');
                    expect(methodGroup.find('FieldLabel').text()).toEqual('Method');
                    methodFieldHelp = 'What to do';
                    expect(methodGroup.find('QuestionTooltip').prop('title')).toEqual(methodFieldHelp);
                    expect(methodGroup.find('Tooltip').prop('title')).toEqual(methodFieldHelp);
                    methodField = methodGroup.find('SelectField');
                    expect(methodField.exists()).toBe(true);
                    methodFieldProps = methodField.props();
                    expect(methodFieldProps.value).toEqual(MethodType.MASK);
                    methodFieldOptions = sortBy(Object.values(MethodType)).map(function (value) { return (__assign(__assign({}, getMethodLabel(value)), { value: value })); });
                    expect(methodFieldProps.options).toEqual(methodFieldOptions);
                    typeGroup = fieldGroup.at(1).find('Field');
                    expect(typeGroup.find('FieldLabel').text()).toEqual('Data Type');
                    typeFieldHelp = 'What to look for. Use an existing pattern or define your own using regular expressions.';
                    expect(typeGroup.find('QuestionTooltip').prop('title')).toEqual(typeFieldHelp);
                    expect(typeGroup.find('Tooltip').prop('title')).toEqual(typeFieldHelp);
                    typeField = typeGroup.find('SelectField');
                    expect(typeField.exists()).toBe(true);
                    typeFieldProps = typeField.props();
                    expect(typeFieldProps.value).toEqual(RuleType.CREDITCARD);
                    typeFieldOptions = sortBy(Object.values(RuleType)).map(function (value) { return ({
                        label: getRuleLabel(value),
                        value: value,
                    }); });
                    expect(typeFieldProps.options).toEqual(typeFieldOptions);
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
    it('Display placeholder field', function () { return __awaiter(void 0, void 0, void 0, function () {
        var wrapper, fieldGroup, methodGroup, methodField, methodFieldInput, methodFieldMenuOptions, replaceOption, updatedMethodGroup, placeholderField, placeholderFieldHelp, hashOption;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, renderComponent()];
                case 1:
                    wrapper = _a.sent();
                    fieldGroup = wrapper.find('FieldGroup');
                    expect(fieldGroup).toHaveLength(2);
                    methodGroup = fieldGroup.at(0).find('Field');
                    expect(methodGroup).toHaveLength(1);
                    methodField = methodGroup.find('[data-test-id="method-field"]');
                    methodFieldInput = methodField.find('input').at(1);
                    methodFieldInput.simulate('keyDown', { key: 'ArrowDown' });
                    methodFieldMenuOptions = wrapper.find('[data-test-id="method-field"] MenuList Option Wrapper');
                    expect(methodFieldMenuOptions).toHaveLength(4);
                    replaceOption = methodFieldMenuOptions.at(3);
                    expect(replaceOption.find('[data-test-id="label"]').text()).toEqual('Replace');
                    expect(replaceOption.find('Description').text()).toEqual('(Replace with Placeholder)');
                    // After the click the placeholder field MUST be in the DOM
                    replaceOption.simulate('click');
                    wrapper.update();
                    expect(wrapper.find('[data-test-id="method-field"] input').at(1).prop('value')).toEqual(MethodType.REPLACE);
                    updatedMethodGroup = wrapper.find('FieldGroup').at(0).find('Field');
                    expect(updatedMethodGroup).toHaveLength(2);
                    placeholderField = updatedMethodGroup.at(1);
                    expect(placeholderField.find('FieldLabel').text()).toEqual('Custom Placeholder (Optional)');
                    placeholderFieldHelp = 'It will replace the default placeholder [Filtered]';
                    expect(placeholderField.find('QuestionTooltip').prop('title')).toEqual(placeholderFieldHelp);
                    expect(placeholderField.find('Tooltip').prop('title')).toEqual(placeholderFieldHelp);
                    // After the click, the placeholder field MUST NOT be in the DOM
                    wrapper
                        .find('[data-test-id="method-field"]')
                        .find('input')
                        .at(1)
                        .simulate('keyDown', { key: 'ArrowDown' });
                    hashOption = wrapper
                        .find('[data-test-id="method-field"] MenuList Option Wrapper')
                        .at(0);
                    hashOption.simulate('click');
                    expect(wrapper.find('[data-test-id="method-field"] input').at(1).prop('value')).toBe(MethodType.HASH);
                    expect(wrapper.find('FieldGroup').at(0).find('Field')).toHaveLength(1);
                    return [2 /*return*/];
            }
        });
    }); });
    it('Display regex field', function () { return __awaiter(void 0, void 0, void 0, function () {
        var wrapper, fieldGroup, typeGroup, typeField, typeFieldInput, typeFieldMenuOptions, regexOption, updatedTypeGroup, regexField, regexFieldHelp, creditCardOption;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, renderComponent()];
                case 1:
                    wrapper = _a.sent();
                    fieldGroup = wrapper.find('FieldGroup');
                    expect(fieldGroup).toHaveLength(2);
                    typeGroup = fieldGroup.at(1).find('Field');
                    expect(typeGroup).toHaveLength(1);
                    typeField = typeGroup.find('[data-test-id="type-field"]');
                    typeFieldInput = typeField.find('input').at(1);
                    typeFieldInput.simulate('keyDown', { key: 'ArrowDown' });
                    typeFieldMenuOptions = wrapper.find('[data-test-id="type-field"] MenuList Option Wrapper');
                    expect(typeFieldMenuOptions).toHaveLength(13);
                    regexOption = typeFieldMenuOptions.at(7);
                    expect(regexOption.find('[data-test-id="label"]').text()).toEqual('Regex matches');
                    // After the click, the regex matches field MUST be in the DOM
                    regexOption.simulate('click');
                    wrapper.update();
                    expect(wrapper.find('[data-test-id="type-field"] input').at(1).prop('value')).toEqual(RuleType.PATTERN);
                    updatedTypeGroup = wrapper.find('FieldGroup').at(1).find('Field');
                    expect(updatedTypeGroup).toHaveLength(2);
                    regexField = updatedTypeGroup.at(1);
                    expect(regexField.find('FieldLabel').text()).toEqual('Regex matches');
                    regexFieldHelp = 'Custom regular expression (see documentation)';
                    expect(regexField.find('QuestionTooltip').prop('title')).toEqual(regexFieldHelp);
                    expect(regexField.find('Tooltip').prop('title')).toEqual(regexFieldHelp);
                    // After the click, the regex matches field MUST NOT be in the DOM
                    wrapper
                        .find('[data-test-id="type-field"]')
                        .find('input')
                        .at(1)
                        .simulate('keyDown', { key: 'ArrowDown' });
                    creditCardOption = wrapper
                        .find('[data-test-id="type-field"] MenuList Option Wrapper')
                        .at(1);
                    creditCardOption.simulate('click');
                    expect(wrapper.find('[data-test-id="type-field"] input').at(1).prop('value')).toBe(RuleType.CREDITCARD);
                    expect(wrapper.find('FieldGroup').at(1).find('Field')).toHaveLength(1);
                    return [2 /*return*/];
            }
        });
    }); });
    it('Display Event Id', function () { return __awaiter(void 0, void 0, void 0, function () {
        var eventId, wrapper, eventIdToggle, eventIdFieldInput;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    eventId = '12345678901234567890123456789012';
                    // @ts-expect-error
                    MockApiClient.addMockResponse({
                        url: "/organizations/" + organizationSlug + "/data-scrubbing-selector-suggestions/",
                        body: {
                            suggestions: [
                                { type: 'value', examples: ['34359738368'], value: "extra.'system.cpu.memory'" },
                                { type: 'value', value: '$frame.abs_path' },
                            ],
                        },
                    });
                    return [4 /*yield*/, renderComponent()];
                case 1:
                    wrapper = _a.sent();
                    eventIdToggle = wrapper.find('Toggle');
                    eventIdToggle.simulate('click');
                    eventIdFieldInput = wrapper.find('[data-test-id="event-id-field"] input');
                    eventIdFieldInput.simulate('change', {
                        target: { value: eventId },
                    });
                    eventIdFieldInput.simulate('blur');
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 2:
                    // @ts-expect-error
                    _a.sent();
                    // Loading
                    expect(wrapper.find('[data-test-id="event-id-field"] FormSpinner')).toHaveLength(1);
                    wrapper.update();
                    // Fetched new suggestions successfully through the informed event ID
                    expect(wrapper.find('[data-test-id="event-id-field"] IconCheckmark')).toHaveLength(1);
                    return [2 /*return*/];
            }
        });
    }); });
});
//# sourceMappingURL=addModal.spec.jsx.map