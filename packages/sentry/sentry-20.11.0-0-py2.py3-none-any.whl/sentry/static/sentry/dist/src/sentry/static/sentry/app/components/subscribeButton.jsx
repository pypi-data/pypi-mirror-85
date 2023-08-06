import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import Button from 'app/components/button';
import { t } from 'app/locale';
import { IconBell } from 'app/icons';
var SubscribeButton = /** @class */ (function (_super) {
    __extends(SubscribeButton, _super);
    function SubscribeButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SubscribeButton.prototype.render = function () {
        var _a = this.props, size = _a.size, isSubscribed = _a.isSubscribed, onClick = _a.onClick, disabled = _a.disabled;
        var icon = <IconBell color={isSubscribed ? 'blue300' : undefined}/>;
        return (<Button size={size} icon={icon} onClick={onClick} disabled={disabled}>
        {isSubscribed ? t('Unsubscribe') : t('Subscribe')}
      </Button>);
    };
    SubscribeButton.propTypes = {
        isSubscribed: PropTypes.bool,
        onClick: PropTypes.func.isRequired,
        disabled: PropTypes.bool,
        // `Object is possibly 'undefined'` if we try to use Button.propTypes.size
        size: PropTypes.any,
    };
    return SubscribeButton;
}(React.Component));
export default SubscribeButton;
//# sourceMappingURL=subscribeButton.jsx.map