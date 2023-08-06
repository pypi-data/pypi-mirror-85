import { __read, __spread } from "tslib";
// Checks if `fn` is a function and calls it with `args`
export function callIfFunction(fn) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    return typeof fn === 'function' && fn.apply(void 0, __spread(args));
}
//# sourceMappingURL=callIfFunction.jsx.map