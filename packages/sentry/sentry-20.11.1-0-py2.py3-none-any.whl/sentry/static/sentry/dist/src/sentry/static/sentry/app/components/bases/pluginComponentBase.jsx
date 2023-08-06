import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import isFunction from 'lodash/isFunction';
import { Client } from 'app/api';
import { FormState, GenericField } from 'app/components/forms';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
var callbackWithArgs = function (context, callback) {
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    return isFunction(callback) ? callback.bind.apply(callback, __spread([context], args)) : undefined;
};
var PluginComponentBase = /** @class */ (function (_super) {
    __extends(PluginComponentBase, _super);
    function PluginComponentBase(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.api = new Client();
        [
            'onLoadSuccess',
            'onLoadError',
            'onSave',
            'onSaveSuccess',
            'onSaveError',
            'onSaveComplete',
            'renderField',
        ].map(function (method) { return (_this[method] = _this[method].bind(_this)); });
        if (_this.fetchData) {
            _this.fetchData = _this.onLoad.bind(_this, _this.fetchData.bind(_this));
        }
        if (_this.onSubmit) {
            _this.onSubmit = _this.onSave.bind(_this, _this.onSubmit.bind(_this));
        }
        _this.state = {
            state: FormState.READY,
        };
        return _this;
    }
    PluginComponentBase.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    PluginComponentBase.prototype.fetchData = function () {
        // Allow children to implement this
    };
    PluginComponentBase.prototype.onSubmit = function () {
        // Allow children to implement this
    };
    PluginComponentBase.prototype.onLoad = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        this.setState({
            state: FormState.LOADING,
        }, callbackWithArgs.apply(void 0, __spread([this, callback], args)));
    };
    PluginComponentBase.prototype.onLoadSuccess = function () {
        this.setState({
            state: FormState.READY,
        });
    };
    PluginComponentBase.prototype.onLoadError = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        this.setState({
            state: FormState.ERROR,
        }, callbackWithArgs.apply(void 0, __spread([this, callback], args)));
        addErrorMessage(t('An error occurred.'));
    };
    PluginComponentBase.prototype.onSave = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        if (this.state.state === FormState.SAVING) {
            return;
        }
        callback = callbackWithArgs.apply(void 0, __spread([this, callback], args));
        this.setState({
            state: FormState.SAVING,
        }, function () {
            addLoadingMessage(t('Saving changes\u2026'));
            callback && callback();
        });
    };
    PluginComponentBase.prototype.onSaveSuccess = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        callback = callbackWithArgs.apply(void 0, __spread([this, callback], args));
        this.setState({
            state: FormState.READY,
        }, function () { return callback && callback(); });
        setTimeout(function () {
            addSuccessMessage(t('Success!'));
        }, 0);
    };
    PluginComponentBase.prototype.onSaveError = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        callback = callbackWithArgs.apply(void 0, __spread([this, callback], args));
        this.setState({
            state: FormState.ERROR,
        }, function () { return callback && callback(); });
        setTimeout(function () {
            addErrorMessage(t('Unable to save changes. Please try again.'));
        }, 0);
    };
    PluginComponentBase.prototype.onSaveComplete = function (callback) {
        var args = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            args[_i - 1] = arguments[_i];
        }
        clearIndicators();
        callback = callbackWithArgs.apply(void 0, __spread([this, callback], args));
        callback && callback();
    };
    PluginComponentBase.prototype.renderField = function (props) {
        var _a;
        props = __assign({}, props);
        var newProps = __assign(__assign({}, props), { formState: this.state.state });
        return <GenericField key={(_a = newProps.config) === null || _a === void 0 ? void 0 : _a.name} {...newProps}/>;
    };
    return PluginComponentBase;
}(React.Component));
export default PluginComponentBase;
//# sourceMappingURL=pluginComponentBase.jsx.map