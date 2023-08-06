import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import SentryTypes from 'app/sentryTypes';
import { nl2br, escape } from 'app/utils';
import { t } from 'app/locale';
import ActivityAuthor from 'app/components/activity/author';
import ActivityItem from 'app/components/activity/item';
import Clipboard from 'app/components/clipboard';
import { IconCopy } from 'app/icons';
import Link from 'app/components/links/link';
import space from 'app/styles/space';
var EventUserFeedback = /** @class */ (function (_super) {
    __extends(EventUserFeedback, _super);
    function EventUserFeedback() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventUserFeedback.prototype.getUrl = function () {
        var _a = this.props, report = _a.report, orgId = _a.orgId, issueId = _a.issueId;
        return "/organizations/" + orgId + "/issues/" + issueId + "/events/" + report.eventID + "/";
    };
    EventUserFeedback.prototype.render = function () {
        var _a = this.props, className = _a.className, report = _a.report;
        var user = report.user || {
            name: report.name,
            email: report.email,
            id: '',
            username: '',
            ip_address: '',
        };
        return (<div className={className}>
        <ActivityItem date={report.dateCreated} author={{ type: 'user', user: user }} header={<div>
              <ActivityAuthor>{report.name}</ActivityAuthor>
              <Clipboard value={report.email}>
                <Email>
                  {report.email}
                  <StyledIconCopy size="xs"/>
                </Email>
              </Clipboard>
              {report.eventID && (<ViewEventLink to={this.getUrl()}>{t('View event')}</ViewEventLink>)}
            </div>}>
          <p dangerouslySetInnerHTML={{
            __html: nl2br(escape(report.comments)),
        }}/>
        </ActivityItem>
      </div>);
    };
    EventUserFeedback.propTypes = {
        report: SentryTypes.UserReport.isRequired,
        orgId: PropTypes.string.isRequired,
        issueId: PropTypes.string.isRequired,
        className: PropTypes.string,
    };
    return EventUserFeedback;
}(React.Component));
export default EventUserFeedback;
var Email = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  cursor: pointer;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  cursor: pointer;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1));
var ViewEventLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: 300;\n  margin-left: ", ";\n  font-size: 0.9em;\n"], ["\n  font-weight: 300;\n  margin-left: ", ";\n  font-size: 0.9em;\n"])), space(1));
var StyledIconCopy = styled(IconCopy)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=userFeedback.jsx.map