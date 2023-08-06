import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import { SectionHeading } from 'app/components/charts/styles';
import { IconWarning } from 'app/icons';
import GroupChart from 'app/components/stream/groupChart';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import SeenByList from 'app/components/seenByList';
import ShortId from 'app/components/shortId';
import Times from 'app/components/group/times';
import space from 'app/styles/space';
var LinkedIssue = /** @class */ (function (_super) {
    __extends(LinkedIssue, _super);
    function LinkedIssue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LinkedIssue.prototype.getEndpoints = function () {
        var groupId = this.props.groupId;
        var groupUrl = "/issues/" + groupId + "/";
        return [['group', groupUrl]];
    };
    LinkedIssue.prototype.renderLoading = function () {
        return <Placeholder height="120px" bottomGutter={2}/>;
    };
    LinkedIssue.prototype.renderError = function (error, disableLog, disableReport) {
        if (disableLog === void 0) { disableLog = false; }
        if (disableReport === void 0) { disableReport = false; }
        var errors = this.state.errors;
        var hasNotFound = Object.values(errors).find(function (resp) { return resp && resp.status === 404; });
        if (hasNotFound) {
            return (<Alert type="warning" icon={<IconWarning size="md"/>}>
          {t('The linked issue cannot be found. It may have been deleted, or merged.')}
        </Alert>);
        }
        return _super.prototype.renderError.call(this, error, disableLog, disableReport);
    };
    LinkedIssue.prototype.renderBody = function () {
        var eventId = this.props.eventId;
        var group = this.state.group;
        var issueUrl = group.permalink + "events/" + eventId + "/";
        return (<Section>
        <SectionHeading>{t('Event Issue')}</SectionHeading>
        <StyledIssueCard>
          <IssueCardHeader>
            <StyledLink to={issueUrl} data-test-id="linked-issue">
              <StyledShortId shortId={group.shortId} avatar={<ProjectBadge project={group.project} avatarSize={16} hideName/>}/>
            </StyledLink>
            <StyledSeenByList seenBy={group.seenBy} maxVisibleAvatars={5}/>
          </IssueCardHeader>
          <IssueCardBody>
            <GroupChart statsPeriod="30d" data={group} height={56}/>
          </IssueCardBody>
          <IssueCardFooter>
            <Times lastSeen={group.lastSeen} firstSeen={group.firstSeen}/>
          </IssueCardFooter>
        </StyledIssueCard>
      </Section>);
    };
    LinkedIssue.propTypes = {
        groupId: PropTypes.string.isRequired,
        eventId: PropTypes.string.isRequired,
    };
    return LinkedIssue;
}(AsyncComponent));
var Section = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var StyledIssueCard = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  border-radius: ", ";\n"], ["\n  border: 1px solid ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var IssueCardHeader = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"])), space(1));
var StyledLink = styled(Link)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
var IssueCardBody = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  background: ", ";\n  padding-top: ", ";\n"], ["\n  background: ", ";\n  padding-top: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, space(1));
var StyledSeenByList = styled(SeenByList)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var StyledShortId = styled(ShortId)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.textColor; });
var IssueCardFooter = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space(0.5), space(1));
export default LinkedIssue;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=linkedIssue.jsx.map