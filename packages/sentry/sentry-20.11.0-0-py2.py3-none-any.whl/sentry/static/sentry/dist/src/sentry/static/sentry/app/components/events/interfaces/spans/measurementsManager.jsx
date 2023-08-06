import { __extends } from "tslib";
import React from 'react';
var MeasurementsManagerContext = React.createContext({
    hoveringMeasurement: function () { },
    notHovering: function () { },
    currentHoveredMeasurement: undefined,
});
var Provider = /** @class */ (function (_super) {
    __extends(Provider, _super);
    function Provider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            currentHoveredMeasurement: undefined,
        };
        _this.hoveringMeasurement = function (measurementName) {
            _this.setState({
                currentHoveredMeasurement: measurementName,
            });
        };
        _this.notHovering = function () {
            _this.setState({
                currentHoveredMeasurement: undefined,
            });
        };
        return _this;
    }
    Provider.prototype.render = function () {
        var childrenProps = {
            hoveringMeasurement: this.hoveringMeasurement,
            notHovering: this.notHovering,
            currentHoveredMeasurement: this.state.currentHoveredMeasurement,
        };
        return (<MeasurementsManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </MeasurementsManagerContext.Provider>);
    };
    return Provider;
}(React.Component));
export { Provider };
export var Consumer = MeasurementsManagerContext.Consumer;
//# sourceMappingURL=measurementsManager.jsx.map