import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import pick from 'lodash/pick';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import { PageContent } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
import routeTitleGen from 'app/utils/routeTitle';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { formatVersion } from 'app/utils/formatters';
import AsyncComponent from 'app/components/asyncComponent';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import LoadingIndicator from 'app/components/loadingIndicator';
import { IconInfo, IconWarning } from 'app/icons';
import space from 'app/styles/space';
import Alert from 'app/components/alert';
import ReleaseHeader from './releaseHeader';
import PickProjectToContinue from './pickProjectToContinue';
import { getReleaseEventView } from './utils';
var ReleaseContext = React.createContext({});
var ReleasesDetail = /** @class */ (function (_super) {
    __extends(ReleasesDetail, _super);
    function ReleasesDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesDetail.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleasesDetail.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { deploys: [] });
    };
    ReleasesDetail.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, params = _a.params, releaseMeta = _a.releaseMeta;
        var query = __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM)))), { health: 1 });
        var basePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/";
        var endpoints = [
            ['release', basePath, { query: query }],
        ];
        if (releaseMeta.deployCount > 0) {
            endpoints.push(['deploys', basePath + "deploys/"]);
        }
        return endpoints;
    };
    ReleasesDetail.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var possiblyWrongProject = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404 || (e === null || e === void 0 ? void 0 : e.status) === 403; });
        if (possiblyWrongProject) {
            return (<PageContent>
          <Alert type="error" icon={<IconWarning />}>
            {t('This release may not be in your selected project.')}
          </Alert>
        </PageContent>);
        }
        return _super.prototype.renderError.apply(this, __spread(args));
    };
    ReleasesDetail.prototype.renderLoading = function () {
        return (<PageContent>
        <LoadingIndicator />
      </PageContent>);
    };
    ReleasesDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, selection = _a.selection, releaseMeta = _a.releaseMeta;
        var _b = this.state, release = _b.release, deploys = _b.deploys, reloading = _b.reloading;
        var project = release === null || release === void 0 ? void 0 : release.projects.find(function (p) { return p.id === selection.projects[0]; });
        var releaseEventView = getReleaseEventView(selection, release === null || release === void 0 ? void 0 : release.version, organization);
        if (!project || !release) {
            if (reloading) {
                return <LoadingIndicator />;
            }
            return null;
        }
        return (<LightWeightNoProjectMessage organization={organization}>
        <StyledPageContent>
          <ReleaseHeader location={location} organization={organization} releaseEventView={releaseEventView} release={release} project={project} releaseMeta={releaseMeta} refetchData={this.fetchData}/>
          <Body>
            <ReleaseContext.Provider value={{
            release: release,
            project: project,
            deploys: deploys,
            releaseMeta: releaseMeta,
            refetchData: this.fetchData,
        }}>
              {this.props.children}
            </ReleaseContext.Provider>
          </Body>
        </StyledPageContent>
      </LightWeightNoProjectMessage>);
    };
    return ReleasesDetail;
}(AsyncView));
var ReleasesDetailContainer = /** @class */ (function (_super) {
    __extends(ReleasesDetailContainer, _super);
    function ReleasesDetailContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesDetailContainer.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        // fetch projects this release belongs to
        return [
            [
                'releaseMeta',
                "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/meta/",
            ],
        ];
    };
    ReleasesDetailContainer.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var has404Errors = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404; });
        if (has404Errors) {
            // This catches a 404 coming from the release endpoint and displays a custom error message.
            return (<PageContent>
          <Alert type="error" icon={<IconWarning />}>
            {t('This release could not be found.')}
          </Alert>
        </PageContent>);
        }
        return _super.prototype.renderError.apply(this, __spread(args));
    };
    ReleasesDetailContainer.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    ReleasesDetailContainer.prototype.renderLoading = function () {
        return (<PageContent>
        <LoadingIndicator />
      </PageContent>);
    };
    ReleasesDetailContainer.prototype.renderProjectsFooterMessage = function () {
        return (<ProjectsFooterMessage>
        <IconInfo size="xs"/> {t('Only projects with this release are visible.')}
      </ProjectsFooterMessage>);
    };
    ReleasesDetailContainer.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, router = _a.router;
        var releaseMeta = this.state.releaseMeta;
        var projects = releaseMeta.projects;
        if (this.isProjectMissingInUrl()) {
            return (<PickProjectToContinue orgSlug={organization.slug} version={params.release} router={router} projects={projects}/>);
        }
        var defaultSelection = {};
        if (organization.features.includes('release-performance-views')) {
            var releaseDate = new Date(releaseMeta.released);
            // Center the release in a 24h time period
            defaultSelection = {
                datetime: {
                    start: new Date(releaseDate.getTime() - 12 * 3600 * 1000),
                    end: new Date(releaseDate.getTime() + 12 * 3600 * 1000),
                    utc: false,
                },
            };
        }
        return (<GlobalSelectionHeader lockedMessageSubject={t('release')} shouldForceProject={projects.length === 1} forceProject={projects.length === 1 ? projects[0] : undefined} specificProjectSlugs={projects.map(function (p) { return p.slug; })} disableMultipleProjectSelection showProjectSettingsLink projectsFooterMessage={this.renderProjectsFooterMessage()} defaultSelection={defaultSelection}>
        <ReleasesDetail {...this.props} releaseMeta={releaseMeta}/>
      </GlobalSelectionHeader>);
    };
    return ReleasesDetailContainer;
}(AsyncComponent));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var ProjectsFooterMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"])), space(1));
var Body = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", " ", ";\n"], ["\n  padding: ", " ", ";\n"])), space(2), space(4));
export { ReleasesDetailContainer, ReleaseContext };
export default withGlobalSelection(withOrganization(ReleasesDetailContainer));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map