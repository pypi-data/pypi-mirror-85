import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import isEqual from 'lodash/isEqual';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from './form';
import Modal from './modal';
import handleXhrErrorResponse from './handleXhrErrorResponse';
var DialogManager = /** @class */ (function (_super) {
    __extends(DialogManager, _super);
    function DialogManager() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.handleChange = function (field, value) {
            _this.setState(function (prevState) {
                var _a;
                return ({
                    values: __assign(__assign({}, prevState.values), (_a = {}, _a[field] = value, _a)),
                    errors: omit(prevState.errors, field),
                });
            });
        };
        _this.handleSave = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, onSubmitSuccess, closeModal, orgSlug, api, trustedRelays, response, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, onSubmitSuccess = _a.onSubmitSuccess, closeModal = _a.closeModal, orgSlug = _a.orgSlug, api = _a.api;
                        trustedRelays = this.getData().trustedRelays.map(function (trustedRelay) {
                            return omit(trustedRelay, ['created', 'lastModified']);
                        });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/", {
                                method: 'PUT',
                                data: { trustedRelays: trustedRelays },
                            })];
                    case 2:
                        response = _b.sent();
                        onSubmitSuccess(response);
                        closeModal();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertErrorXhrResponse(handleXhrErrorResponse(error_1));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleValidate = function (field) { return function () {
            var isFieldValueEmpty = !_this.state.values[field].replace(/\s/g, '');
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
        _this.handleValidateKey = function () {
            var savedRelays = _this.props.savedRelays;
            var _a = _this.state, values = _a.values, errors = _a.errors;
            var isKeyAlreadyTaken = savedRelays.find(function (savedRelay) { return savedRelay.publicKey === values.publicKey; });
            if (isKeyAlreadyTaken && !errors.publicKey) {
                _this.setState({
                    errors: __assign(__assign({}, errors), { publicKey: t('Relay key already taken') }),
                });
                return;
            }
            if (errors.publicKey) {
                _this.setState({
                    errors: omit(errors, 'publicKey'),
                });
            }
            _this.handleValidate('publicKey')();
        };
        return _this;
    }
    DialogManager.prototype.componentDidMount = function () {
        this.validateForm();
    };
    DialogManager.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (!isEqual(prevState.values, this.state.values)) {
            this.validateForm();
        }
        if (!isEqual(prevState.errors, this.state.errors) &&
            Object.keys(this.state.errors).length > 0) {
            this.setValidForm(false);
        }
    };
    DialogManager.prototype.getDefaultState = function () {
        return {
            values: { name: '', publicKey: '', description: '' },
            requiredValues: ['name', 'publicKey'],
            errors: {},
            disables: {},
            isFormValid: false,
            title: this.getTitle(),
        };
    };
    DialogManager.prototype.getTitle = function () {
        return '';
    };
    DialogManager.prototype.getData = function () {
        // Child has to implement this
        throw new Error('Not implemented');
    };
    DialogManager.prototype.getBtnSaveLabel = function () {
        return undefined;
    };
    DialogManager.prototype.setValidForm = function (isFormValid) {
        this.setState({ isFormValid: isFormValid });
    };
    DialogManager.prototype.validateForm = function () {
        var _a = this.state, values = _a.values, requiredValues = _a.requiredValues, errors = _a.errors;
        var isFormValid = requiredValues.every(function (requiredValue) {
            return !!values[requiredValue].replace(/\s/g, '') && !errors[requiredValue];
        });
        this.setValidForm(isFormValid);
    };
    DialogManager.prototype.clearError = function (field) {
        this.setState(function (prevState) { return ({
            errors: omit(prevState.errors, field),
        }); });
    };
    DialogManager.prototype.convertErrorXhrResponse = function (error) {
        switch (error.type) {
            case 'invalid-key':
            case 'missing-key':
                this.setState(function (prevState) { return ({
                    errors: __assign(__assign({}, prevState.errors), { publicKey: error.message }),
                }); });
                break;
            case 'empty-name':
            case 'missing-name':
                this.setState(function (prevState) { return ({
                    errors: __assign(__assign({}, prevState.errors), { name: error.message }),
                }); });
                break;
            default:
                addErrorMessage(error.message);
        }
    };
    DialogManager.prototype.getForm = function () {
        var _a = this.state, values = _a.values, errors = _a.errors, disables = _a.disables, isFormValid = _a.isFormValid;
        return (<Form isFormValid={isFormValid} onSave={this.handleSave} onChange={this.handleChange} onValidate={this.handleValidate} onValidateKey={this.handleValidateKey} errors={errors} values={values} disables={disables}/>);
    };
    DialogManager.prototype.getContent = function () {
        return this.getForm();
    };
    DialogManager.prototype.render = function () {
        var _a = this.state, title = _a.title, isFormValid = _a.isFormValid;
        var btnSaveLabel = this.getBtnSaveLabel();
        var content = this.getContent();
        return (<Modal {...this.props} title={title} onSave={this.handleSave} btnSaveLabel={btnSaveLabel} disabled={!isFormValid} content={content}/>);
    };
    return DialogManager;
}(React.Component));
export default DialogManager;
//# sourceMappingURL=modalManager.jsx.map