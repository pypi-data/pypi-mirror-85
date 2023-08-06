import { __extends, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import { PanelItem } from 'app/components/panels';
import { t, tct } from 'app/locale';
import UserAvatar from 'app/components/avatar/userAvatar';
import CommitLink from 'app/components/commitLink';
import Hovercard from 'app/components/hovercard';
import { IconWarning } from 'app/icons';
import Link from 'app/components/links/link';
import TextOverflow from 'app/components/textOverflow';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
var CommitRow = /** @class */ (function (_super) {
    __extends(CommitRow, _super);
    function CommitRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CommitRow.prototype.renderMessage = function (message) {
        if (!message) {
            return t('No message provided');
        }
        var firstLine = message.split(/\n/)[0];
        return firstLine;
    };
    CommitRow.prototype.renderHovercardBody = function (author) {
        return (<EmailWarning>
        {tct('The email [actorEmail] is not a member of your organization. [inviteUser:Invite] them or link additional emails in [accountSettings:account settings].', {
            actorEmail: <strong>{author.email}</strong>,
            accountSettings: <StyledLink to="/settings/account/emails/"/>,
            inviteUser: (<StyledLink to="" onClick={function () {
                return openInviteMembersModal({
                    initialData: [
                        {
                            emails: new Set([author.email]),
                        },
                    ],
                    source: 'suspect_commit',
                });
            }}/>),
        })}
      </EmailWarning>);
    };
    CommitRow.prototype.render = function () {
        var _a = this.props, commit = _a.commit, customAvatar = _a.customAvatar, props = __rest(_a, ["commit", "customAvatar"]);
        var id = commit.id, dateCreated = commit.dateCreated, message = commit.message, author = commit.author, repository = commit.repository;
        var nonMemberEmail = author && author.id === undefined;
        return (<PanelItem key={id} {...props}>
        {customAvatar ? (customAvatar) : nonMemberEmail ? (<AvatarWrapper>
            <Hovercard body={this.renderHovercardBody(author)}>
              <UserAvatar size={36} user={author}/>
              <EmailWarningIcon>
                <IconWarning size="xs"/>
              </EmailWarningIcon>
            </Hovercard>
          </AvatarWrapper>) : (<AvatarWrapper>
            <UserAvatar size={36} user={author}/>
          </AvatarWrapper>)}

        <CommitMessage>
          <Message>{this.renderMessage(message)}</Message>
          <Meta>
            {tct('[author] committed [timeago]', {
            author: <strong>{(author && author.name) || t('Unknown author')}</strong>,
            timeago: <TimeSince date={dateCreated}/>,
        })}
          </Meta>
        </CommitMessage>

        <div>
          <CommitLink commitId={id} repository={repository}/>
        </div>
      </PanelItem>);
    };
    CommitRow.propTypes = {
        commit: PropTypes.object,
        customAvatar: PropTypes.node,
    };
    return CommitRow;
}(React.Component));
var AvatarWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-self: flex-start;\n  margin-right: ", ";\n"], ["\n  align-self: flex-start;\n  margin-right: ", ";\n"])), space(2));
var EmailWarning = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n  margin: -4px;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n  margin: -4px;\n"])), function (p) { return p.theme.fontSizeSmall; });
var StyledLink = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  border-bottom: 1px dotted ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  border-bottom: 1px dotted ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var EmailWarningIcon = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  top: 15px;\n  left: -11px;\n  display: inline-block;\n  line-height: 12px;\n  border-radius: 50%;\n  border: 1px solid ", ";\n  background: ", ";\n  padding: 1px 2px 3px 2px;\n"], ["\n  position: relative;\n  top: 15px;\n  left: -11px;\n  display: inline-block;\n  line-height: 12px;\n  border-radius: 50%;\n  border: 1px solid ", ";\n  background: ", ";\n  padding: 1px 2px 3px 2px;\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.yellow200; });
var CommitMessage = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n  flex-direction: column;\n  min-width: 0;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  flex-direction: column;\n  min-width: 0;\n  margin-right: ", ";\n"])), space(2));
var Message = styled(TextOverflow)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: 15px;\n  line-height: 1.1;\n  font-weight: bold;\n"], ["\n  font-size: 15px;\n  line-height: 1.1;\n  font-weight: bold;\n"])));
var Meta = styled(TextOverflow)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: 13px;\n  line-height: 1.5;\n  margin: 0;\n  color: ", ";\n"], ["\n  font-size: 13px;\n  line-height: 1.5;\n  margin: 0;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
export default styled(CommitRow)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  align-items: center;\n"], ["\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=commitRow.jsx.map