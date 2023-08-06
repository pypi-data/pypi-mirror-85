import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import 'prismjs/themes/prism-tomorrow.css';
import { performance as performancePlatforms, } from 'app/data/platformCategories';
import { loadDocs } from 'app/actionCreators/projects';
import { t, tct } from 'app/locale';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Feature from 'app/components/acl/feature';
import { IconInfo } from 'app/icons';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import NotFound from 'app/components/errors/notFound';
import { PageHeader } from 'app/styles/organization';
import Projects from 'app/utils/projects';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import platforms from 'app/data/platforms';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var ProjectInstallPlatform = /** @class */ (function (_super) {
    __extends(ProjectInstallPlatform, _super);
    function ProjectInstallPlatform() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            html: '',
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, params, orgId, projectId, platform, html, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        orgId = params.orgId, projectId = params.projectId, platform = params.platform;
                        this.setState({ loading: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, loadDocs(api, orgId, projectId, platform)];
                    case 2:
                        html = (_b.sent()).html;
                        this.setState({ html: html });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({ error: error_1 });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectInstallPlatform.prototype.componentDidMount = function () {
        this.fetchData();
        window.scrollTo(0, 0);
        var platform = this.props.params.platform;
        //redirect if platform is not known.
        if (!platform || platform === 'other') {
            this.redirectToNeutralDocs();
        }
    };
    Object.defineProperty(ProjectInstallPlatform.prototype, "isGettingStarted", {
        get: function () {
            return window.location.href.indexOf('getting-started') > 0;
        },
        enumerable: false,
        configurable: true
    });
    ProjectInstallPlatform.prototype.redirectToNeutralDocs = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var url = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        browserHistory.push(url);
    };
    ProjectInstallPlatform.prototype.render = function () {
        var _a;
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var platform = platforms.find(function (p) { return p.id === params.platform; });
        if (!platform) {
            return <NotFound />;
        }
        var issueStreamLink = "/organizations/" + orgId + "/issues/";
        var performanceOverviewLink = "/organizations/" + orgId + "/performance/";
        var gettingStartedLink = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        var platformLink = (_a = platform.link) !== null && _a !== void 0 ? _a : undefined;
        return (<React.Fragment>
        <StyledPageHeader>
          <h2>{t('Configure %(platform)s', { platform: platform.name })}</h2>
          <ButtonBar gap={1}>
            <Button size="small" to={gettingStartedLink}>
              {t('< Back')}
            </Button>
            <Button size="small" href={platformLink} external>
              {t('Full Documentation')}
            </Button>
          </ButtonBar>
        </StyledPageHeader>

        <div>
          <Alert type="info" icon={<IconInfo />}>
            {tct("\n             This is a quick getting started guide. For in-depth instructions\n             on integrating Sentry with [platform], view\n             [docLink:our complete documentation].", {
            platform: platform.name,
            docLink: <a href={platformLink}/>,
        })}
          </Alert>

          {this.state.loading ? (<LoadingIndicator />) : this.state.error ? (<LoadingError onRetry={this.fetchData}/>) : (<React.Fragment>
              <SentryDocumentTitle title={t('Configure') + " " + platform.name} objSlug={projectId}/>
              <DocumentationWrapper dangerouslySetInnerHTML={{ __html: this.state.html }}/>
            </React.Fragment>)}

          {this.isGettingStarted && (<Projects key={orgId + "-" + projectId} orgId={orgId} slugs={[projectId]} passthroughPlaceholderProject={false}>
              {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetching = _a.fetching, fetchError = _a.fetchError;
            var projectsLoading = !initiallyLoaded && fetching;
            var projectFilter = !projectsLoading && !fetchError && projects.length
                ? {
                    project: projects[0].id,
                }
                : {};
            var showPerformancePrompt = performancePlatforms.includes(platform.id);
            return (<React.Fragment>
                    {showPerformancePrompt && (<Feature features={['organization:performance-view']} hookName="feature-disabled:performance-new-project">
                        {function (_a) {
                var hasFeature = _a.hasFeature;
                if (hasFeature) {
                    return null;
                }
                return (<StyledAlert type="info" icon={<IconInfo />}>
                              {t("Your selected platform supports performance, but your organization does not have performance enabled.")}
                            </StyledAlert>);
            }}
                      </Feature>)}

                    <StyledButtonBar gap={1}>
                      <Button priority="primary" busy={projectsLoading} to={{
                pathname: issueStreamLink,
                query: projectFilter,
                hash: '#welcome',
            }}>
                        {t('Take me to Issues')}
                      </Button>
                      <Button busy={projectsLoading} to={{
                pathname: performanceOverviewLink,
                query: projectFilter,
            }}>
                        {t('Take me to Performance')}
                      </Button>
                    </StyledButtonBar>
                  </React.Fragment>);
        }}
            </Projects>)}
        </div>
      </React.Fragment>);
    };
    return ProjectInstallPlatform;
}(React.Component));
var DocumentationWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .gatsby-highlight {\n    margin-bottom: ", ";\n\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  .alert {\n    margin-bottom: ", ";\n    border-radius: ", ";\n  }\n\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"], ["\n  .gatsby-highlight {\n    margin-bottom: ", ";\n\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  .alert {\n    margin-bottom: ", ";\n    border-radius: ", ";\n  }\n\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"])), space(3), space(3), function (p) { return p.theme.borderRadius; });
var StyledButtonBar = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[0]; }, space(1));
var StyledPageHeader = styled(PageHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n\n  h2 {\n    margin: 0;\n  }\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n\n    h2 {\n      margin-bottom: ", ";\n    }\n  }\n"], ["\n  margin-bottom: ", ";\n\n  h2 {\n    margin: 0;\n  }\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n\n    h2 {\n      margin-bottom: ", ";\n    }\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[0]; }, space(2));
var StyledAlert = styled(Alert)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
export { ProjectInstallPlatform };
export default withApi(withOrganization(ProjectInstallPlatform));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=platform.jsx.map