import { RuleType, MethodType } from './types';
function getSubmitFormatRule(rule) {
    if (rule.type === RuleType.PATTERN && rule.method === MethodType.REPLACE) {
        return {
            type: rule.type,
            pattern: rule.pattern,
            redaction: {
                method: rule.method,
                text: rule === null || rule === void 0 ? void 0 : rule.placeholder,
            },
        };
    }
    if (rule.type === RuleType.PATTERN) {
        return {
            type: rule.type,
            pattern: rule.pattern,
            redaction: {
                method: rule.method,
            },
        };
    }
    if (rule.method === MethodType.REPLACE) {
        return {
            type: rule.type,
            redaction: {
                method: rule.method,
                text: rule === null || rule === void 0 ? void 0 : rule.placeholder,
            },
        };
    }
    return {
        type: rule.type,
        redaction: {
            method: rule.method,
        },
    };
}
function submitRules(api, endpoint, rules) {
    var applications = {};
    var submitFormatRules = {};
    for (var i = 0; i < rules.length; i++) {
        var rule = rules[i];
        var ruleId = String(i);
        submitFormatRules[ruleId] = getSubmitFormatRule(rule);
        if (!applications[rule.source]) {
            applications[rule.source] = [];
        }
        if (!applications[rule.source].includes(ruleId)) {
            applications[rule.source].push(ruleId);
        }
    }
    var piiConfig = { rules: submitFormatRules, applications: applications };
    return api.requestPromise(endpoint, {
        method: 'PUT',
        data: { relayPiiConfig: JSON.stringify(piiConfig) },
    });
}
export default submitRules;
//# sourceMappingURL=submitRules.jsx.map