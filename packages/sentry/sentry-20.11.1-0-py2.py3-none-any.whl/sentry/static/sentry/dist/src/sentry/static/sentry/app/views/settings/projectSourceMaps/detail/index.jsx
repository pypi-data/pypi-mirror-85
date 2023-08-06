import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import routeTitleGen from 'app/utils/routeTitle';
import SearchBar from 'app/components/searchBar';
import Pagination from 'app/components/pagination';
import { PanelTable } from 'app/components/panels';
import { formatVersion } from 'app/utils/formatters';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconDelete } from 'app/icons';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { decodeScalar } from 'app/utils/queryString';
import Confirm from 'app/components/confirm';
import Version from 'app/components/version';
import TextOverflow from 'app/components/textOverflow';
import space from 'app/styles/space';
import Access from 'app/components/acl/access';
import Tooltip from 'app/components/tooltip';
import SourceMapsArtifactRow from './sourceMapsArtifactRow';
var ProjectSourceMapsDetail = /** @class */ (function (_super) {
    __extends(ProjectSourceMapsDetail, _super);
    function ProjectSourceMapsDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleArtifactDelete = function (id) { return __awaiter(_this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        addLoadingMessage(t('Removing artifact\u2026'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + this.getArtifactsUrl() + id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        this.fetchData();
                        addSuccessMessage(t('Artifact removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('Unable to remove artifact. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleArchiveDelete = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, orgId, projectId, name, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, name = _a.name;
                        addLoadingMessage(t('Removing artifacts\u2026'));
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/files/source-maps/", {
                                method: 'DELETE',
                                query: { name: name },
                            })];
                    case 2:
                        _c.sent();
                        this.fetchData();
                        addSuccessMessage(t('Artifacts removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('Unable to remove artifacts. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectSourceMapsDetail.prototype.getTitle = function () {
        var _a = this.props.params, projectId = _a.projectId, name = _a.name;
        return routeTitleGen(t('Archive %s', formatVersion(name)), projectId, false);
    };
    ProjectSourceMapsDetail.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { artifacts: [] });
    };
    ProjectSourceMapsDetail.prototype.getEndpoints = function () {
        return [['artifacts', this.getArtifactsUrl(), { query: { query: this.getQuery() } }]];
    };
    ProjectSourceMapsDetail.prototype.getArtifactsUrl = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, name = _a.name;
        return "/projects/" + orgId + "/" + projectId + "/releases/" + encodeURIComponent(name) + "/files/";
    };
    ProjectSourceMapsDetail.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return decodeScalar(query);
    };
    ProjectSourceMapsDetail.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return t('There are no artifacts that match your search.');
        }
        return t('There are no artifacts in this archive.');
    };
    ProjectSourceMapsDetail.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectSourceMapsDetail.prototype.renderArtifacts = function () {
        var _this = this;
        var organization = this.props.organization;
        var artifacts = this.state.artifacts;
        var artifactApiUrl = this.api.baseUrl + this.getArtifactsUrl();
        if (!artifacts.length) {
            return null;
        }
        return artifacts.map(function (artifact) {
            return (<SourceMapsArtifactRow key={artifact.id} artifact={artifact} onDelete={_this.handleArtifactDelete} downloadUrl={"" + artifactApiUrl + artifact.id + "/?download=1"} downloadRole={organization.debugFilesRole}/>);
        });
    };
    ProjectSourceMapsDetail.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, loading = _a.loading, artifacts = _a.artifacts, artifactsPageLinks = _a.artifactsPageLinks;
        var _b = this.props.params, name = _b.name, orgId = _b.orgId;
        var project = this.props.project;
        return (<React.Fragment>
        <StyledSettingsPageHeader title={<Title>
              {t('Archive')}&nbsp;
              <TextOverflow>
                <Version version={name} tooltipRawVersion anchor={false} truncate/>
              </TextOverflow>
            </Title>} action={<StyledButtonBar gap={1}>
              <ReleaseButton to={"/organizations/" + orgId + "/releases/" + encodeURIComponent(name) + "/?project=" + project.id}>
                {t('Go to Release')}
              </ReleaseButton>
              <Access access={['project:releases']}>
                {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<Tooltip disabled={hasAccess} title={t('You do not have permission to delete artifacts.')}>
                    <Confirm message={t('Are you sure you want to remove all artifacts in this archive?')} onConfirm={_this.handleArchiveDelete} disabled={!hasAccess}>
                      <Button icon={<IconDelete size="sm"/>} title={t('Remove All Artifacts')} label={t('Remove All Artifacts')} disabled={!hasAccess}/>
                    </Confirm>
                  </Tooltip>);
        }}
              </Access>

              <SearchBar placeholder={t('Filter artifacts')} onSearch={this.handleSearch} query={this.getQuery()}/>
            </StyledButtonBar>}/>

        <StyledPanelTable headers={[
            t('Artifact'),
            <SizeColumn key="size">{t('File Size')}</SizeColumn>,
            '',
        ]} emptyMessage={this.getEmptyMessage()} isEmpty={artifacts.length === 0} isLoading={loading}>
          {this.renderArtifacts()}
        </StyledPanelTable>
        <Pagination pageLinks={artifactsPageLinks}/>
      </React.Fragment>);
    };
    return ProjectSourceMapsDetail;
}(AsyncView));
var StyledSettingsPageHeader = styled(SettingsPageHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /*\n    ugly selector to make header work on mobile\n    we can refactor this once we start making other settings more responsive\n  */\n  > div {\n    @media (max-width: ", ") {\n      display: block;\n    }\n    > div {\n      min-width: 0;\n      @media (max-width: ", ") {\n        margin-bottom: ", ";\n      }\n    }\n  }\n"], ["\n  /*\n    ugly selector to make header work on mobile\n    we can refactor this once we start making other settings more responsive\n  */\n  > div {\n    @media (max-width: ", ") {\n      display: block;\n    }\n    > div {\n      min-width: 0;\n      @media (max-width: ", ") {\n        margin-bottom: ", ";\n      }\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[2]; }, space(2));
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledButtonBar = styled(ButtonBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
var StyledPanelTable = styled(PanelTable)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"], ["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"])));
var ReleaseButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var SizeColumn = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
export default ProjectSourceMapsDetail;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map