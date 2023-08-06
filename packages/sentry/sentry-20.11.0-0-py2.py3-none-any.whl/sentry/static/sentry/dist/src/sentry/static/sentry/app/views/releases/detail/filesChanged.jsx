import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import { formatVersion } from 'app/utils/formatters';
import withApi from 'app/utils/withApi';
import { Main } from 'app/components/layouts/thirds';
import Pagination from 'app/components/pagination';
import AsyncView from 'app/views/asyncView';
import { PanelHeader, Panel, PanelBody } from 'app/components/panels';
import FileChange from 'app/components/fileChange';
import { getFilesByRepository, getReposToRender, getQuery } from './utils';
import withRepositories from './withRepositories';
import RepositorySwitcher from './repositorySwitcher';
import EmptyState from './emptyState';
var FilesChanged = /** @class */ (function (_super) {
    __extends(FilesChanged, _super);
    function FilesChanged() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getEndpoints = function () {
            var _a = _this.props, params = _a.params, activeRepository = _a.activeRepository, location = _a.location;
            var orgId = params.orgId, release = params.release;
            var query = getQuery({ location: location, activeRepository: activeRepository });
            return [
                [
                    'fileList',
                    "/organizations/" + orgId + "/releases/" + encodeURIComponent(release) + "/commitfiles/",
                    { query: query },
                ],
            ];
        };
        return _this;
    }
    FilesChanged.prototype.getTitle = function () {
        var params = this.props.params;
        var orgId = params.orgId;
        return routeTitleGen(t('Files Changed - Release %s', formatVersion(params.release)), orgId, false);
    };
    FilesChanged.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { fileList: [] });
    };
    FilesChanged.prototype.renderContent = function () {
        var _a = this.state, fileList = _a.fileList, fileListPageLinks = _a.fileListPageLinks;
        var activeRepository = this.props.activeRepository;
        if (!fileList.length) {
            return (<EmptyState>
          {!activeRepository
                ? t('There are no changed files associated with this release.')
                : t('There are no changed files associated with this release in the %s repository.', activeRepository.name)}
        </EmptyState>);
        }
        var filesByRepository = getFilesByRepository(fileList);
        var reposToRender = getReposToRender(Object.keys(filesByRepository));
        return (<React.Fragment>
        {reposToRender.map(function (repoName) {
            var repoData = filesByRepository[repoName];
            var files = Object.keys(repoData);
            var fileCount = files.length;
            return (<Panel key={repoName}>
              <PanelHeader>
                <span>{repoName}</span>
                <span>{tn('%s file changed', '%s files changed', fileCount)}</span>
              </PanelHeader>
              <PanelBody>
                {files.map(function (filename) {
                var authors = repoData[filename].authors;
                return (<StyledFileChange key={filename} filename={filename} authors={Object.values(authors)}/>);
            })}
              </PanelBody>
            </Panel>);
        })}
        <Pagination pageLinks={fileListPageLinks}/>
      </React.Fragment>);
    };
    FilesChanged.prototype.renderBody = function () {
        var _a = this.props, activeRepository = _a.activeRepository, router = _a.router, repositories = _a.repositories, location = _a.location;
        return (<React.Fragment>
        {repositories.length > 1 && (<RepositorySwitcher repositories={repositories} activeRepository={activeRepository} location={location} router={router}/>)}
        {this.renderContent()}
      </React.Fragment>);
    };
    FilesChanged.prototype.renderComponent = function () {
        return <Main fullWidth>{_super.prototype.renderComponent.call(this)}</Main>;
    };
    return FilesChanged;
}(AsyncView));
export default withApi(withRepositories(FilesChanged));
var StyledFileChange = styled(FileChange)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-radius: 0;\n  border-left: none;\n  border-right: none;\n  border-top: none;\n  :last-child {\n    border: none;\n    border-radius: 0;\n  }\n"], ["\n  border-radius: 0;\n  border-left: none;\n  border-right: none;\n  border-top: none;\n  :last-child {\n    border: none;\n    border-radius: 0;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=filesChanged.jsx.map