import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import routeTitleGen from 'app/utils/routeTitle';
import TextBlock from 'app/views/settings/components/text/textBlock';
import SearchBar from 'app/components/searchBar';
import Pagination from 'app/components/pagination';
import { PanelTable } from 'app/components/panels';
import { decodeScalar } from 'app/utils/queryString';
import { addLoadingMessage, addSuccessMessage, addErrorMessage, } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import space from 'app/styles/space';
import SourceMapsArchiveRow from './sourceMapsArchiveRow';
var ProjectSourceMaps = /** @class */ (function (_super) {
    __extends(ProjectSourceMaps, _super);
    function ProjectSourceMaps() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleDelete = function (name) { return __awaiter(_this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        addLoadingMessage(t('Removing artifacts\u2026'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.getArchivesUrl(), {
                                method: 'DELETE',
                                query: { name: name },
                            })];
                    case 2:
                        _b.sent();
                        this.fetchData();
                        addSuccessMessage(t('Artifacts removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('Unable to remove artifacts. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectSourceMaps.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Source Maps'), projectId, false);
    };
    ProjectSourceMaps.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { archives: [] });
    };
    ProjectSourceMaps.prototype.getEndpoints = function () {
        return [['archives', this.getArchivesUrl(), { query: { query: this.getQuery() } }]];
    };
    ProjectSourceMaps.prototype.getArchivesUrl = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return "/projects/" + orgId + "/" + projectId + "/files/source-maps/";
    };
    ProjectSourceMaps.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return decodeScalar(query);
    };
    ProjectSourceMaps.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return t('There are no archives that match your search.');
        }
        return t('There are no archives for this project.');
    };
    ProjectSourceMaps.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectSourceMaps.prototype.renderArchives = function () {
        var _this = this;
        var archives = this.state.archives;
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!archives.length) {
            return null;
        }
        return archives.map(function (a) {
            return (<SourceMapsArchiveRow key={a.name} archive={a} orgId={orgId} projectId={projectId} onDelete={_this.handleDelete}/>);
        });
    };
    ProjectSourceMaps.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, archives = _a.archives, archivesPageLinks = _a.archivesPageLinks;
        return (<React.Fragment>
        <SettingsPageHeader title={t('Source Maps')} action={<SearchBar placeholder={t('Filter Archives')} onSearch={this.handleSearch} query={this.getQuery()} width="280px"/>}/>

        <TextBlock>
          {tct("These source map archives help Sentry identify where to look when Javascript is minified. By providing this information, you can get better context for your stack traces when debugging. To learn more about source maps, [link: read the docs].", {
            link: (<ExternalLink href="https://docs.sentry.io/platforms/javascript/sourcemaps/"/>),
        })}
        </TextBlock>

        <StyledPanelTable headers={[
            t('Archive'),
            <ArtifactsColumn key="artifacts">{t('Artifacts')}</ArtifactsColumn>,
            t('Type'),
            t('Date Created'),
            '',
        ]} emptyMessage={this.getEmptyMessage()} isEmpty={archives.length === 0} isLoading={loading}>
          {this.renderArchives()}
        </StyledPanelTable>
        <Pagination pageLinks={archivesPageLinks}/>
      </React.Fragment>);
    };
    return ProjectSourceMaps;
}(AsyncView));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns:\n    minmax(120px, 1fr) max-content minmax(85px, max-content) minmax(265px, max-content)\n    75px;\n"], ["\n  grid-template-columns:\n    minmax(120px, 1fr) max-content minmax(85px, max-content) minmax(265px, max-content)\n    75px;\n"])));
var ArtifactsColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n  padding-right: ", ";\n  margin-right: ", ";\n"], ["\n  text-align: right;\n  padding-right: ", ";\n  margin-right: ", ";\n"])), space(1.5), space(0.25));
export default ProjectSourceMaps;
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map