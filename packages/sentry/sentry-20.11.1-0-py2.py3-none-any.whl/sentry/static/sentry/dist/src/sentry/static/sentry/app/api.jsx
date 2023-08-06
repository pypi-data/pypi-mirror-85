import { __assign, __read, __rest, __spread } from "tslib";
import isUndefined from 'lodash/isUndefined';
import isNil from 'lodash/isNil';
import $ from 'jquery';
import { Severity } from '@sentry/react';
import { PROJECT_MOVED, SUDO_REQUIRED, SUPERUSER_REQUIRED, } from 'app/constants/apiErrorCodes';
import { run } from 'app/utils/apiSentryClient';
import { metric } from 'app/utils/analytics';
import { openSudo, redirectToProject } from 'app/actionCreators/modal';
import { uniqueId } from 'app/utils/guid';
import GroupActions from 'app/actions/groupActions';
import createRequestError from 'app/utils/requestError/createRequestError';
var Request = /** @class */ (function () {
    function Request(xhr) {
        this.xhr = xhr;
        this.alive = true;
    }
    Request.prototype.cancel = function () {
        this.alive = false;
        this.xhr.abort();
        metric('app.api.request-abort', 1);
    };
    return Request;
}());
export { Request };
/**
 * Converts input parameters to API-compatible query arguments
 * @param params
 */
