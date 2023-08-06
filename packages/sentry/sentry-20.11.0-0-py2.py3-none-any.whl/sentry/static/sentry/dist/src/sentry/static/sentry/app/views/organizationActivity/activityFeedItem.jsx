import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { t, tn, tct } from 'app/locale';
import CommitLink from 'app/components/commitLink';
import Duration from 'app/components/duration';
import ExternalLink from 'app/components/links/externalLink';
import IssueLink from 'app/components/issueLink';
import MemberListStore from 'app/stores/memberListStore';
import PullRequestLink from 'app/components/pullRequestLink';
import TeamStore from 'app/stores/teamStore';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import VersionHoverCard from 'app/components/versionHoverCard';
import marked from 'app/utils/marked';
import space from 'app/styles/space';
import ActivityAvatar from 'app/components/activity/item/avatar';
var defaultProps = {
    defaultClipped: false,
    clipHeight: 68,
};
var ActivityItem = /** @class */ (function (_super) {
    __extends(ActivityItem, _super);
    function ActivityItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            clipped: _this.props.defaultClipped,
        };
        _this.activityBubbleRef = React.createRef();
        _this.formatProjectActivity = function (author, item) {
            var data = item.data;
            var orgId = _this.props.organization.slug;
            var project = item.project;
            var issue = item.issue;
            var basePath = "/organizations/" + orgId + "/issues/";
            var issueLink = issue ? (<IssueLink orgId={orgId} issue={issue} to={"" + basePath + issue.id + "/"} card>
        {issue.shortId}
      </IssueLink>) : null;
            var versionLink = data.version ? (<VersionHoverCard orgSlug={orgId} projectSlug={project.slug} releaseVersion={data.version}>
        <Version version={data.version} projectId={project.id}/>
      </VersionHoverCard>) : null;
            switch (item.type) {
                case 'note':
                    return tct('[author] commented on [issue]', {
                        author: author,
                        issue: (<IssueLink card orgId={orgId} issue={issue} to={"" + basePath + issue.id + "/activity/#event_" + item.id}>
              {issue.shortId}
            </IssueLink>),
                    });
                case 'set_resolved':
                    return tct('[author] marked [issue] as resolved', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_resolved_by_age':
                    return tct('[author] marked [issue] as resolved due to age', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_resolved_in_release':
                    if (data.version) {
                        return tct('[author] marked [issue] as resolved in [version]', {
                            author: author,
                            version: versionLink,
                            issue: issueLink,
                        });
                    }
                    return tct('[author] marked [issue] as resolved in the upcoming release', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_resolved_in_commit':
                    return tct('[author] marked [issue] as resolved in [version]', {
                        author: author,
                        version: (<CommitLink inline commitId={data.commit && data.commit.id} repository={data.commit && data.commit.repository}/>),
                        issue: issueLink,
                    });
                case 'set_resolved_in_pull_request':
                    return tct('[author] marked [issue] as resolved in [version]', {
                        author: author,
                        version: (<PullRequestLink inline pullRequest={data.pullRequest} repository={data.pullRequest && data.pullRequest.repository}/>),
                        issue: issueLink,
                    });
                case 'set_unresolved':
                    return tct('[author] marked [issue] as unresolved', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_ignored':
                    if (data.ignoreDuration) {
                        return tct('[author] ignored [issue] for [duration]', {
                            author: author,
                            duration: <Duration seconds={data.ignoreDuration * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreCount && data.ignoreWindow) {
                        return tct('[author] ignored [issue] until it happens [count] time(s) in [duration]', {
                            author: author,
                            count: data.ignoreCount,
                            duration: <Duration seconds={data.ignoreWindow * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreCount) {
                        return tct('[author] ignored [issue] until it happens [count] time(s)', {
                            author: author,
                            count: data.ignoreCount,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreUserCount && data.ignoreUserWindow) {
                        return tct('[author] ignored [issue] until it affects [count] user(s) in [duration]', {
                            author: author,
                            count: data.ignoreUserCount,
                            duration: <Duration seconds={data.ignoreUserWindow * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreUserCount) {
                        return tct('[author] ignored [issue] until it affects [count] user(s)', {
                            author: author,
                            count: data.ignoreUserCount,
                            issue: issueLink,
                        });
                    }
                    return tct('[author] ignored [issue]', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_public':
                    return tct('[author] made [issue] public', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_private':
                    return tct('[author] made [issue] private', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_regression':
                    if (data.version) {
                        return tct('[author] marked [issue] as a regression in [version]', {
                            author: author,
                            version: versionLink,
                            issue: issueLink,
                        });
                    }
                    return tct('[author] marked [issue] as a regression', {
                        author: author,
                        issue: issueLink,
                    });
                case 'create_issue':
                    return tct('[author] linked [issue] on [provider]', {
                        author: author,
                        provider: data.provider,
                        issue: issueLink,
                    });
                case 'unmerge_destination':
                    return tn('%2$s migrated %1$s fingerprint from %3$s to %4$s', '%2$s migrated %1$s fingerprints from %3$s to %4$s', data.fingerprints.length, author, data.source ? (<a href={"" + basePath + data.source.id}>{data.source.shortId}</a>) : (t('a group')), issueLink);
                case 'first_seen':
                    return tct('[author] saw [link:issue]', {
                        author: author,
                        issue: issueLink,
                    });
                case 'assigned':
                    var assignee = void 0;
                    if (data.assigneeType === 'team') {
                        var team = TeamStore.getById(data.assignee);
                        assignee = team ? team.slug : '<unknown-team>';
                        return tct('[author] assigned [issue] to #[assignee]', {
                            author: author,
                            issue: issueLink,
                            assignee: assignee,
                        });
                    }
                    if (item.user && data.assignee === item.user.id) {
                        return tct('[author] assigned [issue] to themselves', {
                            author: author,
                            issue: issueLink,
                        });
                    }
                    assignee = MemberListStore.getById(data.assignee);
                    if (assignee && assignee.email) {
                        return tct('[author] assigned [issue] to [assignee]', {
                            author: author,
                            assignee: <span title={assignee.email}>{assignee.name}</span>,
                            issue: issueLink,
                        });
                    }
                    else if (data.assigneeEmail) {
                        return tct('[author] assigned [issue] to [assignee]', {
                            author: author,
                            assignee: data.assigneeEmail,
                            issue: issueLink,
                        });
                    }
                    return tct('[author] assigned [issue] to an [help:unknown user]', {
                        author: author,
                        help: <span title={data.assignee}/>,
                        issue: issueLink,
                    });
                case 'unassigned':
                    return tct('[author] unassigned [issue]', {
                        author: author,
                        issue: issueLink,
                    });
                case 'merge':
                    return tct('[author] merged [count] [link:issues]', {
                        author: author,
                        count: data.issues.length + 1,
                        link: <Link to={"" + basePath + issue.id + "/"}/>,
                    });
                case 'release':
                    return tct('[author] released version [version]', {
                        author: author,
                        version: versionLink,
                    });
                case 'deploy':
                    return tct('[author] deployed version [version] to [environment].', {
                        author: author,
                        version: versionLink,
                        environment: data.environment || 'Default Environment',
                    });
                default:
                    return ''; // should never hit (?)
            }
        };
        return _this;
    }
    ActivityItem.prototype.componentDidMount = function () {
        if (this.activityBubbleRef.current) {
            var bubbleHeight = this.activityBubbleRef.current.offsetHeight;
            if (bubbleHeight > this.props.clipHeight) {
                // okay if this causes re-render; cannot determine until
                // rendered first anyways
                // eslint-disable-next-line react/no-did-mount-set-state
                this.setState({ clipped: true });
            }
        }
    };
    ActivityItem.prototype.render = function () {
        var _a = this.props, className = _a.className, item = _a.item;
        var avatar = (<ActivityAvatar type={!item.user ? 'system' : 'user'} user={item.user} size={36}/>);
        var author = {
            name: item.user ? item.user.name : 'Sentry',
            avatar: avatar,
        };
        var hasBubble = ['note', 'create_issue'].includes(item.type);
        var bubbleProps = __assign(__assign({}, (item.type === 'note'
            ? { dangerouslySetInnerHTML: { __html: marked(item.data.text) } }
            : {})), (item.type === 'create_issue'
            ? {
                children: (<ExternalLink href={item.data.location}>{item.data.title}</ExternalLink>),
            }
            : {}));
        return (<div className={className}>
        {author.avatar}
        <div>
          {this.formatProjectActivity(<span>
              <ActivityAuthor>{author.name}</ActivityAuthor>
            </span>, item)}
          {hasBubble && (<Bubble ref={this.activityBubbleRef} clipped={this.state.clipped} {...bubbleProps}/>)}
          <Meta>
            <Project>{item.project.slug}</Project>
            <StyledTimeSince date={item.dateCreated}/>
          </Meta>
        </div>
      </div>);
    };
    ActivityItem.defaultProps = defaultProps;
    return ActivityItem;
}(React.Component));
export default styled(ActivityItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n  position: relative;\n  margin: 0;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  line-height: 1.4;\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n  position: relative;\n  margin: 0;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  line-height: 1.4;\n  font-size: ", ";\n"])), space(1), space(1), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.fontSizeMedium; });
var ActivityAuthor = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: 600;\n"], ["\n  font-weight: 600;\n"])));
var Meta = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeRelativeSmall; });
var Project = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var Bubble = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  background: ", ";\n  margin: ", " 0;\n  padding: ", " ", ";\n  border: 1px solid ", ";\n  border-radius: 3px;\n  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.04);\n  position: relative;\n  overflow: hidden;\n\n  a {\n    max-width: 100%;\n    overflow-x: hidden;\n    text-overflow: ellipsis;\n  }\n\n  p {\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  ", "\n"], ["\n  background: ", ";\n  margin: ", " 0;\n  padding: ", " ", ";\n  border: 1px solid ", ";\n  border-radius: 3px;\n  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.04);\n  position: relative;\n  overflow: hidden;\n\n  a {\n    max-width: 100%;\n    overflow-x: hidden;\n    text-overflow: ellipsis;\n  }\n\n  p {\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  ",
    "\n"])), function (p) { return p.theme.backgroundSecondary; }, space(0.5), space(1), space(2), function (p) { return p.theme.border; }, function (p) {
    return p.clipped &&
        "\n    max-height: 68px;\n\n    &:after {\n      position: absolute;\n      content: '';\n      display: block;\n      bottom: 0;\n      right: 0;\n      left: 0;\n      height: 36px;\n      background-image: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 1));\n      border-bottom: 6px solid #fff;\n      border-radius: 0 0 3px 3px;\n      pointer-events: none;\n    }\n  ";
});
var StyledTimeSince = styled(TimeSince)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  padding-left: ", ";\n"], ["\n  color: ", ";\n  padding-left: ", ";\n"])), function (p) { return p.theme.gray300; }, space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=activityFeedItem.jsx.map