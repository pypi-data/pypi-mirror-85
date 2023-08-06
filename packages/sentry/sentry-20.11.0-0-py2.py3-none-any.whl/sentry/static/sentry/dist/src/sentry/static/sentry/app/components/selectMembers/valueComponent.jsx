import { __extends } from "tslib";
import React from 'react';
import ActorAvatar from 'app/components/avatar/actorAvatar';
var ValueComponent = /** @class */ (function (_super) {
    __extends(ValueComponent, _super);
    function ValueComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            _this.props.onRemove(_this.props.value);
        };
        return _this;
    }
    ValueComponent.prototype.render = function () {
        return (<a onClick={this.handleClick}>
        <ActorAvatar actor={this.props.value.actor} size={28}/>
      </a>);
    };
    return ValueComponent;
}(React.Component));
export default ValueComponent;
//# sourceMappingURL=valueComponent.jsx.map