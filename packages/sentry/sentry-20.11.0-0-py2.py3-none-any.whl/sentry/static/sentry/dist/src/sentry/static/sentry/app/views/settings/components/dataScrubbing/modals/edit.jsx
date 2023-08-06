import { __assign, __rest } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import ModalManager from './modalManager';
var Edit = function (_a) {
    var savedRules = _a.savedRules, rule = _a.rule, props = __rest(_a, ["savedRules", "rule"]);
    var handleGetNewRules = function (values) {
        var updatedRule = __assign(__assign({}, values), { id: rule.id });
        var newRules = savedRules.map(function (savedRule) {
            if (savedRule.id === updatedRule.id) {
                return updatedRule;
            }
            return savedRule;
        });
        return newRules;
    };
    return (<ModalManager {...props} savedRules={savedRules} title={t('Edit an advanced data scrubbing rule')} initialState={rule} onGetNewRules={handleGetNewRules}/>);
};
export default Edit;
//# sourceMappingURL=edit.jsx.map