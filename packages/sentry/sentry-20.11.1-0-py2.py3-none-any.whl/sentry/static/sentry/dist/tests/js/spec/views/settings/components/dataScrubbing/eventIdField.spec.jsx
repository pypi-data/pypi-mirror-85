import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import EventIdField from 'app/views/settings/components/dataScrubbing/modals/form/eventIdField';
import { EventIdStatus } from 'app/views/settings/components/dataScrubbing/types';
import theme from 'app/utils/theme';
var handleUpdateEventId = jest.fn();
var eventIdValue = '887ab369df634e74aea708bcafe1a175';
function renderComponent(_a) {
    var _b = _a.value, value = _b === void 0 ? eventIdValue : _b, status = _a.status;
    return mountWithTheme(<EventIdField onUpdateEventId={handleUpdateEventId} eventId={{ value: value, status: status }}/>);
}
describe('EventIdField', function () {
    it('default render', function () {
        var wrapper = renderComponent({ value: '', status: EventIdStatus.UNDEFINED });
        var eventIdField = wrapper.find('Field');
        expect(eventIdField.exists()).toBe(true);
        expect(eventIdField.find('FieldLabel').text()).toEqual('Event ID (Optional)');
        var eventIdFieldHelp = 'Providing an event ID will automatically provide you a list of suggested sources';
        expect(eventIdField.find('QuestionTooltip').prop('title')).toEqual(eventIdFieldHelp);
        expect(eventIdField.find('Tooltip').prop('title')).toEqual(eventIdFieldHelp);
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual('');
        expect(eventIdFieldInput.prop('placeholder')).toEqual('XXXXXXXXXXXXXX');
        eventIdFieldInput.simulate('change', {
            target: { value: '887ab369df634e74aea708bcafe1a175' },
        });
        eventIdFieldInput.simulate('blur');
        expect(handleUpdateEventId).toHaveBeenCalled();
    });
    it('LOADING status', function () {
        var wrapper = renderComponent({ status: EventIdStatus.LOADING });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(0);
        expect(eventIdField.find('CloseIcon')).toHaveLength(0);
        expect(eventIdField.find('FormSpinner')).toHaveLength(1);
    });
    it('LOADED status', function () {
        var wrapper = renderComponent({ status: EventIdStatus.LOADED });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(0);
        expect(eventIdField.find('CloseIcon')).toHaveLength(0);
        var iconCheckmark = eventIdField.find('IconCheckmark');
        expect(iconCheckmark).toHaveLength(1);
        var iconCheckmarkColor = iconCheckmark.prop('color');
        expect(theme[iconCheckmarkColor]).toBe(theme.green300);
    });
    it('ERROR status', function () {
        var wrapper = renderComponent({ status: EventIdStatus.ERROR });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        var closeIcon = eventIdField.find('CloseIcon');
        expect(closeIcon).toHaveLength(1);
        expect(closeIcon.find('Tooltip').prop('title')).toEqual('Clear event ID');
        var fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('An error occurred while fetching the suggestions based on this event ID.');
    });
    it('INVALID status', function () {
        var wrapper = renderComponent({ status: EventIdStatus.INVALID });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        expect(eventIdField.find('CloseIcon')).toHaveLength(1);
        var fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('This event ID is invalid.');
    });
    it('NOTFOUND status', function () {
        var wrapper = renderComponent({ status: EventIdStatus.NOT_FOUND });
        var eventIdField = wrapper.find('Field');
        var eventIdFieldInput = eventIdField.find('input');
        expect(eventIdFieldInput.prop('value')).toEqual(eventIdValue);
        expect(eventIdField.find('FieldError')).toHaveLength(1);
        expect(eventIdField.find('CloseIcon')).toHaveLength(1);
        var fieldErrorReason = eventIdField.find('FieldErrorReason');
        expect(fieldErrorReason).toHaveLength(1);
        expect(fieldErrorReason.text()).toEqual('The chosen event ID was not found in projects you have access to.');
    });
});
//# sourceMappingURL=eventIdField.spec.jsx.map