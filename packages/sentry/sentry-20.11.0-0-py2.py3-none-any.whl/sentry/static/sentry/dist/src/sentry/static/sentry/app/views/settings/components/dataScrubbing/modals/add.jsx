import { __assign, __read, __rest, __spread } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import ModalManager from './modalManager';
var Add = function (_a) {
    var savedRules = _a.savedRules, props = __rest(_a, ["savedRules"]);
    var handleGetNewRules = function (values) {
        return __spread(savedRules, [__assign(__assign({}, values), { id: savedRules.length })]);
    };
    return (<ModalManager {...props} savedRules={savedRules} title={t('Add an advanced data scrubbing rule')} onGetNewRules={handleGetNewRules}/>);
};
export default Add;
//# sourceMappingURL=add.jsx.map