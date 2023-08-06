import { __read, __values } from "tslib";
import { RuleType, MethodType } from './types';
// Remap PII config format to something that is more usable in React. Ideally
// we would stop doing this at some point and make some updates to how we
// store this configuration on the server.
//
// For the time being the PII config format is documented at
// https://getsentry.github.io/relay/pii-config/
function convertRelayPiiConfig(relayPiiConfig) {
    var e_1, _a;
    var piiConfig = relayPiiConfig ? JSON.parse(relayPiiConfig) : {};
    var rules = piiConfig.rules || {};
    var applications = piiConfig.applications || {};
    var convertedRules = [];
    for (var application in applications) {
        try {
            for (var _b = (e_1 = void 0, __values(applications[application])), _c = _b.next(); !_c.done; _c = _b.next()) {
                var rule = _c.value;
                var resolvedRule = rules[rule];
                var id = convertedRules.length;
                var source = application;
                if (!resolvedRule) {
                    // Convert a "built-in" rule like "@anything:remove" to an object {
                    //   type: "anything",
                    //   method: "remove"
                    // }
                    if (rule[0] === '@') {
                        var typeAndMethod = rule.slice(1).split(':');
                        var _d = __read(typeAndMethod, 1), type_1 = _d[0];
                        var _e = __read(typeAndMethod, 2), method_1 = _e[1];
                        if (type_1 === 'urlauth')
                            type_1 = 'url_auth';
                        if (type_1 === 'usssn')
                            type_1 = 'us_ssn';
                        convertedRules.push({
                            id: id,
                            method: method_1,
                            type: type_1,
                            source: source,
                        });
                    }
                    continue;
                }
                var type = resolvedRule.type, redaction = resolvedRule.redaction;
                var method = redaction.method;
                if (method === MethodType.REPLACE && resolvedRule.type === RuleType.PATTERN) {
                    convertedRules.push({
                        id: id,
                        method: MethodType.REPLACE,
                        type: RuleType.PATTERN,
                        source: source,
                        placeholder: redaction === null || redaction === void 0 ? void 0 : redaction.text,
                        pattern: resolvedRule.pattern,
                    });
                    continue;
                }
                if (method === MethodType.REPLACE) {
                    convertedRules.push({
                        id: id,
                        method: MethodType.REPLACE,
                        type: type,
                        source: source,
                        placeholder: redaction === null || redaction === void 0 ? void 0 : redaction.text,
                    });
                    continue;
                }
                if (resolvedRule.type === RuleType.PATTERN) {
                    convertedRules.push({
                        id: id,
                        method: method,
                        type: RuleType.PATTERN,
                        source: source,
                        pattern: resolvedRule.pattern,
                    });
                    continue;
                }
                convertedRules.push({ id: id, method: method, type: type, source: source });
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    return convertedRules;
}
export default convertRelayPiiConfig;
//# sourceMappingURL=convertRelayPiiConfig.jsx.map