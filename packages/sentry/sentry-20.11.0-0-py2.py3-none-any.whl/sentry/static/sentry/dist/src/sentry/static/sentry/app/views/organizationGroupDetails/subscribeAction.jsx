import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import SentryTypes from 'app/sentryTypes';
import { IconBell } from 'app/icons';
import { t } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import { getSubscriptionReason } from './utils';
var SubscribeAction = function (_a) {
    var group = _a.group, onClick = _a.onClick;
    var canChangeSubscriptionState = function () {
        var _a, _b;
        return !((_b = (_a = group.subscriptionDetails) === null || _a === void 0 ? void 0 : _a.disabled) !== null && _b !== void 0 ? _b : false);
    };
    var subscribedClassName = "group-subscribe btn btn-default btn-sm" + (group.isSubscribed ? ' active' : '');
    return (canChangeSubscriptionState() && (<div className="btn-group">
        <Tooltip title={getSubscriptionReason(group, true)}>
          <div className={subscribedClassName} title={t('Subscribe')} onClick={onClick}>
            <IconWrapper>
              <IconBell size="xs"/>
            </IconWrapper>
          </div>
        </Tooltip>
      </div>));
};
SubscribeAction.propTypes = {
    group: SentryTypes.Group.isRequired,
    onClick: PropTypes.func.isRequired,
};
export default SubscribeAction;
var IconWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var templateObject_1;
//# sourceMappingURL=subscribeAction.jsx.map