import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import capitalize from 'lodash/capitalize';
import { tct } from 'app/locale';
import { IconMute, IconStar } from 'app/icons';
import EventOrGroupTitle from 'app/components/eventOrGroupTitle';
import Tooltip from 'app/components/tooltip';
import { getMessage, getLocation } from 'app/utils/events';
import withOrganization from 'app/utils/withOrganization';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import UnhandledTag, { TagAndMessageWrapper, } from 'app/views/organizationGroupDetails/unhandledTag';
/**
 * Displays an event or group/issue title (i.e. in Stream)
 */
var EventOrGroupHeader = /** @class */ (function (_super) {
    __extends(EventOrGroupHeader, _super);
    function EventOrGroupHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOrGroupHeader.prototype.getTitleChildren = function () {
        var _a = this.props, hideIcons = _a.hideIcons, hideLevel = _a.hideLevel, data = _a.data;
        var _b = data, level = _b.level, status = _b.status, isBookmarked = _b.isBookmarked, hasSeen = _b.hasSeen;
        return (<React.Fragment>
        {!hideLevel && level && (<GroupLevel level={level}>
            <Tooltip title={"Error level: " + capitalize(level)}>
              <span />
            </Tooltip>
          </GroupLevel>)}
        {!hideIcons && status === 'ignored' && (<IconWrapper>
            <IconMute color="red300"/>
          </IconWrapper>)}
        {!hideIcons && isBookmarked && (<IconWrapper>
            <IconStar isSolid color="yellow300"/>
          </IconWrapper>)}
        <EventOrGroupTitle {...this.props} style={{ fontWeight: hasSeen ? 400 : 600 }}/>
      </React.Fragment>);
    };
    EventOrGroupHeader.prototype.getTitle = function () {
        var _a = this.props, includeLink = _a.includeLink, data = _a.data, params = _a.params, location = _a.location;
        var orgId = params === null || params === void 0 ? void 0 : params.orgId;
        var _b = data, id = _b.id, status = _b.status;
        var _c = data, eventID = _c.eventID, groupID = _c.groupID;
        var props = {
            'data-test-id': status === 'resolved' ? 'resolved-issue' : null,
            style: status === 'resolved' ? { textDecoration: 'line-through' } : undefined,
        };
        if (includeLink) {
            return (<GlobalSelectionLink {...props} to={{
                pathname: "/organizations/" + orgId + "/issues/" + (eventID ? groupID : id) + "/" + (eventID ? "events/" + eventID + "/" : ''),
                query: __assign(__assign({ query: this.props.query }, (location.query.sort !== undefined ? { sort: location.query.sort } : {})), (location.query.project !== undefined ? {} : { _allp: 1 })),
            }}>
          {this.getTitleChildren()}
        </GlobalSelectionLink>);
        }
        else {
            return <span {...props}>{this.getTitleChildren()}</span>;
        }
    };
    EventOrGroupHeader.prototype.render = function () {
        var _a = this.props, className = _a.className, size = _a.size, data = _a.data, organization = _a.organization;
        var location = getLocation(data);
        var message = getMessage(data);
        var isUnhandled = data.isUnhandled;
        var orgFeatures = new Set(organization.features);
        var showUnhandled = isUnhandled && !orgFeatures.has('inbox');
        return (<div className={className} data-test-id="event-issue-header">
        <Title size={size}>{this.getTitle()}</Title>
        {location && <Location size={size}>{location}</Location>}
        {(message || showUnhandled) && (<StyledTagAndMessageWrapper size={size}>
            {showUnhandled && <UnhandledTag />}
            {message && <Message>{message}</Message>}
          </StyledTagAndMessageWrapper>)}
      </div>);
    };
    EventOrGroupHeader.defaultProps = {
        includeLink: true,
        size: 'normal',
    };
    return EventOrGroupHeader;
}(React.Component));
var truncateStyles = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: hidden;\n  max-width: 100%;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n"], ["\n  overflow: hidden;\n  max-width: 100%;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n"])));
var getMargin = function (_a) {
    var size = _a.size;
    if (size === 'small') {
        return 'margin: 0;';
    }
    return 'margin: 0 0 5px';
};
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  ", ";\n  & em {\n    font-size: ", ";\n    font-style: normal;\n    font-weight: 300;\n    color: ", ";\n  }\n"], ["\n  ", ";\n  ", ";\n  & em {\n    font-size: ", ";\n    font-style: normal;\n    font-weight: 300;\n    color: ", ";\n  }\n"])), truncateStyles, getMargin, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
var LocationWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  ", ";\n  direction: rtl;\n  text-align: left;\n  font-size: ", ";\n  color: ", ";\n  span {\n    direction: ltr;\n  }\n"], ["\n  ", ";\n  ", ";\n  direction: rtl;\n  text-align: left;\n  font-size: ", ";\n  color: ", ";\n  span {\n    direction: ltr;\n  }\n"])), truncateStyles, getMargin, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
function Location(props) {
    var children = props.children, rest = __rest(props, ["children"]);
    return (<LocationWrapper {...rest}>
      {tct('in [location]', {
        location: <span>{children}</span>,
    })}
    </LocationWrapper>);
}
var StyledTagAndMessageWrapper = styled(TagAndMessageWrapper)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), getMargin);
var Message = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n  font-size: ", ";\n"], ["\n  ", ";\n  font-size: ", ";\n"])), truncateStyles, function (p) { return p.theme.fontSizeMedium; });
var IconWrapper = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: relative;\n  top: 2px;\n\n  margin-right: 5px;\n"], ["\n  position: relative;\n  top: 2px;\n\n  margin-right: 5px;\n"])));
var GroupLevel = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: absolute;\n  left: -1px;\n  width: 9px;\n  height: 15px;\n  border-radius: 0 3px 3px 0;\n\n  background-color: ", ";\n\n  & span {\n    display: block;\n    width: 9px;\n    height: 15px;\n  }\n"], ["\n  position: absolute;\n  left: -1px;\n  width: 9px;\n  height: 15px;\n  border-radius: 0 3px 3px 0;\n\n  background-color: ",
    ";\n\n  & span {\n    display: block;\n    width: 9px;\n    height: 15px;\n  }\n"])), function (p) {
    switch (p.level) {
        case 'sample':
            return p.theme.purple300;
        case 'info':
            return p.theme.blue300;
        case 'warning':
            return p.theme.yellow300;
        case 'error':
            return p.theme.orange400;
        case 'fatal':
            return p.theme.red300;
        default:
            return p.theme.gray300;
    }
});
export default withRouter(withOrganization(EventOrGroupHeader));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=eventOrGroupHeader.jsx.map