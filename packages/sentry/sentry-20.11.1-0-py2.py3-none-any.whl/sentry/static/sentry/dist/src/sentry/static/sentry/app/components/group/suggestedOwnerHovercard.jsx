import { __extends, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import moment from 'moment';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import Hovercard from 'app/components/hovercard';
import { IconCommit, IconWarning } from 'app/icons';
import Link from 'app/components/links/link';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { defined } from 'app/utils';
var SuggestedOwnerHovercard = /** @class */ (function (_super) {
    __extends(SuggestedOwnerHovercard, _super);
    function SuggestedOwnerHovercard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            commitsExpanded: false,
            rulesExpanded: false,
        };
        return _this;
    }
    SuggestedOwnerHovercard.prototype.render = function () {
        var _this = this;
        var _a = this.props, actor = _a.actor, commits = _a.commits, rules = _a.rules, props = __rest(_a, ["actor", "commits", "rules"]);
        var _b = this.state, commitsExpanded = _b.commitsExpanded, rulesExpanded = _b.rulesExpanded;
        return (<Hovercard header={<React.Fragment>
            <HovercardHeader>
              <HovercardActorAvatar actor={actor}/>
              {actor.name || actor.email}
            </HovercardHeader>
            {actor.id === undefined && (<EmailAlert icon={<IconWarning size="xs"/>} type="warning">
                {tct('The email [actorEmail] is not a member of your organization. [inviteUser:Invite] them or link additional emails in [accountSettings:account settings].', {
            actorEmail: <strong>{actor.email}</strong>,
            accountSettings: <Link to="/settings/account/emails/"/>,
            inviteUser: (<a onClick={function () {
                return openInviteMembersModal({
                    initialData: [
                        {
                            emails: new Set([actor.email]),
                        },
                    ],
                    source: 'suggested_assignees',
                });
            }}/>),
        })}
              </EmailAlert>)}
          </React.Fragment>} body={<HovercardBody>
            {commits !== undefined && (<React.Fragment>
                <div className="divider">
                  <h6>{t('Commits')}</h6>
                </div>
                <div>
                  {commits
            .slice(0, commitsExpanded ? commits.length : 3)
            .map(function (_a, i) {
            var message = _a.message, dateCreated = _a.dateCreated;
            return (<CommitReasonItem key={i}>
                        <CommitIcon />
                        <CommitMessage message={message} date={dateCreated}/>
                      </CommitReasonItem>);
        })}
                </div>
                {commits.length > 3 && !commitsExpanded ? (<ViewMoreButton onClick={function () { return _this.setState({ commitsExpanded: true }); }}/>) : null}
              </React.Fragment>)}
            {defined(rules) && (<React.Fragment>
                <div className="divider">
                  <h6>{t('Matching Ownership Rules')}</h6>
                </div>
                <div>
                  {rules
            .slice(0, rulesExpanded ? rules.length : 3)
            .map(function (_a, i) {
            var _b = __read(_a, 2), type = _b[0], matched = _b[1];
            return (<RuleReasonItem key={i}>
                        <OwnershipTag tagType={type}/>
                        <OwnershipValue>{matched}</OwnershipValue>
                      </RuleReasonItem>);
        })}
                </div>
                {rules.length > 3 && !rulesExpanded ? (<ViewMoreButton onClick={function () { return _this.setState({ rulesExpanded: true }); }}/>) : null}
              </React.Fragment>)}
          </HovercardBody>} {...props}/>);
    };
    return SuggestedOwnerHovercard;
}(React.Component));
var tagColors = {
    url: theme.green200,
    path: theme.purple300,
    tag: theme.blue300,
};
var CommitIcon = styled(function (p) { return <IconCommit {...p}/>; })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n  flex-shrink: 0;\n"], ["\n  margin-right: ", ";\n  flex-shrink: 0;\n"])), space(0.5));
var CommitMessage = styled(function (_a) {
    var _b = _a.message, message = _b === void 0 ? '' : _b, date = _a.date, props = __rest(_a, ["message", "date"]);
    return (<div {...props}>
    {message.split('\n')[0]}
    <CommitDate date={date}/>
  </div>);
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-top: ", ";\n  hyphens: auto;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-top: ", ";\n  hyphens: auto;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeExtraSmall; }, space(0.25));
var CommitDate = styled(function (_a) {
    var date = _a.date, props = __rest(_a, ["date"]);
    return (<div {...props}>{moment(date).fromNow()}</div>);
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  margin-top: ", ";\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.gray300; });
var CommitReasonItem = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space(1));
var RuleReasonItem = styled('code')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space(1));
var OwnershipTag = styled(function (_a) {
    var tagType = _a.tagType, props = __rest(_a, ["tagType"]);
    return <div {...props}>{tagType}</div>;
})(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  border-radius: 2px;\n  font-weight: bold;\n  min-width: 34px;\n  text-align: center;\n"], ["\n  background: ", ";\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  border-radius: 2px;\n  font-weight: bold;\n  min-width: 34px;\n  text-align: center;\n"])), function (p) { return tagColors[p.tagType.indexOf('tags') === -1 ? p.tagType : 'tag']; }, function (p) { return p.theme.white; }, function (p) { return p.theme.fontSizeExtraSmall; }, space(0.25), space(0.5), space(0.25), space(0.5), space(0.25));
var ViewMoreButton = styled(function (p) { return (<Button {...p} priority="link" size="zero">
    {t('View more')}
  </Button>); })(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  border: none;\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  width: 100%;\n  min-width: 34px;\n"], ["\n  border: none;\n  color: ", ";\n  font-size: ", ";\n  padding: ", " ", ";\n  margin: ", " ", " ", " 0;\n  width: 100%;\n  min-width: 34px;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeExtraSmall; }, space(0.25), space(0.5), space(1), space(0.25), space(0.25));
var OwnershipValue = styled('code')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  word-break: break-all;\n  line-height: 1.2;\n"], ["\n  word-break: break-all;\n  line-height: 1.2;\n"])));
var EmailAlert = styled(function (p) { return <Alert iconSize="16px" {...p}/>; })(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin: 10px -13px -13px;\n  border-radius: 0;\n  border-color: #ece0b0;\n  padding: 10px;\n  font-size: ", ";\n  font-weight: normal;\n  box-shadow: none;\n"], ["\n  margin: 10px -13px -13px;\n  border-radius: 0;\n  border-color: #ece0b0;\n  padding: 10px;\n  font-size: ", ";\n  font-weight: normal;\n  box-shadow: none;\n"])), function (p) { return p.theme.fontSizeSmall; });
var HovercardHeader = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var HovercardActorAvatar = styled(function (p) { return (<ActorAvatar size={20} hasTooltip={false} {...p}/>); })(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var HovercardBody = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-top: -", ";\n"], ["\n  margin-top: -", ";\n"])), space(2));
export default SuggestedOwnerHovercard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=suggestedOwnerHovercard.jsx.map