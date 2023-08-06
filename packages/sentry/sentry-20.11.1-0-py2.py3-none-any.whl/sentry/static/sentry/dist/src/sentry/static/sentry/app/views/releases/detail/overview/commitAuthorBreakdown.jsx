import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import UserAvatar from 'app/components/avatar/userAvatar';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import AsyncComponent from 'app/components/asyncComponent';
import { percent } from 'app/utils';
import { userDisplayName } from 'app/utils/formatters';
import Button from 'app/components/button';
import { SectionHeading, Wrapper } from './styles';
var CommitAuthorBreakdown = /** @class */ (function (_super) {
    __extends(CommitAuthorBreakdown, _super);
    function CommitAuthorBreakdown() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onCollapseToggle = function () {
            _this.setState(function (state) { return ({
                collapsed: !state.collapsed,
            }); });
        };
        return _this;
    }
    CommitAuthorBreakdown.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { collapsed: true });
    };
    CommitAuthorBreakdown.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, projectSlug = _a.projectSlug, version = _a.version;
        var commitsEndpoint = "/projects/" + orgId + "/" + projectSlug + "/releases/" + encodeURIComponent(version) + "/commits/";
        return [['commits', commitsEndpoint]];
    };
    CommitAuthorBreakdown.prototype.getDisplayPercent = function (authorCommitCount) {
        var commits = this.state.commits;
        var calculatedPercent = Math.round(percent(authorCommitCount, commits.length));
        return (calculatedPercent < 1 ? '<1' : calculatedPercent) + "%";
    };
    CommitAuthorBreakdown.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var collapsed = this.state.collapsed;
        // group commits by author
        var groupedAuthorCommits = (_a = this.state.commits) === null || _a === void 0 ? void 0 : _a.reduce(function (authorCommitsAccumulator, commit) {
            var _a, _b;
            var email = (_b = (_a = commit.author) === null || _a === void 0 ? void 0 : _a.email) !== null && _b !== void 0 ? _b : 'unknown';
            if (authorCommitsAccumulator.hasOwnProperty(email)) {
                authorCommitsAccumulator[email].commitCount += 1;
            }
            else {
                authorCommitsAccumulator[email] = {
                    commitCount: 1,
                    author: commit.author,
                };
            }
            return authorCommitsAccumulator;
        }, {});
        // sort authors by number of commits
        var sortedAuthorsByNumberOfCommits = Object.values(groupedAuthorCommits).sort(function (a, b) { return b.commitCount - a.commitCount; });
        if (!sortedAuthorsByNumberOfCommits.length) {
            return null;
        }
        // collapse them
        var MAX = CommitAuthorBreakdown.MAX_WHEN_COLLAPSED;
        var initialNumberOfAuthors = sortedAuthorsByNumberOfCommits.length;
        var canExpand = initialNumberOfAuthors > MAX;
        if (collapsed && canExpand) {
            sortedAuthorsByNumberOfCommits = sortedAuthorsByNumberOfCommits.slice(0, MAX);
        }
        var collapsedNumberOfAuthors = initialNumberOfAuthors - sortedAuthorsByNumberOfCommits.length;
        return (<Wrapper>
        <SectionHeading>{t('Commit Author Breakdown')}</SectionHeading>
        {sortedAuthorsByNumberOfCommits.map(function (_a) {
            var commitCount = _a.commitCount, author = _a.author;
            return (<AuthorLine key={author === null || author === void 0 ? void 0 : author.email}>
            <Author>
              <StyledUserAvatar user={author} size={20} hasTooltip/>
              <AuthorName>{userDisplayName(author || {}, false)}</AuthorName>
            </Author>

            <Stats>
              <Commits>{tn('%s commit', '%s commits', commitCount)}</Commits>
              <Percent>{_this.getDisplayPercent(commitCount)}</Percent>
            </Stats>
          </AuthorLine>);
        })}
        {collapsedNumberOfAuthors > 0 && (<StyledButton priority="link" onClick={this.onCollapseToggle}>
            {tn('Show %s collapsed author', 'Show %s collapsed authors', collapsedNumberOfAuthors)}
          </StyledButton>)}
        {collapsedNumberOfAuthors === 0 && canExpand && (<StyledButton priority="link" onClick={this.onCollapseToggle}>
            {t('Collapse')}
          </StyledButton>)}
      </Wrapper>);
    };
    CommitAuthorBreakdown.MAX_WHEN_COLLAPSED = 5;
    return CommitAuthorBreakdown;
}(AsyncComponent));
var AuthorLine = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeSmall; });
var Author = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  overflow: hidden;\n"])));
var StyledUserAvatar = styled(UserAvatar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var AuthorName = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: 600;\n  color: ", ";\n  padding-right: ", ";\n  ", ";\n"], ["\n  font-weight: 600;\n  color: ", ";\n  padding-right: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, space(0.5), overflowEllipsis);
var Stats = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  width: 115px;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  width: 115px;\n"])));
var Commits = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Percent = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  min-width: 40px;\n  text-align: right;\n  color: ", ";\n"], ["\n  min-width: 40px;\n  text-align: right;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledButton = styled(Button)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
export default CommitAuthorBreakdown;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=commitAuthorBreakdown.jsx.map