import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AvatarList from 'app/components/avatar/avatarList';
import Button from 'app/components/button';
import Hovercard from 'app/components/hovercard';
import LastCommit from 'app/components/lastCommit';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import RepoLabel from 'app/components/repoLabel';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withRelease from 'app/utils/withRelease';
import withRepositories from 'app/utils/withRepositories';
import Clipboard from 'app/components/clipboard';
import { IconCopy } from 'app/icons';
import Version from 'app/components/version';
var VersionHoverCard = /** @class */ (function (_super) {
    __extends(VersionHoverCard, _super);
    function VersionHoverCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            visible: false,
        };
        return _this;
    }
    VersionHoverCard.prototype.toggleHovercard = function () {
        this.setState({
            visible: true,
        });
    };
    VersionHoverCard.prototype.getRepoLink = function () {
        var orgSlug = this.props.orgSlug;
        return {
            header: null,
            body: (<ConnectRepo>
          <h5>{t('Releases are better with commit data!')}</h5>
          <p>
            {t('Connect a repository to see commit info, files changed, and authors involved in future releases.')}
          </p>
          <Button href={"/organizations/" + orgSlug + "/repos/"} priority="primary">
            {t('Connect a repository')}
          </Button>
        </ConnectRepo>),
        };
    };
    VersionHoverCard.prototype.getBody = function () {
        var _a = this.props, releaseVersion = _a.releaseVersion, release = _a.release, deploys = _a.deploys;
        if (release === undefined || deploys === undefined) {
            return { header: null, body: null };
        }
        var lastCommit = release.lastCommit;
        var recentDeploysByEnvironment = deploys.reduce(function (dbe, deploy) {
            var dateFinished = deploy.dateFinished, environment = deploy.environment;
            if (!dbe.hasOwnProperty(environment)) {
                dbe[environment] = dateFinished;
            }
            return dbe;
        }, {});
        var mostRecentDeploySlice = Object.keys(recentDeploysByEnvironment);
        if (Object.keys(recentDeploysByEnvironment).length > 3) {
            mostRecentDeploySlice = Object.keys(recentDeploysByEnvironment).slice(0, 3);
        }
        return {
            header: (<HeaderWrapper>
          {t('Release')}
          <VersionWrapper>
            <StyledVersion version={releaseVersion} truncate anchor={false}/>

            <Clipboard value={releaseVersion}>
              <ClipboardIconWrapper>
                <IconCopy size="xs"/>
              </ClipboardIconWrapper>
            </Clipboard>
          </VersionWrapper>
        </HeaderWrapper>),
            body: (<div>
          <div className="row row-flex">
            <div className="col-xs-4">
              <h6>{t('New Issues')}</h6>
              <div className="count-since">{release.newGroups}</div>
            </div>
            <div className="col-xs-8">
              <h6 style={{ textAlign: 'right' }}>
                {release.commitCount}{' '}
                {release.commitCount !== 1 ? t('commits ') : t('commit ')} {t('by ')}{' '}
                {release.authors.length}{' '}
                {release.authors.length !== 1 ? t('authors') : t('author')}{' '}
              </h6>
              <AvatarList users={release.authors} avatarSize={25} tooltipOptions={{ container: 'body' }} typeMembers="authors"/>
            </div>
          </div>
          {lastCommit && <LastCommit commit={lastCommit} headerClass="commit-heading"/>}
          {deploys.length > 0 && (<div>
              <div className="divider">
                <h6 className="deploy-heading">{t('Deploys')}</h6>
              </div>
              {mostRecentDeploySlice.map(function (env, idx) {
                var dateFinished = recentDeploysByEnvironment[env];
                return (<div className="deploy" key={idx}>
                    <div className="deploy-meta" style={{ position: 'relative' }}>
                      <VersionRepoLabel>{env}</VersionRepoLabel>
                      {dateFinished && <StyledTimeSince date={dateFinished}/>}
                    </div>
                  </div>);
            })}
            </div>)}
        </div>),
        };
    };
    VersionHoverCard.prototype.render = function () {
        var _a;
        var _b = this.props, deploysLoading = _b.deploysLoading, deploysError = _b.deploysError, release = _b.release, releaseLoading = _b.releaseLoading, releaseError = _b.releaseError, repositories = _b.repositories, repositoriesLoading = _b.repositoriesLoading, repositoriesError = _b.repositoriesError;
        var header = null;
        var body = null;
        var loading = !!(deploysLoading || releaseLoading || repositoriesLoading);
        var error = (_a = deploysError !== null && deploysError !== void 0 ? deploysError : releaseError) !== null && _a !== void 0 ? _a : repositoriesError;
        var hasRepos = repositories && repositories.length > 0;
        if (loading) {
            body = <LoadingIndicator mini/>;
        }
        else if (error) {
            body = <LoadingError />;
        }
        else {
            var renderObj = hasRepos && release ? this.getBody() : this.getRepoLink();
            header = renderObj.header;
            body = renderObj.body;
        }
        return (<Hovercard {...this.props} header={header} body={body}>
        {this.props.children}
      </Hovercard>);
    };
    return VersionHoverCard;
}(React.Component));
export { VersionHoverCard };
export default withApi(withRelease(withRepositories(VersionHoverCard)));
var ConnectRepo = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  text-align: center;\n"], ["\n  padding: ", ";\n  text-align: center;\n"])), space(2));
var VersionRepoLabel = styled(RepoLabel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 86px;\n"], ["\n  width: 86px;\n"])));
var StyledTimeSince = styled(TimeSince)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  position: absolute;\n  left: 98px;\n  width: 50%;\n  padding: 3px 0;\n"], ["\n  color: ", ";\n  position: absolute;\n  left: 98px;\n  width: 50%;\n  padding: 3px 0;\n"])), function (p) { return p.theme.gray300; });
var HeaderWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var VersionWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  justify-content: flex-end;\n"])));
var StyledVersion = styled(Version)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-right: ", ";\n  max-width: 190px;\n"], ["\n  margin-right: ", ";\n  max-width: 190px;\n"])), space(0.5));
var ClipboardIconWrapper = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  &:hover {\n    cursor: pointer;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=versionHoverCard.jsx.map