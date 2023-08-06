import { __assign, __read, __rest, __spread } from "tslib";
var RealClient = jest.requireActual('app/api');
var Request = /** @class */ (function () {
    function Request() {
    }
    return Request;
}());
export { Request };
var respond = function (isAsync, fn) {
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    if (fn) {
        if (isAsync) {
            setTimeout(function () { return fn.apply(void 0, __spread(args)); }, 1);
        }
        else {
            fn.apply(void 0, __spread(args));
        }
    }
};
var DEFAULT_MOCK_RESPONSE_OPTIONS = {
    predicate: function () { return true; },
};
var mergeMock = jest.fn();
var Client = /** @class */ (function () {
    function Client() {
        this.hasProjectBeenRenamed = RealClient.Client.prototype.hasProjectBeenRenamed;
        this.handleRequestError = RealClient.Client.prototype.handleRequestError;
        this.bulkUpdate = RealClient.Client.prototype.bulkUpdate;
        this._chain = RealClient.Client.prototype._chain;
        this._wrapRequest = RealClient.Client.prototype._wrapRequest;
    }
    Client.clearMockResponses = function () {
        Client.mockResponses = [];
    };
    // Returns a jest mock that represents Client.request calls
    Client.addMockResponse = function (response, options) {
        if (options === void 0) { options = DEFAULT_MOCK_RESPONSE_OPTIONS; }
        var mock = jest.fn();
        Client.mockResponses.unshift([
            __assign(__assign({ statusCode: 200, body: '', method: 'GET', callCount: 0 }, response), { headers: response.headers || {} }),
            mock,
            options.predicate,
        ]);
        return mock;
    };
    Client.findMockResponse = function (url, options) {
        return Client.mockResponses.find(function (_a) {
            var _b = __read(_a, 3), response = _b[0], _mock = _b[1], predicate = _b[2];
            var matchesURL = url === response.url;
            var matchesMethod = (options.method || 'GET') === response.method;
            var matchesPredicate = predicate(url, options);
            return matchesURL && matchesMethod && matchesPredicate;
        });
    };
    Client.prototype.uniqueId = function () {
        return '123';
    };
    // In the real client, this clears in-flight responses. It's NOT clearMockResponses. You probably don't want to call this from a test.
    Client.prototype.clear = function () { };
    Client.prototype.wrapCallback = function (_id, error) {
        var _this = this;
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            // @ts-expect-error
            if (_this.hasProjectBeenRenamed.apply(_this, __spread(args))) {
                return;
            }
            respond.apply(void 0, __spread([Client.mockAsync, error], args));
        };
    };
    Client.prototype.requestPromise = function (path, _a) {
        var _this = this;
        if (_a === void 0) { _a = {}; }
        var includeAllArgs = _a.includeAllArgs, options = __rest(_a, ["includeAllArgs"]);
        return new Promise(function (resolve, reject) {
            _this.request(path, __assign(__assign({}, options), { success: function (data) {
                    var args = [];
                    for (var _i = 1; _i < arguments.length; _i++) {
                        args[_i - 1] = arguments[_i];
                    }
                    includeAllArgs ? resolve(__spread([data], args)) : resolve(data);
                }, error: function (error) {
                    var _args = [];
                    for (var _i = 1; _i < arguments.length; _i++) {
                        _args[_i - 1] = arguments[_i];
                    }
                    reject(error);
                } }));
        });
    };
    Client.prototype.request = function (url, options) {
        var _a;
        if (options === void 0) { options = {}; }
        var _b = __read(Client.findMockResponse(url, options) || [
            undefined,
            undefined,
        ], 2), response = _b[0], mock = _b[1];
        if (!response || !mock) {
            // Endpoints need to be mocked
            var err_1 = new Error("No mocked response found for request:\n\t" + (options.method || 'GET') + " " + url);
            // Mutate stack to drop frames since test file so that we know where in the test
            // this needs to be mocked
            var lines = (_a = err_1.stack) === null || _a === void 0 ? void 0 : _a.split('\n');
            var startIndex = lines === null || lines === void 0 ? void 0 : lines.findIndex(function (line) { return line.includes('tests/js/spec'); });
            err_1.stack = __spread(['\n', lines === null || lines === void 0 ? void 0 : lines[0]], lines === null || lines === void 0 ? void 0 : lines.slice(startIndex)).join('\n');
            // Throwing an error here does not do what we want it to do....
            // Because we are mocking an API client, we generally catch errors to show
            // user-friendly error messages, this means in tests this error gets gobbled
            // up and developer frustration ensues. Use `setTimeout` to get around this
            setTimeout(function () {
                throw err_1;
            });
        }
        else {
            // has mocked response
            // mock gets returned when we add a mock response, will represent calls to api.request
            mock(url, options);
            var body = typeof response.body === 'function' ? response.body(url, options) : response.body;
            if (response.statusCode !== 200) {
                response.callCount++;
                var deferred = $.Deferred();
                var errorResponse = Object.assign({
                    status: response.statusCode,
                    responseText: JSON.stringify(body),
                    responseJSON: body,
                }, {
                    overrideMimeType: function () { },
                    abort: function () { },
                    then: function () { },
                    error: function () { },
                }, deferred, new XMLHttpRequest());
                this.handleRequestError({
                    id: '1234',
                    path: url,
                    requestOptions: options,
                }, errorResponse, 'error', 'error');
            }
            else {
                response.callCount++;
                respond(Client.mockAsync, options.success, body, {}, {
                    getResponseHeader: function (key) { return response.headers[key]; },
                });
            }
        }
        respond(Client.mockAsync, options.complete);
    };
    Client.prototype.merge = function (params, options) {
        mergeMock(params, options);
        return RealClient.Client.prototype.merge.call(this, params, options);
    };
    Client.mockResponses = [];
    Client.mockAsync = false;
    return Client;
}());
export { Client, mergeMock };
//# sourceMappingURL=api.jsx.map