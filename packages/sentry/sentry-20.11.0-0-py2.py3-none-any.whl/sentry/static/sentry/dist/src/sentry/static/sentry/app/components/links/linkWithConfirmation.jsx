import { __extends, __rest } from "tslib";
import React from 'react';
import classNames from 'classnames';
import Confirm from 'app/components/confirm';
/**
 * <Confirm> is a more generic version of this component
 */
var LinkWithConfirmation = /** @class */ (function (_super) {
    __extends(LinkWithConfirmation, _super);
    function LinkWithConfirmation() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LinkWithConfirmation.prototype.render = function () {
        var _a = this.props, className = _a.className, disabled = _a.disabled, title = _a.title, children = _a.children, otherProps = __rest(_a, ["className", "disabled", "title", "children"]);
        return (<Confirm {...otherProps} disabled={disabled}>
        <a href="#" className={classNames(className || '', { disabled: disabled })} title={title}>
          {children}
        </a>
      </Confirm>);
    };
    return LinkWithConfirmation;
}(React.PureComponent));
export default LinkWithConfirmation;
//# sourceMappingURL=linkWithConfirmation.jsx.map