import { __read } from "tslib";
/**
 * Given a list of rule objects returned from the API, locate the matching
 * rules for a specific owner.
 */
function findMatchedRules(rules, owner) {
    if (!rules) {
        return undefined;
    }
    var matchOwner = function (actorType, key) {
        return (actorType === 'user' && key === owner.email) ||
            (actorType === 'team' && key === owner.name);
    };
    var actorHasOwner = function (_a) {
        var _b = __read(_a, 2), actorType = _b[0], key = _b[1];
        return actorType === owner.type && matchOwner(actorType, key);
    };
    return rules
        .filter(function (_a) {
        var _b = __read(_a, 2), _ = _b[0], ruleActors = _b[1];
        return ruleActors.find(actorHasOwner);
    })
        .map(function (_a) {
        var _b = __read(_a, 1), rule = _b[0];
        return rule;
    });
}
export { findMatchedRules };
//# sourceMappingURL=findMatchedRules.jsx.map