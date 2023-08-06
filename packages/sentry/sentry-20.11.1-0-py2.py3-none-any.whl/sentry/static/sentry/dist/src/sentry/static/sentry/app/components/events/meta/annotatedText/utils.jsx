import { t } from 'app/locale';
var REMARKS = {
    a: 'Annotated',
    x: 'Removed',
    s: 'Replaced',
    m: 'Masked',
    p: 'Pseudonymized',
    e: 'Encrypted',
};
var KNOWN_RULES = {
    '!limit': 'size limits',
    '!raw': 'raw payload',
    '!config': 'SDK configuration',
};
export function getTooltipText(_a) {
    var _b = _a.remark, remark = _b === void 0 ? '' : _b, _c = _a.rule_id, rule = _c === void 0 ? '' : _c;
    var remark_title = REMARKS[remark];
    var rule_title = KNOWN_RULES[rule] || t('PII rule "%s"', rule);
    if (remark_title) {
        return t('%s because of %s', remark_title, rule_title);
    }
    return rule_title;
}
//# sourceMappingURL=utils.jsx.map