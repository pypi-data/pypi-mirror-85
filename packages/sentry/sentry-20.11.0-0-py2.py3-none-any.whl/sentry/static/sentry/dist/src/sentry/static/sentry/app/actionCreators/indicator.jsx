import { __assign, __makeTemplateObject, __rest } from "tslib";
import * as Sentry from '@sentry/react';
import React from 'react';
import styled from '@emotion/styled';
import { DEFAULT_TOAST_DURATION } from 'app/constants';
import { t, tct } from 'app/locale';
import IndicatorActions from 'app/actions/indicatorActions';
import space from 'app/styles/space';
// Removes a single indicator
export function removeIndicator(indicator) {
    IndicatorActions.remove(indicator);
}
// Clears all indicators
export function clearIndicators() {
    IndicatorActions.clear();
}
// Note previous IndicatorStore.add behavior was to default to "loading" if no type was supplied
export function addMessage(msg, type, options) {
    if (options === void 0) { options = {}; }
    var optionsDuration = options.duration, append = options.append, rest = __rest(options, ["duration", "append"]);
    // XXX: Debug for https://sentry.io/organizations/sentry/issues/1595204979/
    if (
    // @ts-expect-error
    typeof (msg === null || msg === void 0 ? void 0 : msg.message) !== 'undefined' &&
        // @ts-expect-error
        typeof (msg === null || msg === void 0 ? void 0 : msg.code) !== 'undefined' &&
        // @ts-expect-error
        typeof (msg === null || msg === void 0 ? void 0 : msg.extra) !== 'undefined') {
        Sentry.captureException(new Error('Attempt to XHR response to Indicators'));
    }
    // use default only if undefined, as 0 is a valid duration
    var duration = typeof optionsDuration === 'undefined' ? DEFAULT_TOAST_DURATION : optionsDuration;
    var action = append ? 'append' : 'replace';
    // XXX: This differs from `IndicatorStore.add` since it won't return the indicator that is created
    // because we are firing an action. You can just add a new message and it will, by default,
    // replace active indicator
    IndicatorActions[action](msg, type, __assign(__assign({}, rest), { duration: duration }));
}
function addMessageWithType(type) {
    return function (msg, options) { return addMessage(msg, type, options); };
}
export function addLoadingMessage(msg, options) {
    if (msg === void 0) { msg = t('Saving changes...'); }
    return addMessageWithType('loading')(msg, options);
}
export function addErrorMessage(msg, options) {
    return addMessageWithType('error')(msg, options);
}
export function addSuccessMessage(msg, options) {
    return addMessageWithType('success')(msg, options);
}
var PRETTY_VALUES = new Map([
    ['', '<empty>'],
    [null, '<none>'],
    [undefined, '<unset>'],
    // if we don't cast as any, then typescript complains because booleans are not valid keys
    [true, 'enabled'],
    [false, 'disabled'],
]);
// Transform form values into a string
// Otherwise bool values will not get rendered and empty strings look like a bug
var prettyFormString = function (val, model, fieldName) {
    var descriptor = model.fieldDescriptor.get(fieldName);
    if (descriptor && typeof descriptor.formatMessageValue === 'function') {
        var initialData = model.initialData;
        // XXX(epurkhsier): We pass the "props" as the descriptor and initialData.
        // This isn't necessarily all of the props of the form field, but should
        // make up a good portion needed for formatting.
        return descriptor.formatMessageValue(val, __assign(__assign({}, descriptor), { initialData: initialData }));
    }
    if (PRETTY_VALUES.has(val)) {
        return PRETTY_VALUES.get(val);
    }
    return "" + val;
};
/**
 * This will call an action creator to generate a "Toast" message that
 * notifies user the field that changed with its previous and current values.
 *
 * Also allows for undo
 */
export function saveOnBlurUndoMessage(change, model, fieldName) {
    if (!model) {
        return;
    }
    var label = model.getDescriptor(fieldName, 'label');
    if (!label) {
        return;
    }
    var prettifyValue = function (val) { return prettyFormString(val, model, fieldName); };
    // Hide the change text when formatMessageValue is explicitly set to false
    var showChangeText = model.getDescriptor(fieldName, 'formatMessageValue') !== false;
    addSuccessMessage(tct(showChangeText
        ? 'Changed [fieldName] from [oldValue] to [newValue]'
        : 'Changed [fieldName]', {
        root: <MessageContainer />,
        fieldName: <FieldName>{label}</FieldName>,
        oldValue: <FormValue>{prettifyValue(change.old)}</FormValue>,
        newValue: <FormValue>{prettifyValue(change.new)}</FormValue>,
    }), {
        modelArg: {
            model: model,
            id: fieldName,
            undo: function () {
                if (!model || !fieldName) {
                    return;
                }
                var oldValue = model.getValue(fieldName);
                var didUndo = model.undo();
                var newValue = model.getValue(fieldName);
                if (!didUndo) {
                    return;
                }
                if (!label) {
                    return;
                }
                // `saveField` can return null if it can't save
                var saveResult = model.saveField(fieldName, newValue);
                if (!saveResult) {
                    addErrorMessage(tct(showChangeText
                        ? 'Unable to restore [fieldName] from [oldValue] to [newValue]'
                        : 'Unable to restore [fieldName]', {
                        root: <MessageContainer />,
                        fieldName: <FieldName>{label}</FieldName>,
                        oldValue: <FormValue>{prettifyValue(oldValue)}</FormValue>,
                        newValue: <FormValue>{prettifyValue(newValue)}</FormValue>,
                    }));
                    return;
                }
                saveResult.then(function () {
                    addMessage(tct(showChangeText
                        ? 'Restored [fieldName] from [oldValue] to [newValue]'
                        : 'Restored [fieldName]', {
                        root: <MessageContainer />,
                        fieldName: <FieldName>{label}</FieldName>,
                        oldValue: <FormValue>{prettifyValue(oldValue)}</FormValue>,
                        newValue: <FormValue>{prettifyValue(newValue)}</FormValue>,
                    }), 'undo', {
                        duration: DEFAULT_TOAST_DURATION,
                    });
                });
            },
        },
    });
}
var FormValue = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-style: italic;\n  margin: 0 ", ";\n"], ["\n  font-style: italic;\n  margin: 0 ", ";\n"])), space(0.5));
var FieldName = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: bold;\n  margin: 0 ", ";\n"], ["\n  font-weight: bold;\n  margin: 0 ", ";\n"])), space(0.5));
var MessageContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=indicator.jsx.map