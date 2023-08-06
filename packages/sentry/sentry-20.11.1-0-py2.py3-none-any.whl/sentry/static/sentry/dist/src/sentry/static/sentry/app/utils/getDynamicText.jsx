import { IS_ACCEPTANCE_TEST } from 'app/constants';
// Return a specified "fixed" string when we are in a testing environment
// (more specifically, when IS_ACCEPTANCE_TEST is true)
export default function getDynamicText(_a) {
    var value = _a.value, fixed = _a.fixed;
    return IS_ACCEPTANCE_TEST ? fixed : value;
}
//# sourceMappingURL=getDynamicText.jsx.map