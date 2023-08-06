import { __makeTemplateObject } from "tslib";
import React from 'react';
import classNames from 'classnames';
import moment from 'moment';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconShow } from 'app/icons';
import { userDisplayName } from 'app/utils/formatters';
import AvatarList from 'app/components/avatar/avatarList';
import ConfigStore from 'app/stores/configStore';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
var SeenByList = function (_a) {
    var _b = _a.avatarSize, avatarSize = _b === void 0 ? 28 : _b, _c = _a.seenBy, seenBy = _c === void 0 ? [] : _c, _d = _a.iconTooltip, iconTooltip = _d === void 0 ? t('People who have viewed this') : _d, _e = _a.maxVisibleAvatars, maxVisibleAvatars = _e === void 0 ? 10 : _e, _f = _a.iconPosition, iconPosition = _f === void 0 ? 'left' : _f, className = _a.className;
    var activeUser = ConfigStore.get('user');
    var displayUsers = seenBy.filter(function (user) { return activeUser.id !== user.id; });
    if (displayUsers.length === 0) {
        return null;
    }
    // Note className="seen-by" is required for responsive design
    return (<SeenByWrapper iconPosition={iconPosition} className={classNames('seen-by', className)}>
      <AvatarList users={displayUsers} avatarSize={avatarSize} maxVisibleAvatars={maxVisibleAvatars} renderTooltip={function (user) { return (<React.Fragment>
            {userDisplayName(user)}
            <br />
            {moment(user.lastSeen).format('LL')}
          </React.Fragment>); }}/>
      <IconWrapper iconPosition={iconPosition}>
        <Tooltip title={iconTooltip}>
          <IconShow size="sm" color="gray200"/>
        </Tooltip>
      </IconWrapper>
    </SeenByWrapper>);
};
var SeenByWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  margin-top: 15px;\n  float: right;\n  ", ";\n"], ["\n  display: flex;\n  margin-top: 15px;\n  float: right;\n  ", ";\n"])), function (p) { return (p.iconPosition === 'left' ? 'flex-direction: row-reverse' : ''); });
var IconWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background-color: transparent;\n  color: ", ";\n  height: 28px;\n  width: 24px;\n  line-height: 26px;\n  text-align: center;\n  padding-top: ", ";\n  ", ";\n"], ["\n  background-color: transparent;\n  color: ", ";\n  height: 28px;\n  width: 24px;\n  line-height: 26px;\n  text-align: center;\n  padding-top: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, space(0.5), function (p) { return (p.iconPosition === 'left' ? 'margin-right: 10px' : ''); });
export default SeenByList;
var templateObject_1, templateObject_2;
//# sourceMappingURL=seenByList.jsx.map