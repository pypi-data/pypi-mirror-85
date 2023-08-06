import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import PlatformIcon from 'platformicons';
import { analytics } from 'app/utils/analytics';
import { loadDocs } from 'app/actionCreators/projects';
import { t, tct } from 'app/locale';
import Alert, { alertStyles } from 'app/components/alert';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import FirstEventIndicator from 'app/views/onboarding/projectSetup/firstEventIndicator';
import { IconInfo } from 'app/icons';
import LoadingError from 'app/components/loadingError';
import Panel from 'app/components/panels/panel';
import PanelBody from 'app/components/panels/panelBody';
import platforms from 'app/data/platforms';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import getDynamicText from 'app/utils/getDynamicText';
import withOrganization from 'app/utils/withOrganization';
import testableTransition from 'app/utils/testableTransition';
/**
 * The documentation will include the following string should it be missing the
 * verification example, which currently a lot of docs are.
 */
var INCOMPLETE_DOC_FLAG = 'TODO-ADD-VERIFICATION-EXAMPLE';
var recordAnalyticsDocsClicked = function (_a) {
    var organization = _a.organization, project = _a.project, platform = _a.platform;
    return analytics('onboarding_v2.full_docs_clicked', {
        org_id: organization.id,
        project: project === null || project === void 0 ? void 0 : project.slug,
        platform: platform,
    });
};
var ProjectDocs = /** @class */ (function (_super) {
    __extends(ProjectDocs, _super);
    function ProjectDocs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            platformDocs: null,
            loadedPlatform: null,
            hasError: false,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, platform, platformDocs, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization, platform = _a.platform;
                        if (!project || !platform) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, loadDocs(api, organization.slug, project.slug, platform)];
                    case 2:
                        platformDocs = _b.sent();
                        this.setState({ platformDocs: platformDocs, loadedPlatform: platform, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        if (platform === 'other') {
                            // TODO(epurkhiser): There are currently no docs for the other
                            // platform. We should add generic documentation, in which case, this
                            // check should go away.
                            return [2 /*return*/];
                        }
                        this.setState({ hasError: error_1 });
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFullDocsClick = function () {
            var _a = _this.props, organization = _a.organization, project = _a.project, platform = _a.platform;
            recordAnalyticsDocsClicked({ organization: organization, project: project, platform: platform });
        };
        return _this;
    }
    ProjectDocs.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectDocs.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.platform !== this.props.platform ||
            nextProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    Object.defineProperty(ProjectDocs.prototype, "missingExampleWarning", {
        /**
         * TODO(epurkhiser): This can be removed once all documentation has an
         * example for sending the users first event.
         */
        get: function () {
            var _a;
            var _b = this.state, loadedPlatform = _b.loadedPlatform, platformDocs = _b.platformDocs;
            var missingExample = platformDocs && platformDocs.html.includes(INCOMPLETE_DOC_FLAG);
            if (!missingExample) {
                return null;
            }
            return (<Alert type="warning" icon={<IconInfo size="md"/>}>
        {tct("Looks like this getting started example is still undergoing some\n           work and doesn't include an example for triggering an event quite\n           yet! If you have trouble sending your first event be sure to consult\n           the [docsLink:full documentation] for [platform].", {
                docsLink: <ExternalLink href={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link}/>,
                platform: (_a = platforms.find(function (p) { return p.id === loadedPlatform; })) === null || _a === void 0 ? void 0 : _a.name,
            })}
      </Alert>);
        },
        enumerable: false,
        configurable: true
    });
    ProjectDocs.prototype.render = function () {
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, platform = _b.platform, scrollTargetId = _b.scrollTargetId;
        var _c = this.state, loadedPlatform = _c.loadedPlatform, platformDocs = _c.platformDocs, hasError = _c.hasError;
        var introduction = (<Panel>
        <PanelBody withPadding>
          <PlatformHeading platform={(_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other'}/>

          <Description id={scrollTargetId}>
            {tct("Follow these instructions to install and verify the integration\n               of Sentry into your application, including sending\n               [strong:your first event] from your development environment. See\n               the full documentation for additional configuration, platform\n               features, and methods of sending events.", { strong: <strong /> })}
          </Description>
          <Footer>
            {project && (<FirstEventIndicator organization={organization} project={project} eventType="error"/>)}
            <div>
              <Button external onClick={this.handleFullDocsClick} href={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link} size="small">
                {t('Full Documentation')}
              </Button>
            </div>
          </Footer>
        </PanelBody>
      </Panel>);
        var docs = platformDocs !== null && (<DocsContainer>
        <AnimatePresence>
          <DocsWrapper key={platformDocs.html}>
            <div dangerouslySetInnerHTML={{ __html: platformDocs.html }}/>
            {this.missingExampleWarning}
          </DocsWrapper>
        </AnimatePresence>
      </DocsContainer>);
        var loadingError = (<LoadingError message={t('Failed to load documentation for the %s platform.', platform)} onRetry={this.fetchData}/>);
        var testOnlyAlert = (<Alert type="warning">
        Platform documentation is not rendered in for tests in CI
      </Alert>);
        return (<React.Fragment>
        {introduction}
        {getDynamicText({
            value: !hasError ? docs : loadingError,
            fixed: testOnlyAlert,
        })}
      </React.Fragment>);
    };
    return ProjectDocs;
}(React.Component));
var docsTransition = {
    initial: {
        opacity: 0,
        y: -10,
    },
    animate: {
        opacity: 1,
        y: 0,
        delay: 0.1,
        transition: { duration: 0.2 },
    },
    exit: {
        opacity: 0,
        y: 10,
        transition: { duration: 0.2 },
    },
    transition: testableTransition(),
};
var Description = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 0.9em;\n"], ["\n  font-size: 0.9em;\n"])));
var Footer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n"])), space(1));
var HeadingContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n"], ["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n"])));
var Heading = styled(motion.div)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n  grid-column: 1;\n  grid-row: 1;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n  grid-column: 1;\n  grid-row: 1;\n"])), space(1), space(2));
Heading.defaultProps = __assign({}, docsTransition);
var Header = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 1.8rem;\n  margin-right: 16px;\n  font-weight: bold;\n"], ["\n  font-size: 1.8rem;\n  margin-right: 16px;\n  font-weight: bold;\n"])));
var PlatformHeading = function (_a) {
    var _b, _c;
    var platform = _a.platform;
    return (<HeadingContainer>
    <AnimatePresence initial={false}>
      <Heading key={platform}>
        <PlatformIcon platform={platform} size={24}/>
        <Header>
          {t('%s SDK Installation Guide', (_c = (_b = platforms.find(function (p) { return p.id === platform; })) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : t('Unknown'))}
        </Header>
      </Heading>
    </AnimatePresence>
  </HeadingContainer>);
};
PlatformHeading.propTypes = {
    platform: PropTypes.string.isRequired,
};
var getAlertClass = function (type) { return (type === 'muted' ? 'alert' : "alert-" + type); };
var mapAlertStyles = function (p, type) {
    return css(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n    .", " {\n      ", ";\n      display: block;\n    }\n  "], ["\n    .", " {\n      ", ";\n      display: block;\n    }\n  "])), getAlertClass(type), alertStyles({ theme: p.theme, type: type }));
};
var DocsContainer = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n"], ["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n"])));
var DocsWrapper = styled(motion.div)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-column: 1;\n  grid-row: 1;\n\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6,\n  p {\n    margin-bottom: 18px;\n  }\n\n  code {\n    font-size: 87.5%;\n    color: #e83e8c;\n  }\n\n  pre code {\n    color: inherit;\n    font-size: inherit;\n    white-space: pre;\n  }\n\n  h2 {\n    font-size: 1.4em;\n  }\n\n  .alert h5 {\n    font-size: 1em;\n    margin-bottom: 1rem;\n  }\n\n  /**\n   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts\n   */\n  .content-flush-bottom *:last-child {\n    margin-bottom: 0;\n  }\n\n  ", "\n"], ["\n  grid-column: 1;\n  grid-row: 1;\n\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6,\n  p {\n    margin-bottom: 18px;\n  }\n\n  code {\n    font-size: 87.5%;\n    color: #e83e8c;\n  }\n\n  pre code {\n    color: inherit;\n    font-size: inherit;\n    white-space: pre;\n  }\n\n  h2 {\n    font-size: 1.4em;\n  }\n\n  .alert h5 {\n    font-size: 1em;\n    margin-bottom: 1rem;\n  }\n\n  /**\n   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts\n   */\n  .content-flush-bottom *:last-child {\n    margin-bottom: 0;\n  }\n\n  ", "\n"])), function (p) { return Object.keys(p.theme.alert).map(function (type) { return mapAlertStyles(p, type); }); });
DocsWrapper.defaultProps = __assign({}, docsTransition);
export default withOrganization(withApi(ProjectDocs));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=projectDocs.jsx.map