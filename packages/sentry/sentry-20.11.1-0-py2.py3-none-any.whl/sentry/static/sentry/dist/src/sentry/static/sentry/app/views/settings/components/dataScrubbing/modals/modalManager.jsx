import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import isEqual from 'lodash/isEqual';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import { RuleType, MethodType, EventIdStatus, } from '../types';
import submitRules from '../submitRules';
import Form from './form';
import Modal from './modal';
import handleError, { ErrorType } from './handleError';
import { valueSuggestions } from '../utils';
import { fetchSourceGroupData, saveToSourceGroupData } from './utils';
var ModalManager = /** @class */ (function (_super) {
    __extends(ModalManager, _super);
    function ModalManager() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.handleChange = function (field, value) {
            var _a;
            var values = __assign(__assign({}, _this.state.values), (_a = {}, _a[field] = value, _a));
            if (values.type !== RuleType.PATTERN && values.pattern) {
                values.pattern = '';
            }
            if (values.method !== MethodType.REPLACE && values.placeholder) {
                values.placeholder = '';
            }
            _this.setState(function (prevState) { return ({
                values: values,
                requiredValues: _this.getRequiredValues(values),
                errors: omit(prevState.errors, field),
            }); });
        };
        _this.handleSave = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, endpoint, api, onSubmitSuccess, closeModal, onGetNewRules, newRules, data, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, endpoint = _a.endpoint, api = _a.api, onSubmitSuccess = _a.onSubmitSuccess, closeModal = _a.closeModal, onGetNewRules = _a.onGetNewRules;
                        newRules = onGetNewRules(this.state.values);
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, submitRules(api, endpoint, newRules)];
                    case 2:
                        data = _b.sent();
                        onSubmitSuccess(data);
                        closeModal();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertRequestError(handleError(error_1));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleValidate = function (field) { return function () {
            var isFieldValueEmpty = !_this.state.values[field].trim();
            var fieldErrorAlreadyExist = _this.state.errors[field];
            if (isFieldValueEmpty && fieldErrorAlreadyExist) {
                return;
            }
            if (isFieldValueEmpty && !fieldErrorAlreadyExist) {
                _this.setState(function (prevState) {
                    var _a;
                    return ({
                        errors: __assign(__assign({}, prevState.errors), (_a = {}, _a[field] = t('Field Required'), _a)),
                    });
                });
                return;
            }
            if (!isFieldValueEmpty && fieldErrorAlreadyExist) {
                _this.clearError(field);
            }
        }; };
        _this.handleUpdateEventId = function (eventId) {
            if (eventId === _this.state.eventId.value) {
                return;
            }
            _this.setState({
                eventId: { value: eventId, status: EventIdStatus.UNDEFINED },
            });
        };
        return _this;
    }
    ModalManager.prototype.componentDidMount = function () {
        this.handleValidateForm();
    };
    ModalManager.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (!isEqual(prevState.values, this.state.values)) {
            this.handleValidateForm();
        }
        if (prevState.eventId.value !== this.state.eventId.value) {
            this.loadSourceSuggestions();
        }
        if (prevState.eventId.status !== this.state.eventId.status) {
            saveToSourceGroupData(this.state.eventId, this.state.sourceSuggestions);
        }
    };
    ModalManager.prototype.getDefaultState = function () {
        var _a = fetchSourceGroupData(), eventId = _a.eventId, sourceSuggestions = _a.sourceSuggestions;
        var values = this.getInitialValues();
        return {
            values: values,
            requiredValues: this.getRequiredValues(values),
            errors: {},
            isFormValid: false,
            eventId: {
                value: eventId,
                status: !eventId ? EventIdStatus.UNDEFINED : EventIdStatus.LOADED,
            },
            sourceSuggestions: sourceSuggestions,
        };
    };
    ModalManager.prototype.getInitialValues = function () {
        var _a, _b, _c, _d, _e;
        var initialState = this.props.initialState;
        return {
            type: (_a = initialState === null || initialState === void 0 ? void 0 : initialState.type) !== null && _a !== void 0 ? _a : RuleType.CREDITCARD,
            method: (_b = initialState === null || initialState === void 0 ? void 0 : initialState.method) !== null && _b !== void 0 ? _b : MethodType.MASK,
            source: (_c = initialState === null || initialState === void 0 ? void 0 : initialState.source) !== null && _c !== void 0 ? _c : '',
            placeholder: (_d = initialState === null || initialState === void 0 ? void 0 : initialState.placeholder) !== null && _d !== void 0 ? _d : '',
            pattern: (_e = initialState === null || initialState === void 0 ? void 0 : initialState.pattern) !== null && _e !== void 0 ? _e : '',
        };
    };
    ModalManager.prototype.getRequiredValues = function (values) {
        var type = values.type;
        var requiredValues = ['type', 'method', 'source'];
        if (type === RuleType.PATTERN) {
            requiredValues.push('pattern');
        }
        return requiredValues;
    };
    ModalManager.prototype.clearError = function (field) {
        this.setState(function (prevState) { return ({
            errors: omit(prevState.errors, field),
        }); });
    };
    ModalManager.prototype.loadSourceSuggestions = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, orgSlug, projectId, api, eventId, query, rawSuggestions, sourceSuggestions_1, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, orgSlug = _a.orgSlug, projectId = _a.projectId, api = _a.api;
                        eventId = this.state.eventId;
                        if (!eventId.value) {
                            this.setState(function (prevState) { return ({
                                sourceSuggestions: valueSuggestions,
                                eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.UNDEFINED }),
                            }); });
                            return [2 /*return*/];
                        }
                        this.setState(function (prevState) { return ({
                            sourceSuggestions: valueSuggestions,
                            eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.LOADING }),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        query = { eventId: eventId.value };
                        if (projectId) {
                            query.projectId = projectId;
                        }
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/data-scrubbing-selector-suggestions/", { query: query })];
                    case 2:
                        rawSuggestions = _c.sent();
                        sourceSuggestions_1 = rawSuggestions.suggestions;
                        if (sourceSuggestions_1 && sourceSuggestions_1.length > 0) {
                            this.setState(function (prevState) { return ({
                                sourceSuggestions: sourceSuggestions_1,
                                eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.LOADED }),
                            }); });
                            return [2 /*return*/];
                        }
                        this.setState(function (prevState) { return ({
                            sourceSuggestions: valueSuggestions,
                            eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.NOT_FOUND }),
                        }); });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState(function (prevState) { return ({
                            eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.ERROR }),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ModalManager.prototype.convertRequestError = function (error) {
        switch (error.type) {
            case ErrorType.InvalidSelector:
                this.setState(function (prevState) { return ({
                    errors: __assign(__assign({}, prevState.errors), { source: error.message }),
                }); });
                break;
            case ErrorType.RegexParse:
                this.setState(function (prevState) { return ({
                    errors: __assign(__assign({}, prevState.errors), { pattern: error.message }),
                }); });
                break;
            default:
                addErrorMessage(error.message);
        }
    };
    ModalManager.prototype.handleValidateForm = function () {
        var _a = this.state, values = _a.values, requiredValues = _a.requiredValues;
        var isFormValid = requiredValues.every(function (requiredValue) { return !!values[requiredValue]; });
        this.setState({ isFormValid: isFormValid });
    };
    ModalManager.prototype.render = function () {
        var _a = this.state, values = _a.values, errors = _a.errors, isFormValid = _a.isFormValid, eventId = _a.eventId, sourceSuggestions = _a.sourceSuggestions;
        var title = this.props.title;
        return (<Modal {...this.props} title={title} onSave={this.handleSave} disabled={!isFormValid} content={<Form onChange={this.handleChange} onValidate={this.handleValidate} onUpdateEventId={this.handleUpdateEventId} eventId={eventId} errors={errors} values={values} sourceSuggestions={sourceSuggestions}/>}/>);
    };
    return ModalManager;
}(React.Component));
export default ModalManager;
//# sourceMappingURL=modalManager.jsx.map