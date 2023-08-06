import { __assign, __extends, __rest } from "tslib";
import debounce from 'lodash/debounce';
import React from 'react';
import * as Sentry from '@sentry/react';
import NoteInput from 'app/components/activity/note/input';
import localStorage from 'app/utils/localStorage';
var defaultProps = {
    /**
     * Triggered when local storage has been loaded and parsed.
     */
    onLoad: function (data) { return data; },
    onSave: function (data) { return data; },
};
var NoteInputWithStorage = /** @class */ (function (_super) {
    __extends(NoteInputWithStorage, _super);
    function NoteInputWithStorage() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.save = debounce(function (value) {
            var _a;
            var _b = _this.props, itemKey = _b.itemKey, onSave = _b.onSave;
            var currentObj = _this.fetchFromStorage() || {};
            _this.saveToStorage(__assign(__assign({}, currentObj), (_a = {}, _a[itemKey] = onSave(value), _a)));
        }, 150);
        _this.handleChange = function (e, options) {
            if (options === void 0) { options = {}; }
            var onChange = _this.props.onChange;
            if (onChange) {
                onChange(e, options);
            }
            if (options.updating) {
                return;
            }
            _this.save(e.target.value);
        };
        /**
         * Handler when note is created.
         *
         * Remove in progress item from local storage if it exists
         */
        _this.handleCreate = function (data) {
            var _a = _this.props, itemKey = _a.itemKey, onCreate = _a.onCreate;
            if (onCreate) {
                onCreate(data);
            }
            // Remove from local storage
            var storageObj = _this.fetchFromStorage() || {};
            // Nothing from this `itemKey` is saved to storage, do nothing
            if (!storageObj.hasOwnProperty(itemKey)) {
                return;
            }
            // Remove `itemKey` from stored object and save to storage
            // eslint-disable-next-line no-unused-vars
            var _b = storageObj, _c = itemKey, _oldItem = _b[_c], newStorageObj = __rest(_b, [typeof _c === "symbol" ? _c : _c + ""]);
            _this.saveToStorage(newStorageObj);
        };
        return _this;
    }
    NoteInputWithStorage.prototype.fetchFromStorage = function () {
        var storageKey = this.props.storageKey;
        var storage = localStorage.getItem(storageKey);
        if (!storage) {
            return null;
        }
        try {
            return JSON.parse(storage);
        }
        catch (err) {
            Sentry.withScope(function (scope) {
                scope.setExtra('storage', storage);
                Sentry.captureException(err);
            });
            return null;
        }
    };
    NoteInputWithStorage.prototype.saveToStorage = function (obj) {
        var storageKey = this.props.storageKey;
        try {
            localStorage.setItem(storageKey, JSON.stringify(obj));
        }
        catch (err) {
            Sentry.captureException(err);
            Sentry.withScope(function (scope) {
                scope.setExtra('storage', obj);
                Sentry.captureException(err);
            });
        }
    };
    NoteInputWithStorage.prototype.getValue = function () {
        var _a = this.props, itemKey = _a.itemKey, text = _a.text, onLoad = _a.onLoad;
        if (text) {
            return text;
        }
        var storageObj = this.fetchFromStorage();
        if (!storageObj) {
            return '';
        }
        if (!storageObj.hasOwnProperty(itemKey)) {
            return '';
        }
        if (!onLoad) {
            return storageObj[itemKey];
        }
        return onLoad(storageObj[itemKey]);
    };
    NoteInputWithStorage.prototype.render = function () {
        // Make sure `this.props` does not override `onChange` and `onCreate`
        return (<NoteInput {...this.props} text={this.getValue()} onCreate={this.handleCreate} onChange={this.handleChange}/>);
    };
    NoteInputWithStorage.defaultProps = defaultProps;
    return NoteInputWithStorage;
}(React.Component));
export default NoteInputWithStorage;
//# sourceMappingURL=inputWithStorage.jsx.map