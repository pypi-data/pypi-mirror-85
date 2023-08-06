import { __assign, __extends } from "tslib";
import React from 'react';
import CommitRow from 'app/components/commitRow';
import { t } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import { formatVersion } from 'app/utils/formatters';
import withApi from 'app/utils/withApi';
import Pagination from 'app/components/pagination';
import AsyncView from 'app/views/asyncView';
import { PanelHeader, Panel, PanelBody } from 'app/components/panels';
import { getCommitsByRepository, getQuery, getReposToRender } from './utils';
import withRepositories from './withRepositories';
import RepositorySwitcher from './repositorySwitcher';
import EmptyState from './emptyState';
var Commits = /** @class */ (function (_super) {
    __extends(Commits, _super);
    function Commits() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Commits.prototype.getTitle = function () {
        var params = this.props.params;
        var orgId = params.orgId;
        return routeTitleGen(t('Commits - Release %s', formatVersion(params.release)), orgId, false);
    };
    Commits.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { commits: [] });
    };
    Commits.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, projectSlug = _a.projectSlug, activeRepository = _a.activeRepository, location = _a.location;
        var orgId = params.orgId, release = params.release;
        var query = getQuery({ location: location, activeRepository: activeRepository });
        return [
            [
                'commits',
                "/projects/" + orgId + "/" + projectSlug + "/releases/" + encodeURIComponent(release) + "/commits/",
                { query: query },
            ],
        ];
    };
    Commits.prototype.renderContent = function () {
        var _a = this.state, commits = _a.commits, commitsPageLinks = _a.commitsPageLinks;
        var activeRepository = this.props.activeRepository;
        if (!commits.length) {
            return (<EmptyState>
          {!activeRepository
                ? t('There are no commits associated with this release.')
                : t('There are no commits associated with this release in the %s repository.', activeRepository.name)}
        </EmptyState>);
        }
        var commitsByRepository = getCommitsByRepository(commits);
        var reposToRender = getReposToRender(Object.keys(commitsByRepository));
        return (<React.Fragment>
        {reposToRender.map(function (repoName) {
            var _a;
            return (<Panel key={repoName}>
            <PanelHeader>{repoName}</PanelHeader>
            <PanelBody>
              {(_a = commitsByRepository[repoName]) === null || _a === void 0 ? void 0 : _a.map(function (commit) { return (<CommitRow key={commit.id} commit={commit}/>); })}
            </PanelBody>
          </Panel>);
        })}
        <Pagination pageLinks={commitsPageLinks}/>
      </React.Fragment>);
    };
    Commits.prototype.renderBody = function () {
        var _a = this.props, location = _a.location, router = _a.router, activeRepository = _a.activeRepository, repositories = _a.repositories;
        return (<React.Fragment>
        {repositories.length > 1 && (<RepositorySwitcher repositories={repositories} activeRepository={activeRepository} location={location} router={router}/>)}
        {this.renderContent()}
      </React.Fragment>);
    };
    return Commits;
}(AsyncView));
export default withApi(withRepositories(Commits));
//# sourceMappingURL=commits.jsx.map