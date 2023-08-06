import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { PanelTable } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Pagination from 'app/components/pagination';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import routeTitleGen from 'app/utils/routeTitle';
import Checkbox from 'app/components/checkbox';
import SearchBar from 'app/components/searchBar';
// TODO(android-mappings): use own components once we decide how this should look like
import DebugFileRow from 'app/views/settings/projectDebugFiles/debugFileRow';
var ProjectProguard = /** @class */ (function (_super) {
    __extends(ProjectProguard, _super);
    function ProjectProguard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (id) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + encodeURIComponent(id), {
                method: 'DELETE',
                complete: function () { return _this.fetchData(); },
            });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        return _this;
    }
    ProjectProguard.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('ProGuard Mappings'), projectId, false);
    };
    ProjectProguard.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { mappings: [], showDetails: false });
    };
    ProjectProguard.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            [
                'mappings',
                "/projects/" + orgId + "/" + projectId + "/files/dsyms/",
                { query: { query: location.query.query, file_formats: 'proguard' } },
            ],
        ];
        return endpoints;
    };
    ProjectProguard.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ProjectProguard.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return t('There are no mappings that match your search.');
        }
        return t('There are no mappings for this project.');
    };
    ProjectProguard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectProguard.prototype.renderMappings = function () {
        var _this = this;
        var _a = this.state, mappings = _a.mappings, showDetails = _a.showDetails;
        var _b = this.props, organization = _b.organization, params = _b.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!(mappings === null || mappings === void 0 ? void 0 : mappings.length)) {
            return null;
        }
        return mappings.map(function (mapping) {
            var downloadUrl = _this.api.baseUrl + "/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + encodeURIComponent(mapping.id);
            return (<DebugFileRow debugFile={mapping} showDetails={showDetails} downloadUrl={downloadUrl} downloadRole={organization.debugFilesRole} onDelete={_this.handleDelete} key={mapping.id}/>);
        });
    };
    ProjectProguard.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, loading = _a.loading, showDetails = _a.showDetails, mappings = _a.mappings, mappingsPageLinks = _a.mappingsPageLinks;
        return (<React.Fragment>
        <SettingsPageHeader title={t('ProGuard Mappings')}/>

        <TextBlock>
          {t("ProGuard mapping files are used to convert minified classes, methods and field names into a human readable format.")}
        </TextBlock>

        <Wrapper>
          <TextBlock noMargin>{t('Uploaded mappings')}:</TextBlock>

          <Filters>
            <Label>
              <Checkbox checked={showDetails} onChange={function (e) {
            _this.setState({ showDetails: e.target.checked });
        }}/>
              {t('show details')}
            </Label>

            <SearchBar placeholder={t('Search mappings')} onSearch={this.handleSearch} query={this.getQuery()}/>
          </Filters>
        </Wrapper>

        <StyledPanelTable headers={[
            t('Debug ID'),
            t('Information'),
            <Actions key="actions">{t('Actions')}</Actions>,
        ]} emptyMessage={this.getEmptyMessage()} isEmpty={(mappings === null || mappings === void 0 ? void 0 : mappings.length) === 0} isLoading={loading}>
          {this.renderMappings()}
        </StyledPanelTable>
        <Pagination pageLinks={mappingsPageLinks}/>
      </React.Fragment>);
    };
    return ProjectProguard;
}(AsyncView));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: 37% 1fr auto;\n"], ["\n  grid-template-columns: 37% 1fr auto;\n"])));
var Actions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(4), space(4), space(1), function (p) { return p.theme.breakpoints[0]; });
var Filters = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content minmax(200px, 400px);\n  align-items: center;\n  justify-content: flex-end;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: min-content minmax(200px, 400px);\n  align-items: center;\n  justify-content: flex-end;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var Label = styled('label')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-weight: normal;\n  display: flex;\n  margin-bottom: 0;\n  white-space: nowrap;\n  input {\n    margin-top: 0;\n    margin-right: ", ";\n  }\n"], ["\n  font-weight: normal;\n  display: flex;\n  margin-bottom: 0;\n  white-space: nowrap;\n  input {\n    margin-top: 0;\n    margin-right: ", ";\n  }\n"])), space(1));
export default ProjectProguard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=projectProguard.jsx.map