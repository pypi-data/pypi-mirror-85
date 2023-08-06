var _a, _b;
import { __assign } from "tslib";
import { assert } from 'app/types/utils';
// Refer to src/sentry/api/event_search.py
export var AGGREGATIONS = {
    count: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    count_unique: {
        parameters: [
            {
                kind: 'column',
                columnTypes: ['string', 'integer', 'number', 'duration', 'date', 'boolean'],
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    min: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate([
                    'integer',
                    'number',
                    'duration',
                    'date',
                ]),
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    max: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate([
                    'integer',
                    'number',
                    'duration',
                    'date',
                ]),
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    avg: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    sum: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'area',
    },
    last_seen: {
        parameters: [],
        outputType: 'date',
        isSortable: true,
        multiPlotType: 'area',
    },
    // Tracing functions.
    p50: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p75: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p95: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        type: [],
        isSortable: true,
        multiPlotType: 'line',
    },
    p99: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p100: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    percentile: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: true,
            },
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '0.5',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    failure_rate: {
        parameters: [],
        outputType: 'percentage',
        isSortable: true,
        multiPlotType: 'line',
    },
    apdex: {
        generateDefaultValue: function (_a) {
            var _b, _c;
            var parameter = _a.parameter, organization = _a.organization;
            return (_c = (_b = organization.apdexThreshold) === null || _b === void 0 ? void 0 : _b.toString()) !== null && _c !== void 0 ? _c : parameter.defaultValue;
        },
        parameters: [
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    user_misery: {
        generateDefaultValue: function (_a) {
            var _b, _c;
            var parameter = _a.parameter, organization = _a.organization;
            return (_c = (_b = organization.apdexThreshold) === null || _b === void 0 ? void 0 : _b.toString()) !== null && _c !== void 0 ? _c : parameter.defaultValue;
        },
        parameters: [
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: false,
        multiPlotType: 'area',
    },
    eps: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    epm: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
};
// TPM and TPS are aliases that are only used in Performance
export var ALIASES = {
    tpm: 'epm',
    tps: 'eps',
};
assert(AGGREGATIONS);
var FieldKey;
(function (FieldKey) {
    FieldKey["CULPRIT"] = "culprit";
    FieldKey["DEVICE_ARCH"] = "device.arch";
    FieldKey["DEVICE_BATTERY_LEVEL"] = "device.battery_level";
    FieldKey["DEVICE_BRAND"] = "device.brand";
    FieldKey["DEVICE_CHARGING"] = "device.charging";
    FieldKey["DEVICE_LOCALE"] = "device.locale";
    FieldKey["DEVICE_NAME"] = "device.name";
    FieldKey["DEVICE_ONLINE"] = "device.online";
    FieldKey["DEVICE_ORIENTATION"] = "device.orientation";
    FieldKey["DEVICE_SIMULATOR"] = "device.simulator";
    FieldKey["DEVICE_UUID"] = "device.uuid";
    FieldKey["DIST"] = "dist";
    FieldKey["ENVIRONMENT"] = "environment";
    FieldKey["ERROR_HANDLED"] = "error.handled";
    FieldKey["ERROR_UNHANDLED"] = "error.unhandled";
    FieldKey["ERROR_MECHANISM"] = "error.mechanism";
    FieldKey["ERROR_TYPE"] = "error.type";
    FieldKey["ERROR_VALUE"] = "error.value";
    FieldKey["EVENT_TYPE"] = "event.type";
    FieldKey["GEO_CITY"] = "geo.city";
    FieldKey["GEO_COUNTRY_CODE"] = "geo.country_code";
    FieldKey["GEO_REGION"] = "geo.region";
    FieldKey["HTTP_METHOD"] = "http.method";
    FieldKey["HTTP_REFERER"] = "http.referer";
    FieldKey["HTTP_URL"] = "http.url";
    FieldKey["ID"] = "id";
    FieldKey["ISSUE"] = "issue";
    FieldKey["LOCATION"] = "location";
    FieldKey["MESSAGE"] = "message";
    FieldKey["OS_BUILD"] = "os.build";
    FieldKey["OS_KERNEL_VERSION"] = "os.kernel_version";
    FieldKey["PLATFORM_NAME"] = "platform.name";
    FieldKey["PROJECT"] = "project";
    FieldKey["RELEASE"] = "release";
    FieldKey["SDK_NAME"] = "sdk.name";
    FieldKey["SDK_VERSION"] = "sdk.version";
    FieldKey["STACK_ABS_PATH"] = "stack.abs_path";
    FieldKey["STACK_COLNO"] = "stack.colno";
    FieldKey["STACK_FILENAME"] = "stack.filename";
    FieldKey["STACK_FUNCTION"] = "stack.function";
    FieldKey["STACK_IN_APP"] = "stack.in_app";
    FieldKey["STACK_LINENO"] = "stack.lineno";
    FieldKey["STACK_MODULE"] = "stack.module";
    FieldKey["STACK_PACKAGE"] = "stack.package";
    FieldKey["STACK_STACK_LEVEL"] = "stack.stack_level";
    FieldKey["TIME"] = "time";
    FieldKey["TIMESTAMP"] = "timestamp";
    FieldKey["TITLE"] = "title";
    FieldKey["TRACE"] = "trace";
    FieldKey["TRACE_PARENT_SPAN"] = "trace.parent_span";
    FieldKey["TRACE_SPAN"] = "trace.span";
    FieldKey["TRANSACTION"] = "transaction";
    FieldKey["TRANSACTION_DURATION"] = "transaction.duration";
    FieldKey["TRANSACTION_OP"] = "transaction.op";
    FieldKey["TRANSACTION_STATUS"] = "transaction.status";
    FieldKey["USER_EMAIL"] = "user.email";
    FieldKey["USER_ID"] = "user.id";
    FieldKey["USER_IP"] = "user.ip";
    FieldKey["USER_USERNAME"] = "user.username";
    FieldKey["USER_DISPLAY"] = "user.display";
})(FieldKey || (FieldKey = {}));
/**
 * Refer to src/sentry/snuba/events.py, search for Columns
 */
export var FIELDS = (_a = {},
    _a[FieldKey.ID] = 'string',
    // issue.id and project.id are omitted on purpose.
    // Customers should use `issue` and `project` instead.
    _a[FieldKey.TIMESTAMP] = 'date',
    _a[FieldKey.TIME] = 'date',
    _a[FieldKey.CULPRIT] = 'string',
    _a[FieldKey.LOCATION] = 'string',
    _a[FieldKey.MESSAGE] = 'string',
    _a[FieldKey.PLATFORM_NAME] = 'string',
    _a[FieldKey.ENVIRONMENT] = 'string',
    _a[FieldKey.RELEASE] = 'string',
    _a[FieldKey.DIST] = 'string',
    _a[FieldKey.TITLE] = 'string',
    _a[FieldKey.EVENT_TYPE] = 'string',
    // tags.key and tags.value are omitted on purpose as well.
    _a[FieldKey.TRANSACTION] = 'string',
    _a[FieldKey.USER_ID] = 'string',
    _a[FieldKey.USER_EMAIL] = 'string',
    _a[FieldKey.USER_USERNAME] = 'string',
    _a[FieldKey.USER_IP] = 'string',
    _a[FieldKey.SDK_NAME] = 'string',
    _a[FieldKey.SDK_VERSION] = 'string',
    _a[FieldKey.HTTP_METHOD] = 'string',
    _a[FieldKey.HTTP_REFERER] = 'string',
    _a[FieldKey.HTTP_URL] = 'string',
    _a[FieldKey.OS_BUILD] = 'string',
    _a[FieldKey.OS_KERNEL_VERSION] = 'string',
    _a[FieldKey.DEVICE_NAME] = 'string',
    _a[FieldKey.DEVICE_BRAND] = 'string',
    _a[FieldKey.DEVICE_LOCALE] = 'string',
    _a[FieldKey.DEVICE_UUID] = 'string',
    _a[FieldKey.DEVICE_ARCH] = 'string',
    _a[FieldKey.DEVICE_BATTERY_LEVEL] = 'number',
    _a[FieldKey.DEVICE_ORIENTATION] = 'string',
    _a[FieldKey.DEVICE_SIMULATOR] = 'boolean',
    _a[FieldKey.DEVICE_ONLINE] = 'boolean',
    _a[FieldKey.DEVICE_CHARGING] = 'boolean',
    _a[FieldKey.GEO_COUNTRY_CODE] = 'string',
    _a[FieldKey.GEO_REGION] = 'string',
    _a[FieldKey.GEO_CITY] = 'string',
    _a[FieldKey.ERROR_TYPE] = 'string',
    _a[FieldKey.ERROR_VALUE] = 'string',
    _a[FieldKey.ERROR_MECHANISM] = 'string',
    _a[FieldKey.ERROR_HANDLED] = 'boolean',
    _a[FieldKey.ERROR_UNHANDLED] = 'boolean',
    _a[FieldKey.STACK_ABS_PATH] = 'string',
    _a[FieldKey.STACK_FILENAME] = 'string',
    _a[FieldKey.STACK_PACKAGE] = 'string',
    _a[FieldKey.STACK_MODULE] = 'string',
    _a[FieldKey.STACK_FUNCTION] = 'string',
    _a[FieldKey.STACK_IN_APP] = 'boolean',
    _a[FieldKey.STACK_COLNO] = 'number',
    _a[FieldKey.STACK_LINENO] = 'number',
    _a[FieldKey.STACK_STACK_LEVEL] = 'number',
    // contexts.key and contexts.value omitted on purpose.
    // Transaction event fields.
    _a[FieldKey.TRANSACTION_DURATION] = 'duration',
    _a[FieldKey.TRANSACTION_OP] = 'string',
    _a[FieldKey.TRANSACTION_STATUS] = 'string',
    _a[FieldKey.TRACE] = 'string',
    _a[FieldKey.TRACE_SPAN] = 'string',
    _a[FieldKey.TRACE_PARENT_SPAN] = 'string',
    // Field alises defined in src/sentry/api/event_search.py
    _a[FieldKey.PROJECT] = 'string',
    _a[FieldKey.ISSUE] = 'string',
    _a[FieldKey.USER_DISPLAY] = 'string',
    _a);
export var FIELD_TAGS = Object.freeze(Object.fromEntries(Object.keys(FIELDS).map(function (item) { return [item, { key: item, name: item }]; })));
// This list should be removed with the tranaction-events feature flag.
export var TRACING_FIELDS = [
    'avg',
    'sum',
    'transaction.duration',
    'transaction.op',
    'transaction.status',
    'p50',
    'p75',
    'p95',
    'p99',
    'p100',
    'percentile',
    'failure_rate',
    'apdex',
    'user_misery',
    'eps',
    'epm',
];
export var WebVital;
(function (WebVital) {
    WebVital["FP"] = "measurements.fp";
    WebVital["FCP"] = "measurements.fcp";
    WebVital["LCP"] = "measurements.lcp";
    WebVital["FID"] = "measurements.fid";
    WebVital["CLS"] = "measurements.cls";
    WebVital["TTFB"] = "measurements.ttfb";
    WebVital["RequestTime"] = "measurements.ttfb.requesttime";
})(WebVital || (WebVital = {}));
var MEASUREMENTS = (_b = {},
    _b[WebVital.FP] = 'duration',
    _b[WebVital.FCP] = 'duration',
    _b[WebVital.LCP] = 'duration',
    _b[WebVital.FID] = 'duration',
    _b[WebVital.CLS] = 'number',
    _b[WebVital.TTFB] = 'duration',
    _b[WebVital.RequestTime] = 'duration',
    _b);
export var MEASUREMENT_PATTERN = /^measurements\.([a-zA-Z0-9-_.]+)$/;
export function isMeasurement(field) {
    var results = field.match(MEASUREMENT_PATTERN);
    return !!results;
}
export function measurementType(field) {
    if (MEASUREMENTS.hasOwnProperty(field)) {
        return MEASUREMENTS[field];
    }
    return 'number';
}
export function getMeasurementSlug(field) {
    var results = field.match(MEASUREMENT_PATTERN);
    if (results && results.length >= 2) {
        return results[1];
    }
    return null;
}
var AGGREGATE_PATTERN = /^([^\(]+)\((.*?)(?:\s*,\s*(.*))?\)$/;
export function getAggregateArg(field) {
    var results = field.match(AGGREGATE_PATTERN);
    if (results && results.length >= 3) {
        return results[2];
    }
    return null;
}
export function generateAggregateFields(organization, eventFields, excludeFields) {
    if (excludeFields === void 0) { excludeFields = []; }
    var functions = Object.keys(AGGREGATIONS);
    var fields = Object.values(eventFields).map(function (field) { return field.field; });
    functions.forEach(function (func) {
        var parameters = AGGREGATIONS[func].parameters.map(function (param) {
            var generator = AGGREGATIONS[func].generateDefaultValue;
            if (typeof generator === 'undefined') {
                return param;
            }
            return __assign(__assign({}, param), { defaultValue: generator({ parameter: param, organization: organization }) });
        });
        if (parameters.every(function (param) { return typeof param.defaultValue !== 'undefined'; })) {
            var newField = func + "(" + parameters
                .map(function (param) { return param.defaultValue; })
                .join(',') + ")";
            if (fields.indexOf(newField) === -1 && excludeFields.indexOf(newField) === -1) {
                fields.push(newField);
            }
        }
    });
    return fields.map(function (field) { return ({ field: field }); });
}
export function explodeFieldString(field) {
    var results = field.match(AGGREGATE_PATTERN);
    if (results && results.length >= 3) {
        return {
            kind: 'function',
            function: [
                results[1],
                results[2],
                results[3],
            ],
        };
    }
    return { kind: 'field', field: field };
}
export function generateFieldAsString(value) {
    if (value.kind === 'field') {
        return value.field;
    }
    var aggregation = value.function[0];
    var parameters = value.function.slice(1).filter(function (i) { return i; });
    return aggregation + "(" + parameters.join(',') + ")";
}
export function explodeField(field) {
    var results = explodeFieldString(field.field);
    return results;
}
/**
 * Get the alias that the API results will have for a given aggregate function name
 */
export function getAggregateAlias(field) {
    if (!field.match(AGGREGATE_PATTERN)) {
        return field;
    }
    return field
        .replace(AGGREGATE_PATTERN, '$1_$2_$3')
        .replace(/\./g, '_')
        .replace(/\,/g, '_')
        .replace(/_+$/, '');
}
/**
 * Check if a field name looks like an aggregate function or known aggregate alias.
 */
export function isAggregateField(field) {
    return field.match(AGGREGATE_PATTERN) !== null;
}
/**
 * Convert a function string into type it will output.
 * This is useful when you need to format values in tooltips,
 * or in series markers.
 */
export function aggregateOutputType(field) {
    var matches = AGGREGATE_PATTERN.exec(field);
    if (!matches) {
        return 'number';
    }
    var outputType = aggregateFunctionOutputType(matches[1], matches[2]);
    if (outputType === null) {
        return 'number';
    }
    return outputType;
}
/**
 * Converts a function string and its first argument into its output type.
 * - If the function has a fixed output type, that will be the result.
 * - If the function does not define an output type, the output type will be equal to
 *   the type of its first argument.
 * - If the function has an optional first argument, and it was not defined, make sure
 *   to use the default argument as the first argument.
 * - If the type could not be determined, return null.
 */
export function aggregateFunctionOutputType(funcName, firstArg) {
    var _a;
    var aggregate = AGGREGATIONS[ALIASES[funcName] || funcName];
    // Attempt to use the function's outputType.
    if (aggregate === null || aggregate === void 0 ? void 0 : aggregate.outputType) {
        return aggregate.outputType;
    }
    // If the first argument is undefined and it is not required,
    // then we attempt to get the default value.
    if (!firstArg && ((_a = aggregate === null || aggregate === void 0 ? void 0 : aggregate.parameters) === null || _a === void 0 ? void 0 : _a[0])) {
        if (aggregate.parameters[0].required === false) {
            firstArg = aggregate.parameters[0].defaultValue;
        }
    }
    // If the function is an inherit type it will have a field as
    // the first parameter and we can use that to get the type.
    if (firstArg && FIELDS.hasOwnProperty(firstArg)) {
        return FIELDS[firstArg];
    }
    else if (firstArg && isMeasurement(firstArg)) {
        return measurementType(firstArg);
    }
    return null;
}
/**
 * Get the multi-series chart type for an aggregate function.
 */
export function aggregateMultiPlotType(field) {
    var matches = AGGREGATE_PATTERN.exec(field);
    // Handle invalid data.
    if (!matches) {
        return 'area';
    }
    var funcName = matches[1];
    if (!AGGREGATIONS.hasOwnProperty(funcName)) {
        return 'area';
    }
    return AGGREGATIONS[funcName].multiPlotType;
}
function validateForNumericAggregate(validColumnTypes) {
    return function (_a) {
        var name = _a.name, dataType = _a.dataType;
        // these built-in columns cannot be applied to numeric aggregates such as percentile(...)
        if ([
            FieldKey.DEVICE_BATTERY_LEVEL,
            FieldKey.STACK_COLNO,
            FieldKey.STACK_LINENO,
            FieldKey.STACK_STACK_LEVEL,
        ].includes(name)) {
            return false;
        }
        return validColumnTypes.includes(dataType);
    };
}
//# sourceMappingURL=fields.jsx.map