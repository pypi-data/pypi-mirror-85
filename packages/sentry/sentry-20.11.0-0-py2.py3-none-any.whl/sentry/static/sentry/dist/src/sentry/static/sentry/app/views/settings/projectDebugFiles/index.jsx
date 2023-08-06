import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { PanelTable } from 'app/components/panels';
import { fields } from 'app/data/forms/projectDebugFiles';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import Pagination from 'app/components/pagination';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import routeTitleGen from 'app/utils/routeTitle';
import Checkbox from 'app/components/checkbox';
import SearchBar from 'app/components/searchBar';
import ProjectActions from 'app/actions/projectActions';
import DebugFileRow from './debugFileRow';
var ProjectDebugSymbols = /** @class */ (function (_super) {
    __extends(ProjectDebugSymbols, _super);
    function ProjectDebugSymbols() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (id) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + id, {
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
    ProjectDebugSymbols.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Debug Files'), projectId, false);
    };
    ProjectDebugSymbols.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { showDetails: false });
    };
    ProjectDebugSymbols.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location;
        var builtinSymbolSources = (this.state || {}).builtinSymbolSources;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            [
                'debugFiles',
                "/projects/" + orgId + "/" + projectId + "/files/dsyms/",
                {
                    query: {
                        query: location.query.query,
                        file_formats: organization.features.includes('android-mappings')
                            ? ['breakpad', 'macho', 'elf', 'pe', 'pdb', 'sourcebundle']
                            : undefined,
                    },
                },
            ],
        ];
        if (!builtinSymbolSources && organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    };
    ProjectDebugSymbols.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ProjectDebugSymbols.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return t('There are no debug symbols that match your search.');
        }
        return t('There are no debug symbols for this project.');
    };
    ProjectDebugSymbols.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectDebugSymbols.prototype.renderDebugFiles = function () {
        var _this = this;
        var _a = this.state, debugFiles = _a.debugFiles, showDetails = _a.showDetails;
        var _b = this.props, organization = _b.organization, params = _b.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!(debugFiles === null || debugFiles === void 0 ? void 0 : debugFiles.length)) {
            return null;
        }
        return debugFiles.map(function (debugFile) {
            var downloadUrl = _this.api.baseUrl + "/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + debugFile.id;
            return (<DebugFileRow debugFile={debugFile} showDetails={showDetails} downloadUrl={downloadUrl} downloadRole={organization.debugFilesRole} onDelete={_this.handleDelete} key={debugFile.id}/>);
        });
    };
    ProjectDebugSymbols.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, params = _b.params;
        var _c = this.state, loading = _c.loading, showDetails = _c.showDetails, builtinSymbolSources = _c.builtinSymbolSources, debugFiles = _c.debugFiles, debugFilesPageLinks = _c.debugFilesPageLinks;
        var orgId = params.orgId, projectId = params.projectId;
        var features = organization.features, access = organization.access;
        var fieldProps = {
            organization: organization,
            builtinSymbolSources: builtinSymbolSources || [],
        };
        return (<React.Fragment>
        <SettingsPageHeader title={t('Debug Information Files')}/>

        <TextBlock>
          {t("\n            Debug information files are used to convert addresses and minified\n            function names from native crash reports into function names and\n            locations.\n          ")}
        </TextBlock>

        {features.includes('symbol-sources') && (<React.Fragment>
            <PermissionAlert />

            <Form saveOnBlur allowUndo initialData={project} apiMethod="PUT" apiEndpoint={"/projects/" + orgId + "/" + projectId + "/"} onSubmitSuccess={ProjectActions.updateSuccess} key={((_a = project.builtinSymbolSources) === null || _a === void 0 ? void 0 : _a.join()) || project.id}>
              <JsonForm features={new Set(features)} title={t('External Sources')} disabled={!access.includes('project:write')} fields={[fields.symbolSources, fields.builtinSymbolSources]} additionalFieldProps={fieldProps}/>
            </Form>
          </React.Fragment>)}

        <Wrapper>
          <TextBlock noMargin>{t('Uploaded debug information files')}:</TextBlock>

          <Filters>
            <Label>
              <Checkbox checked={showDetails} onChange={function (e) {
            _this.setState({ showDetails: e.target.checked });
        }}/>
              {t('show details')}
            </Label>

            <SearchBar placeholder={t('Search DIFs')} onSearch={this.handleSearch} query={this.getQuery()}/>
          </Filters>
        </Wrapper>

        <StyledPanelTable headers={[
            t('Debug ID'),
            t('Information'),
            <Actions key="actions">{t('Actions')}</Actions>,
        ]} emptyMessage={this.getEmptyMessage()} isEmpty={(debugFiles === null || debugFiles === void 0 ? void 0 : debugFiles.length) === 0} isLoading={loading}>
          {this.renderDebugFiles()}
        </StyledPanelTable>
        <Pagination pageLinks={debugFilesPageLinks}/>
      </React.Fragment>);
    };
    return ProjectDebugSymbols;
}(AsyncView));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: 37% 1fr auto;\n"], ["\n  grid-template-columns: 37% 1fr auto;\n"])));
var Actions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(4), space(4), space(1), function (p) { return p.theme.breakpoints[0]; });
var Filters = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content minmax(200px, 400px);\n  align-items: center;\n  justify-content: flex-end;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: min-content minmax(200px, 400px);\n  align-items: center;\n  justify-content: flex-end;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var Label = styled('label')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-weight: normal;\n  display: flex;\n  margin-bottom: 0;\n  white-space: nowrap;\n  input {\n    margin-top: 0;\n    margin-right: ", ";\n  }\n"], ["\n  font-weight: normal;\n  display: flex;\n  margin-bottom: 0;\n  white-space: nowrap;\n  input {\n    margin-top: 0;\n    margin-right: ", ";\n  }\n"])), space(1));
export default ProjectDebugSymbols;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map