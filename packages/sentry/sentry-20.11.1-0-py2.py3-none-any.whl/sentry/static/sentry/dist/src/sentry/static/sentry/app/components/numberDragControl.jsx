import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconArrow } from 'app/icons';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
var NumberDragControl = /** @class */ (function (_super) {
    __extends(NumberDragControl, _super);
    function NumberDragControl() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isClicked: false,
        };
        return _this;
    }
    NumberDragControl.prototype.render = function () {
        var _this = this;
        var _a = this.props, onChange = _a.onChange, axis = _a.axis, step = _a.step, shiftStep = _a.shiftStep, props = __rest(_a, ["onChange", "axis", "step", "shiftStep"]);
        var isX = (axis !== null && axis !== void 0 ? axis : 'x') === 'x';
        return (<Wrapper {...props} onMouseDown={function (event) {
            if (event.button !== 0) {
                return;
            }
            // XXX(epurkhiser): We can remove this later, just curious if people
            // are actually using the drag control
            trackAnalyticsEvent({
                eventName: 'Number Drag Control: Clicked',
                eventKey: 'number_drag_control.clicked',
            });
            event.currentTarget.requestPointerLock();
            _this.setState({ isClicked: true });
        }} onMouseUp={function () {
            document.exitPointerLock();
            _this.setState({ isClicked: false });
        }} onMouseMove={function (event) {
            var _a;
            if (!_this.state.isClicked) {
                return;
            }
            var delta = isX ? event.movementX : event.movementY * -1;
            var deltaOne = delta > 0 ? Math.ceil(delta / 100) : Math.floor(delta / 100);
            var deltaStep = deltaOne * ((_a = (event.shiftKey ? shiftStep : step)) !== null && _a !== void 0 ? _a : 1);
            onChange(deltaStep, event);
        }} isActive={this.state.isClicked} isX={isX}>
        <IconArrow direction={isX ? 'left' : 'up'} size="8px"/>
        <IconArrow direction={isX ? 'right' : 'down'} size="8px"/>
      </Wrapper>);
    };
    return NumberDragControl;
}(React.Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  padding: ", ";\n  ", ";\n  cursor: ", ";\n  color: ", ";\n  background: ", ";\n  border-radius: 2px;\n"], ["\n  display: grid;\n  padding: ", ";\n  ",
    ";\n  cursor: ", ";\n  color: ", ";\n  background: ", ";\n  border-radius: 2px;\n"])), space(0.5), function (p) {
    return p.isX
        ? 'grid-template-columns: max-content max-content'
        : 'grid-template-rows: max-content max-content';
}, function (p) { return (p.isX ? 'ew-resize' : 'ns-resize'); }, function (p) { return (p.isActive ? p.theme.gray500 : p.theme.gray300); }, function (p) { return p.isActive && p.theme.backgroundSecondary; });
export default NumberDragControl;
var templateObject_1;
//# sourceMappingURL=numberDragControl.jsx.map