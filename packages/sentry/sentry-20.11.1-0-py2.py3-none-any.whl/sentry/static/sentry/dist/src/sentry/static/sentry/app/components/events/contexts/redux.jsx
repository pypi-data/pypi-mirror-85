import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import ClippedBox from 'app/components/clippedBox';
var ReduxContextType = /** @class */ (function (_super) {
    __extends(ReduxContextType, _super);
    function ReduxContextType() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReduxContextType.prototype.getKnownData = function () {
        return [
            {
                key: 'value',
                subject: t('Latest State'),
                value: this.props.data,
            },
        ];
    };
    ReduxContextType.prototype.render = function () {
        return (<ClippedBox clipHeight={250}>
        <ContextBlock data={this.getKnownData()}/>
      </ClippedBox>);
    };
    return ReduxContextType;
}(React.Component));
export default ReduxContextType;
//# sourceMappingURL=redux.jsx.map