export function paramsToQueryArgs(params) {
    var p = params.itemIds
        ? { id: params.itemIds } // items matching array of itemids
        : params.query
            ? { query: params.query } // items matching search query
            : {}; // all items
    // only include environment if it is not null/undefined
    if (params.query && !isNil(params.environment)) {
        p.environment = params.environment;
    }
    // only include projects if it is not null/undefined/an empty array
    if (params.project && params.project.length) {
        p.project = params.project;
    }
    // only include date filters if they are not null/undefined
    if (params.query) {
        ['start', 'end', 'period', 'utc'].forEach(function (prop) {
            if (!isNil(params[prop])) {
                p[prop === 'period' ? 'statsPeriod' : prop] = params[prop];
            }
        });
    }
    return p;
}
var Client = /** @class */ (function () {
    function Client(options) {
        if (options === void 0) { options = {}; }
        if (isUndefined(options)) {
            options = {};
        }
        this.baseUrl = options.baseUrl || '/api/0';
        this.activeRequests = {};
    }
    /**
     * Check if the API response says project has been renamed.
     * If so, redirect user to new project slug
     */
    // TODO: refine this type later
    Client.prototype.hasProjectBeenRenamed = function (response) {
        var _a, _b, _c, _d, _e;
        var code = (_b = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
        // XXX(billy): This actually will never happen because we can't intercept the 302
        // jQuery ajax will follow the redirect by default...
        if (code !== PROJECT_MOVED) {
            return false;
        }
        var slug = (_e = (_d = (_c = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra) === null || _e === void 0 ? void 0 : _e.slug;
        redirectToProject(slug);
        return true;
    };
    Client.prototype.wrapCallback = function (id, func, cleanup) {
        var _this = this;
        if (cleanup === void 0) { cleanup = false; }
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var req = _this.activeRequests[id];
            if (cleanup === true) {
                delete _this.activeRequests[id];
            }
            if (req && req.alive) {
                // Check if API response is a 302 -- means project slug was renamed and user
                // needs to be redirected
                // @ts-expect-error
                if (_this.hasProjectBeenRenamed.apply(_this, __spread(args))) {
                    return;
                }
                if (isUndefined(func)) {
                    return;
                }
                // Call success callback
                return func.apply(req, args); // eslint-disable-line
            }
        };
    };
    /**
     * Attempt to cancel all active XHR requests
     */
    Client.prototype.clear = function () {
        for (var id in this.activeRequests) {
            this.activeRequests[id].cancel();
        }
    };
    Client.prototype.handleRequestError = function (_a, response, textStatus, errorThrown) {
        var _this = this;
        var _b, _c;
        var id = _a.id, path = _a.path, requestOptions = _a.requestOptions;
        var code = (_c = (_b = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _b === void 0 ? void 0 : _b.detail) === null || _c === void 0 ? void 0 : _c.code;
        var isSudoRequired = code === SUDO_REQUIRED || code === SUPERUSER_REQUIRED;
        if (isSudoRequired) {
            openSudo({
                superuser: code === SUPERUSER_REQUIRED,
                sudo: code === SUDO_REQUIRED,
                retryRequest: function () {
                    return _this.requestPromise(path, requestOptions)
                        .then(function (data) {
                        if (typeof requestOptions.success !== 'function') {
                            return;
                        }
                        requestOptions.success(data);
                    })
                        .catch(function (err) {
                        if (typeof requestOptions.error !== 'function') {
                            return;
                        }
                        requestOptions.error(err);
                    });
                },
                onClose: function () {
                    if (typeof requestOptions.error !== 'function') {
                        return;
                    }
                    // If modal was closed, then forward the original response
                    requestOptions.error(response);
                },
            });
            return;
        }
        // Call normal error callback
        var errorCb = this.wrapCallback(id, requestOptions.error);
        if (typeof errorCb !== 'function') {
            return;
        }
        errorCb(response, textStatus, errorThrown);
    };
    Client.prototype.request = function (path, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var method = options.method || (options.data ? 'POST' : 'GET');
        var data = options.data;
        if (!isUndefined(data) && method !== 'GET') {
            data = JSON.stringify(data);
        }
        var query;
        try {
            query = $.param(options.query || [], true);
        }
        catch (err) {
            run(function (Sentry) {
                return Sentry.withScope(function (scope) {
                    scope.setExtra('path', path);
                    scope.setExtra('query', options.query);
                    Sentry.captureException(err);
                });
            });
            throw err;
        }
        var id = uniqueId();
        metric.mark({ name: "api-request-start-" + id });
        var fullUrl;
        if (path.indexOf(this.baseUrl) === -1) {
            fullUrl = this.baseUrl + path;
        }
        else {
            fullUrl = path;
        }
        if (query) {
            if (fullUrl.indexOf('?') !== -1) {
                fullUrl += '&' + query;
            }
            else {
                fullUrl += '?' + query;
            }
        }
        var errorObject = new Error();
        this.activeRequests[id] = new Request($.ajax({
            url: fullUrl,
            method: method,
            data: data,
            contentType: 'application/json',
            headers: {
                Accept: 'application/json; charset=utf-8',
            },
            success: function (responseData, textStatus, xhr) {
                metric.measure({
                    name: 'app.api.request-success',
                    start: "api-request-start-" + id,
                    data: {
                        status: xhr && xhr.status,
                    },
                });
                if (!isUndefined(options.success)) {
                    _this.wrapCallback(id, options.success)(responseData, textStatus, xhr);
                }
            },
            error: function (resp, textStatus, errorThrown) {
                metric.measure({
                    name: 'app.api.request-error',
                    start: "api-request-start-" + id,
                    data: {
                        status: resp && resp.status,
                    },
                });
                if (resp && resp.status !== 0 && resp.status !== 404) {
                    run(function (Sentry) {
                        return Sentry.withScope(function (scope) {
                            // `requestPromise` can pass its error object
                            var preservedError = options.preservedError || errorObject;
                            var errorObjectToUse = createRequestError(resp, preservedError.stack, method, path);
                            errorObjectToUse.removeFrames(3);
                            // Setting this to warning because we are going to capture all failed requests
                            scope.setLevel(Severity.Warning);
                            scope.setTag('http.statusCode', String(resp.status));
                            Sentry.captureException(errorObjectToUse);
                        });
                    });
                }
                _this.handleRequestError({
                    id: id,
                    path: path,
                    requestOptions: options,
                }, resp, textStatus, errorThrown);
            },
            complete: function (jqXHR, textStatus) {
                return _this.wrapCallback(id, options.complete, true)(jqXHR, textStatus);
            },
        }));
        return this.activeRequests[id];
    };
    Client.prototype.requestPromise = function (path, _a) {
        var _this = this;
        if (_a === void 0) { _a = {}; }
        var includeAllArgs = _a.includeAllArgs, options = __rest(_a, ["includeAllArgs"]);
        // Create an error object here before we make any async calls so
        // that we have a helpful stack trace if it errors
        //
        // This *should* get logged to Sentry only if the promise rejection is not handled
        // (since SDK captures unhandled rejections). Ideally we explicitly ignore rejection
        // or handle with a user friendly error message
        var preservedError = new Error();
        return new Promise(function (resolve, reject) {
            _this.request(path, __assign(__assign({}, options), { preservedError: preservedError, success: function (data, textStatus, xhr) {
                    includeAllArgs ? resolve([data, textStatus, xhr]) : resolve(data);
                }, error: function (resp) {
                    var errorObjectToUse = createRequestError(resp, preservedError.stack, options.method, path);
                    errorObjectToUse.removeFrames(2);
                    // Although `this.request` logs all error responses, this error object can
                    // potentially be logged by Sentry's unhandled rejection handler
                    reject(errorObjectToUse);
                } }));
        });
    };
    Client.prototype._chain = function () {
        var funcs = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            funcs[_i] = arguments[_i];
        }
        var filteredFuncs = funcs.filter(function (f) { return typeof f === 'function'; });
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            filteredFuncs.forEach(function (func) {
                func.apply(funcs, args);
            });
        };
    };
    Client.prototype._wrapRequest = function (path, options, extraParams) {
        if (isUndefined(extraParams)) {
            extraParams = {};
        }
        options.success = this._chain(options.success, extraParams.success);
        options.error = this._chain(options.error, extraParams.error);
        options.complete = this._chain(options.complete, extraParams.complete);
        return this.request(path, options);
    };
    Client.prototype.bulkDelete = function (params, options) {
        var path = params.projectId
            ? "/projects/" + params.orgId + "/" + params.projectId + "/issues/"
            : "/organizations/" + params.orgId + "/issues/";
        var query = paramsToQueryArgs(params);
        var id = uniqueId();
        GroupActions.delete(id, params.itemIds);
        return this._wrapRequest(path, {
            query: query,
            method: 'DELETE',
            success: function (response) {
                GroupActions.deleteSuccess(id, params.itemIds, response);
            },
            error: function (error) {
                GroupActions.deleteError(id, params.itemIds, error);
            },
        }, options);
    };
    Client.prototype.bulkUpdate = function (params, options) {
        var path = params.projectId
            ? "/projects/" + params.orgId + "/" + params.projectId + "/issues/"
            : "/organizations/" + params.orgId + "/issues/";
        var query = paramsToQueryArgs(params);
        var id = uniqueId();
        GroupActions.update(id, params.itemIds, params.data);
        return this._wrapRequest(path, {
            query: query,
            method: 'PUT',
            data: params.data,
            success: function (response) {
                GroupActions.updateSuccess(id, params.itemIds, response);
            },
            error: function (error) {
                GroupActions.updateError(id, params.itemIds, error, params.failSilently);
            },
        }, options);
    };
    Client.prototype.merge = function (params, options) {
        var path = params.projectId
            ? "/projects/" + params.orgId + "/" + params.projectId + "/issues/"
            : "/organizations/" + params.orgId + "/issues/";
        var query = paramsToQueryArgs(params);
        var id = uniqueId();
        GroupActions.merge(id, params.itemIds);
        return this._wrapRequest(path, {
            query: query,
            method: 'PUT',
            data: { merge: 1 },
            success: function (response) {
                GroupActions.mergeSuccess(id, params.itemIds, response);
            },
            error: function (error) {
                GroupActions.mergeError(id, params.itemIds, error);
            },
        }, options);
    };
    return Client;
}());
export { Client };
//# sourceMappingURL=api.jsx.map