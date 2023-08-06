import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Avatar from 'app/components/avatar';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var BaseBadge = React.memo(function (_a) {
    var displayName = _a.displayName, _b = _a.hideName, hideName = _b === void 0 ? false : _b, _c = _a.hideAvatar, hideAvatar = _c === void 0 ? false : _c, _d = _a.avatarProps, avatarProps = _d === void 0 ? {} : _d, _e = _a.avatarSize, avatarSize = _e === void 0 ? 24 : _e, description = _a.description, team = _a.team, organization = _a.organization, project = _a.project, className = _a.className;
    return (<Wrapper className={className}>
      {!hideAvatar && (<StyledAvatar {...avatarProps} size={avatarSize} hideName={hideName} team={team} organization={organization} project={project}/>)}

      {(!hideName || !!description) && (<DisplayNameAndDescription>
          {!hideName && (<DisplayName data-test-id="badge-display-name">{displayName}</DisplayName>)}
          {!!description && <Description>{description}</Description>}
        </DisplayNameAndDescription>)}
    </Wrapper>);
});
export default BaseBadge;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledAvatar = styled(Avatar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n  flex-shrink: 0;\n"], ["\n  margin-right: ", ";\n  flex-shrink: 0;\n"])), function (p) { return (p.hideName ? 0 : space(1)); });
var DisplayNameAndDescription = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  line-height: 1;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex-direction: column;\n  line-height: 1;\n  overflow: hidden;\n"])));
var DisplayName = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  line-height: 1.2;\n"], ["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  line-height: 1.2;\n"])));
var Description = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  line-height: 14px;\n  ", ";\n"], ["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  line-height: 14px;\n  ", ";\n"])), space(0.25), function (p) { return p.theme.gray300; }, overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=baseBadge.jsx.map