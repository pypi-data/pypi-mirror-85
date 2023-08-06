import { __assign } from "tslib";
import { IS_ACCEPTANCE_TEST } from 'app/constants';
/**
 * Use with a framer-motion transition to disable the animation in testing
 * environments.
 *
 * If your animation has no transition you can simply specify
 *
 * ```tsx
 * Component.defaultProps = {
 *   transition: testableTransition(),
 * }
 * ```
 *
 * This function simply disables the animation `type`.
 */
var testableTransition = !IS_ACCEPTANCE_TEST
    ? function (t) { return t; }
    : function (transition) {
        return __assign(__assign({}, transition), { delay: 0, staggerChildren: 0, type: false });
    };
export default testableTransition;
//# sourceMappingURL=testableTransition.jsx.map