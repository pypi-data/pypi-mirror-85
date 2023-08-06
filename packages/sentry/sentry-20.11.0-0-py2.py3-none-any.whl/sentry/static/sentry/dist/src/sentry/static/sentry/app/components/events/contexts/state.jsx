import { __extends, __read } from "tslib";
import React from 'react';
import upperFirst from 'lodash/upperFirst';
import { t } from 'app/locale';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import ClippedBox from 'app/components/clippedBox';
import { getMeta } from 'app/components/events/meta/metaProxy';
var StateContextType = /** @class */ (function (_super) {
    __extends(StateContextType, _super);
    function StateContextType() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StateContextType.prototype.getStateTitle = function (name, type) {
        return "" + name + (type ? " (" + upperFirst(type) + ")" : '');
    };
    StateContextType.prototype.getKnownData = function () {
        var primaryState = this.props.data.state;
        if (!primaryState) {
            return [];
        }
        return [
            {
                key: 'state',
                subject: this.getStateTitle(t('State'), primaryState.type),
                value: primaryState.value,
            },
        ];
    };
    StateContextType.prototype.getUnknownData = function () {
        var _this = this;
        var data = this.props.data;
        return Object.entries(data)
            .filter(function (_a) {
            var _b = __read(_a, 1), key = _b[0];
            return !['type', 'title', 'state'].includes(key);
        })
            .map(function (_a) {
            var _b = __read(_a, 2), name = _b[0], state = _b[1];
            return ({
                key: name,
                value: state.value,
                subject: _this.getStateTitle(name, state.type),
                meta: getMeta(data, name),
            });
        });
    };
    StateContextType.prototype.render = function () {
        return (<ClippedBox clipHeight={250}>
        <ContextBlock data={this.getKnownData()}/>
        <ContextBlock data={this.getUnknownData()}/>
      </ClippedBox>);
    };
    return StateContextType;
}(React.Component));
export default StateContextType;
//# sourceMappingURL=state.jsx.map