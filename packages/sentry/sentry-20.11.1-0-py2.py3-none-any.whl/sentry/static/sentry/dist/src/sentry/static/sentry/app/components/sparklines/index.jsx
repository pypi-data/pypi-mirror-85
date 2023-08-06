import { __extends } from "tslib";
import { Sparklines } from 'react-sparklines';
import PropTypes from 'prop-types';
/**
 * This is required because:
 *
 * - React.Suspense only works with default exports
 * - typescript complains that the library's `propTypes` does not
 * have `children defined.
 * - typescript also won't let us access `Sparklines.propTypes`
 */
var SparklinesWithCustomPropTypes = /** @class */ (function (_super) {
    __extends(SparklinesWithCustomPropTypes, _super);
    function SparklinesWithCustomPropTypes() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SparklinesWithCustomPropTypes.propTypes = {
        children: PropTypes.node,
        data: PropTypes.array,
        limit: PropTypes.number,
        width: PropTypes.number,
        height: PropTypes.number,
        svgWidth: PropTypes.number,
        svgHeight: PropTypes.number,
        preserveAspectRatio: PropTypes.string,
        margin: PropTypes.number,
        style: PropTypes.object,
        min: PropTypes.number,
        max: PropTypes.number,
        onMouseMove: PropTypes.func,
    };
    return SparklinesWithCustomPropTypes;
}(Sparklines));
export default SparklinesWithCustomPropTypes;
//# sourceMappingURL=index.jsx.map