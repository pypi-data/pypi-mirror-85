import { __assign, __decorate, __read, __rest } from "tslib";
import { observable, computed, action } from 'mobx';
import isEqual from 'lodash/isEqual';
import { Client } from 'app/api';
import { addErrorMessage, saveOnBlurUndoMessage } from 'app/actionCreators/indicator';
import { defined } from 'app/utils';
import { t } from 'app/locale';
import FormState from 'app/components/forms/state';
var FormModel = /** @class */ (function () {
    function FormModel(_a) {
        if (_a === void 0) { _a = {}; }
        var initialData = _a.initialData, options = __rest(_a, ["initialData"]);
        /**
         * Map of field name -> value
         */
        this.fields = observable.map();
        /**
         * Errors for individual fields
         * Note we don't keep error in `this.fieldState` so that we can easily
         * See if the form is in an "error" state with the `isError` getter
         */
        this.errors = new Map();
        /**
         * State of individual fields
         *
         * Map of field name -> object
         */
        this.fieldState = new Map();
        /**
         * Holds field properties as declared in <Form>
         * Does not need to be observable since these props should never change
         */
        this.fieldDescriptor = new Map();
        /**
         * Holds a list of `fields` states
         */
        this.snapshots = [];
        /**
         * POJO of field name -> value
         * It holds field values "since last save"
         */
        this.initialData = {};
        this.options = options || {};
        if (initialData) {
            this.setInitialData(initialData);
        }
        this.api = new Client();
    }
    /**
     * Reset state of model
     */
    FormModel.prototype.reset = function () {
        this.api.clear();
        this.fieldDescriptor.clear();
        this.resetForm();
    };
    FormModel.prototype.resetForm = function () {
        this.fields.clear();
        this.errors.clear();
        this.fieldState.clear();
        this.snapshots = [];
        this.initialData = {};
    };
    Object.defineProperty(FormModel.prototype, "formChanged", {
        /**
         * Deep equality comparison between last saved state and current fields state
         */
        get: function () {
            return !isEqual(this.initialData, this.fields.toJSON());
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(FormModel.prototype, "formData", {
        get: function () {
            return this.fields;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(FormModel.prototype, "isSaving", {
        /** Is form saving */
        get: function () {
            return this.formState === FormState.SAVING;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(FormModel.prototype, "isError", {
        /** Does form have any errors */
        get: function () {
            return !!this.errors.size;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Sets initial form data
     *
     * Also resets snapshots
     */
    FormModel.prototype.setInitialData = function (initialData) {
        this.fields.replace(initialData || {});
        this.initialData = this.fields.toJSON() || {};
        this.snapshots = [new Map(this.fields.entries())];
    };
    /**
     * Set form options
     */
    FormModel.prototype.setFormOptions = function (options) {
        this.options = options || {};
    };
    /**
     * Set field properties
     */
    FormModel.prototype.setFieldDescriptor = function (id, props) {
        //TODO(TS): add type to props
        this.fieldDescriptor.set(id, props);
        // Set default value iff initialData for field is undefined
        // This must take place before checking for `props.setValue` so that it can
        // be applied to `defaultValue`
        if (typeof props.defaultValue !== 'undefined' &&
            typeof this.initialData[id] === 'undefined') {
            this.initialData[id] =
                typeof props.defaultValue === 'function'
                    ? props.defaultValue()
                    : props.defaultValue;
            this.fields.set(id, this.initialData[id]);
        }
        if (typeof props.setValue === 'function') {
            this.initialData[id] = props.setValue(this.initialData[id], props);
            this.fields.set(id, this.initialData[id]);
        }
    };
    /**
     * Remove a field from the descriptor map and errors.
     */
    FormModel.prototype.removeField = function (id) {
        this.fieldDescriptor.delete(id);
        this.errors.delete(id);
    };
    /**
     * Creates a cloned Map of `this.fields` and returns a closure that when called
     * will save Map to `snapshots
     */
    FormModel.prototype.createSnapshot = function () {
        var _this = this;
        var snapshot = new Map(this.fields.entries());
        return function () { return _this.snapshots.unshift(snapshot); };
    };
    FormModel.prototype.getDescriptor = function (id, key) {
        // Needs to call `has` or else component will not be reactive if `id` doesn't exist in observable map
        var descriptor = this.fieldDescriptor.has(id) && this.fieldDescriptor.get(id);
        if (!descriptor) {
            return null;
        }
        return descriptor[key];
    };
    FormModel.prototype.getFieldState = function (id, key) {
        // Needs to call `has` or else component will not be reactive if `id` doesn't exist in observable map
        var fieldState = this.fieldState.has(id) && this.fieldState.get(id);
        if (!fieldState) {
            return null;
        }
        return fieldState[key];
    };
    FormModel.prototype.getValue = function (id) {
        if (!this.fields.has(id)) {
            return '';
        }
        return this.fields.get(id);
    };
    FormModel.prototype.getTransformedValue = function (id) {
        var fieldDescriptor = this.fieldDescriptor.get(id);
        var transformer = fieldDescriptor && typeof fieldDescriptor.getValue === 'function'
            ? fieldDescriptor.getValue
            : null;
        var value = this.getValue(id);
        return transformer ? transformer(value) : value;
    };
    /**
     * Data represented in UI
     */
    FormModel.prototype.getData = function () {
        return this.fields.toJSON();
    };
    /**
     * Form data that will be sent to API endpoint (i.e. after transforms)
     */
    FormModel.prototype.getTransformedData = function () {
        var _this = this;
        var form = this.getData();
        return Object.keys(form)
            .map(function (id) { return [id, _this.getTransformedValue(id)]; })
            .reduce(function (acc, _a) {
            var _b = __read(_a, 2), id = _b[0], value = _b[1];
            acc[id] = value;
            return acc;
        }, {});
    };
    FormModel.prototype.getError = function (id) {
        return this.errors.has(id) && this.errors.get(id);
    };
    // Returns true if not required or is required and is not empty
    FormModel.prototype.isValidRequiredField = function (id) {
        // Check field descriptor to see if field is required
        var isRequired = this.getDescriptor(id, 'required');
        var value = this.getValue(id);
        return !isRequired || (value !== '' && defined(value));
    };
    FormModel.prototype.isValidField = function (id) {
        return (this.getError(id) || []).length === 0;
    };
    FormModel.prototype.doApiRequest = function (_a) {
        var _this = this;
        var apiEndpoint = _a.apiEndpoint, apiMethod = _a.apiMethod, data = _a.data;
        var endpoint = apiEndpoint || this.options.apiEndpoint || '';
        var method = apiMethod || this.options.apiMethod;
        return new Promise(function (resolve, reject) {
            return _this.api.request(endpoint, {
                method: method,
                data: data,
                success: function (response) { return resolve(response); },
                error: function (error) { return reject(error); },
            });
        });
    };
    /**
     * Set the value of the form field
     * if quiet is true, we skip callbacks, validations
     */
    FormModel.prototype.setValue = function (id, value, _a) {
        var quiet = (_a === void 0 ? {} : _a).quiet;
        var fieldDescriptor = this.fieldDescriptor.get(id);
        var finalValue = value;
        if (fieldDescriptor && typeof fieldDescriptor.transformInput === 'function') {
            finalValue = fieldDescriptor.transformInput(value);
        }
        this.fields.set(id, finalValue);
        if (quiet) {
            return;
        }
        if (this.options.onFieldChange) {
            this.options.onFieldChange(id, finalValue);
        }
        this.validateField(id);
        this.updateShowSaveState(id, finalValue);
        this.updateShowReturnButtonState(id, finalValue);
    };
    FormModel.prototype.validateField = function (id) {
        var _this = this;
        var validate = this.getDescriptor(id, 'validate');
        var errors = [];
        if (typeof validate === 'function') {
            // Returns "tuples" of [id, error string]
            errors = validate({ model: this, id: id, form: this.getData() }) || [];
        }
        var fieldIsRequiredMessage = t('Field is required');
        if (!this.isValidRequiredField(id)) {
            errors.push([id, fieldIsRequiredMessage]);
        }
        // If we have no errors, ensure we clear the field
        errors = errors.length === 0 ? [[id, null]] : errors;
        errors.forEach(function (_a) {
            var _b = __read(_a, 2), field = _b[0], errorMessage = _b[1];
            return _this.setError(field, errorMessage);
        });
        return undefined;
    };
    FormModel.prototype.updateShowSaveState = function (id, value) {
        var isValueChanged = value !== this.initialData[id];
        // Update field state to "show save" if save on blur is disabled for this field
        // (only if contents of field differs from initial value)
        var saveOnBlurFieldOverride = this.getDescriptor(id, 'saveOnBlur');
        if (typeof saveOnBlurFieldOverride === 'undefined' || saveOnBlurFieldOverride) {
            return;
        }
        if (this.getFieldState(id, 'showSave') === isValueChanged) {
            return;
        }
        this.setFieldState(id, 'showSave', isValueChanged);
    };
    FormModel.prototype.updateShowReturnButtonState = function (id, value) {
        var isValueChanged = value !== this.initialData[id];
        var shouldShowReturnButton = this.getDescriptor(id, 'showReturnButton');
        if (!shouldShowReturnButton) {
            return;
        }
        // Only update state if state has changed
        if (this.getFieldState(id, 'showReturnButton') === isValueChanged) {
            return;
        }
        this.setFieldState(id, 'showReturnButton', isValueChanged);
    };
    /**
     * Changes form values to previous saved state
     */
    FormModel.prototype.undo = function () {
        // Always have initial data snapshot
        if (this.snapshots.length < 2) {
            return null;
        }
        this.snapshots.shift();
        this.fields.replace(this.snapshots[0]);
        return true;
    };
    /**
     * Attempts to save entire form to server and saves a snapshot for undos
     */
    FormModel.prototype.saveForm = function () {
        var _this = this;
        if (!this.validateForm()) {
            return null;
        }
        var saveSnapshot = this.createSnapshot();
        var request = this.doApiRequest({
            data: this.getTransformedData(),
        });
        this.setFormSaving();
        request
            .then(function (resp) {
            // save snapshot
            if (saveSnapshot) {
                saveSnapshot();
                saveSnapshot = null;
            }
            if (_this.options.onSubmitSuccess) {
                _this.options.onSubmitSuccess(resp, _this);
            }
        })
            .catch(function (resp) {
            // should we revert field value to last known state?
            saveSnapshot = null;
            if (_this.options.resetOnError) {
                _this.setInitialData({});
            }
            _this.submitError(resp);
            if (_this.options.onSubmitError) {
                _this.options.onSubmitError(resp, _this);
            }
        });
        return request;
    };
    /**
     * Attempts to save field and show undo message if necessary.
     * Calls submit handlers.
     * TODO(billy): This should return a promise that resolves (instead of null)
     */
    FormModel.prototype.saveField = function (id, currentValue) {
        var _this = this;
        var oldValue = this.initialData[id];
        var savePromise = this.saveFieldRequest(id, currentValue);
        if (!savePromise) {
            return null;
        }
        return savePromise
            .then(function (resp) {
            var newValue = _this.getValue(id);
            var change = { old: oldValue, new: newValue };
            // Only use `allowUndo` option if explicitly defined
            if (typeof _this.options.allowUndo === 'undefined' || _this.options.allowUndo) {
                saveOnBlurUndoMessage(change, _this, id);
            }
            if (_this.options.onSubmitSuccess) {
                _this.options.onSubmitSuccess(resp, _this, id, change);
            }
            return resp;
        })
            .catch(function (error) {
            if (_this.options.onSubmitError) {
                _this.options.onSubmitError(error, _this, id);
            }
            return {};
        });
    };
    /**
     * Saves a field with new value
     *
     * If field has changes, field does not have errors, then it will:
     * Save a snapshot, apply any data transforms, perform api request.
     *
     * If successful then: 1) reset save state, 2) update `initialData`, 3) save snapshot
     * If failed then: 1) reset save state, 2) add error state
     */
    FormModel.prototype.saveFieldRequest = function (id, currentValue) {
        var _a;
        var _this = this;
        var initialValue = this.initialData[id];
        // Don't save if field hasn't changed
        // Don't need to check for error state since initialData wouldn't have updated since last error
        if (currentValue === initialValue ||
            (currentValue === '' && !defined(initialValue))) {
            return null;
        }
        // Check for error first
        this.validateField(id);
        if (!this.isValidField(id)) {
            return null;
        }
        // shallow clone fields
        var saveSnapshot = this.createSnapshot();
        // Save field + value
        this.setSaving(id, true);
        var fieldDescriptor = this.fieldDescriptor.get(id);
        // Check if field needs to handle transforming request object
        var getData = typeof fieldDescriptor.getData === 'function' ? fieldDescriptor.getData : function (a) { return a; };
        var request = this.doApiRequest({
            data: getData((_a = {}, _a[id] = this.getTransformedValue(id), _a), { model: this, id: id, form: this.getData() }),
        });
        request
            .then(function (data) {
            _this.setSaving(id, false);
            // save snapshot
            if (saveSnapshot) {
                saveSnapshot();
                saveSnapshot = null;
            }
            // Update initialData after successfully saving a field as it will now be the baseline value
            _this.initialData[id] = _this.getValue(id);
            return data;
        })
            .catch(function (resp) {
            // should we revert field value to last known state?
            saveSnapshot = null;
            // Field can be configured to reset on error
            // e.g. BooleanFields
            var shouldReset = _this.getDescriptor(id, 'resetOnError');
            if (shouldReset) {
                _this.setValue(id, initialValue);
            }
            // API can return a JSON object with either:
            // 1) map of {[fieldName] => Array<ErrorMessages>}
            // 2) {'non_field_errors' => Array<ErrorMessages>}
            if (resp && resp.responseJSON) {
                //non-field errors can be camelcase or snake case
                var nonFieldErrors = resp.responseJSON.non_field_errors || resp.responseJSON.nonFieldErrors;
                // Show resp msg from API endpoint if possible
                if (Array.isArray(resp.responseJSON[id]) && resp.responseJSON[id].length) {
                    // Just take first resp for now
                    _this.setError(id, resp.responseJSON[id][0]);
                }
                else if (Array.isArray(nonFieldErrors) && nonFieldErrors.length) {
                    addErrorMessage(nonFieldErrors[0], { duration: 10000 });
                    // Reset saving state
                    _this.setError(id, '');
                }
                else {
                    _this.setError(id, 'Failed to save');
                }
            }
            else {
                // Default error behavior
                _this.setError(id, 'Failed to save');
            }
            // eslint-disable-next-line no-console
            console.error('Error saving form field', resp && resp.responseJSON);
        });
        return request;
    };
    /**
     * This is called when a field is blurred
     *
     * If `saveOnBlur` is set then call `saveField` and handle form callbacks accordingly
     */
    FormModel.prototype.handleBlurField = function (id, currentValue) {
        // Nothing to do if `saveOnBlur` is not on
        if (!this.options.saveOnBlur) {
            return null;
        }
        // Fields can individually set `saveOnBlur` to `false` (note this is ignored when `undefined`)
        var saveOnBlurFieldOverride = this.getDescriptor(id, 'saveOnBlur');
        if (typeof saveOnBlurFieldOverride !== 'undefined' && !saveOnBlurFieldOverride) {
            return null;
        }
        return this.saveField(id, currentValue);
    };
    FormModel.prototype.setFormSaving = function () {
        this.formState = FormState.SAVING;
    };
    /**
     * This is called when a field does not saveOnBlur and has an individual "Save" button
     */
    FormModel.prototype.handleSaveField = function (id, currentValue) {
        var _this = this;
        var savePromise = this.saveField(id, currentValue);
        if (!savePromise) {
            return null;
        }
        return savePromise.then(function () {
            _this.setFieldState(id, 'showSave', false);
        });
    };
    /**
     * Cancel "Save Field" state and revert form value back to initial value
     */
    FormModel.prototype.handleCancelSaveField = function (id) {
        this.setValue(id, this.initialData[id]);
        this.setFieldState(id, 'showSave', false);
    };
    FormModel.prototype.setFieldState = function (id, key, value) {
        var _a;
        var state = __assign(__assign({}, (this.fieldState.get(id) || {})), (_a = {}, _a[key] = value, _a));
        this.fieldState.set(id, state);
    };
    /**
     * Set "saving" state for field
     */
    FormModel.prototype.setSaving = function (id, value) {
        // When saving, reset error state
        this.setError(id, false);
        this.setFieldState(id, FormState.SAVING, value);
        this.setFieldState(id, FormState.READY, !value);
    };
    /**
     * Set "error" state for field
     */
    FormModel.prototype.setError = function (id, error) {
        // Note we don't keep error in `this.fieldState` so that we can easily
        // See if the form is in an "error" state with the `isError` getter
        if (!!error) {
            this.formState = FormState.ERROR;
            this.errors.set(id, error);
        }
        else {
            this.formState = FormState.READY;
            this.errors.delete(id);
        }
        // Field should no longer to "saving", but is not necessarily "ready"
        this.setFieldState(id, FormState.SAVING, false);
    };
    /**
     * Returns true if there are no errors
     */
    FormModel.prototype.validateForm = function () {
        var _this = this;
        Array.from(this.fieldDescriptor.keys()).forEach(function (id) { return !_this.validateField(id); });
        return !this.isError;
    };
    FormModel.prototype.handleErrorResponse = function (_a) {
        var _this = this;
        var resp = (_a === void 0 ? {} : _a).responseJSON;
        if (!resp) {
            return;
        }
        // Show resp msg from API endpoint if possible
        Object.keys(resp).forEach(function (id) {
            //non-field errors can be camelcase or snake case
            var nonFieldErrors = resp.non_field_errors || resp.nonFieldErrors;
            if ((id === 'non_field_errors' || id === 'nonFieldErrors') &&
                Array.isArray(nonFieldErrors) &&
                nonFieldErrors.length) {
                addErrorMessage(nonFieldErrors[0], { duration: 10000 });
            }
            else if (Array.isArray(resp[id]) && resp[id].length) {
                // Just take first resp for now
                _this.setError(id, resp[id][0]);
            }
        });
    };
    FormModel.prototype.submitSuccess = function (data) {
        // update initial data
        this.formState = FormState.READY;
        this.initialData = data;
    };
    FormModel.prototype.submitError = function (err) {
        this.formState = FormState.ERROR;
        this.formErrors = this.mapFormErrors(err.responseJSON);
        this.handleErrorResponse({ responseJSON: this.formErrors });
    };
    FormModel.prototype.mapFormErrors = function (responseJSON) {
        return responseJSON;
    };
    __decorate([
        observable
    ], FormModel.prototype, "errors", void 0);
    __decorate([
        observable
    ], FormModel.prototype, "fieldState", void 0);
    __decorate([
        observable
    ], FormModel.prototype, "formState", void 0);
    __decorate([
        computed
    ], FormModel.prototype, "formChanged", null);
    __decorate([
        computed
    ], FormModel.prototype, "formData", null);
    __decorate([
        computed
    ], FormModel.prototype, "isSaving", null);
    __decorate([
        computed
    ], FormModel.prototype, "isError", null);
    __decorate([
        action
    ], FormModel.prototype, "setValue", null);
    __decorate([
        action
    ], FormModel.prototype, "validateField", null);
    __decorate([
        action
    ], FormModel.prototype, "updateShowSaveState", null);
    __decorate([
        action
    ], FormModel.prototype, "updateShowReturnButtonState", null);
    __decorate([
        action
    ], FormModel.prototype, "undo", null);
    __decorate([
        action
    ], FormModel.prototype, "saveForm", null);
    __decorate([
        action
    ], FormModel.prototype, "saveField", null);
    __decorate([
        action
    ], FormModel.prototype, "saveFieldRequest", null);
    __decorate([
        action
    ], FormModel.prototype, "handleBlurField", null);
    __decorate([
        action
    ], FormModel.prototype, "setFormSaving", null);
    __decorate([
        action
    ], FormModel.prototype, "handleSaveField", null);
    __decorate([
        action
    ], FormModel.prototype, "handleCancelSaveField", null);
    __decorate([
        action
    ], FormModel.prototype, "setFieldState", null);
    __decorate([
        action
    ], FormModel.prototype, "setSaving", null);
    __decorate([
        action
    ], FormModel.prototype, "setError", null);
    __decorate([
        action
    ], FormModel.prototype, "validateForm", null);
    __decorate([
        action
    ], FormModel.prototype, "handleErrorResponse", null);
    __decorate([
        action
    ], FormModel.prototype, "submitSuccess", null);
    __decorate([
        action
    ], FormModel.prototype, "submitError", null);
    return FormModel;
}());
export default FormModel;
//# sourceMappingURL=model.jsx.map