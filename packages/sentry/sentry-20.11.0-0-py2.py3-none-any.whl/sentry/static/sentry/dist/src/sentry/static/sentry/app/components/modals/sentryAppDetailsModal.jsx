import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import PluginIcon from 'app/plugins/components/pluginIcon';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import marked, { singleLineRenderer } from 'app/utils/marked';
import { IconFlag } from 'app/icons';
import Tag from 'app/components/tagDeprecated';
import { toPermissions } from 'app/utils/consolidatedScopes';
import CircleIndicator from 'app/components/circleIndicator';
import { recordInteraction } from 'app/utils/recordSentryAppInteraction';
import { trackIntegrationEvent, getIntegrationFeatureGate, } from 'app/utils/integrationUtil';
//No longer a modal anymore but yea :)
var SentryAppDetailsModal = /** @class */ (function (_super) {
    __extends(SentryAppDetailsModal, _super);
    function SentryAppDetailsModal() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SentryAppDetailsModal.prototype.componentDidUpdate = function (prevProps) {
        //if the user changes org, count this as a fresh event to track
        if (this.props.organization.id !== prevProps.organization.id) {
            this.trackOpened();
        }
    };
    SentryAppDetailsModal.prototype.componentDidMount = function () {
        this.trackOpened();
    };
    SentryAppDetailsModal.prototype.trackOpened = function () {
        var _a = this.props, sentryApp = _a.sentryApp, organization = _a.organization, isInstalled = _a.isInstalled;
        recordInteraction(sentryApp.slug, 'sentry_app_viewed');
        trackIntegrationEvent({
            eventKey: 'integrations.install_modal_opened',
            eventName: 'Integrations: Install Modal Opened',
            integration_type: 'sentry_app',
            integration: sentryApp.slug,
            already_installed: isInstalled,
            view: 'external_install',
            integration_status: sentryApp.status,
        }, organization, { startSession: true });
    };
    SentryAppDetailsModal.prototype.getEndpoints = function () {
        var sentryApp = this.props.sentryApp;
        return [['featureData', "/sentry-apps/" + sentryApp.slug + "/features/"]];
    };
    SentryAppDetailsModal.prototype.featureTags = function (features) {
        return features.map(function (feature) {
            var feat = feature.featureGate.replace(/integrations/g, '');
            return <StyledTag key={feat}>{feat.replace(/-/g, ' ')}</StyledTag>;
        });
    };
    Object.defineProperty(SentryAppDetailsModal.prototype, "permissions", {
        get: function () {
            return toPermissions(this.props.sentryApp.scopes);
        },
        enumerable: false,
        configurable: true
    });
    SentryAppDetailsModal.prototype.onInstall = function () {
        return __awaiter(this, void 0, void 0, function () {
            var onInstall, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        onInstall = this.props.onInstall;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, onInstall()];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    SentryAppDetailsModal.prototype.renderPermissions = function () {
        var permissions = this.permissions;
        if (Object.keys(permissions).filter(function (scope) { return permissions[scope].length > 0; }).length === 0) {
            return null;
        }
        return (<React.Fragment>
        <Title>Permissions</Title>
        {permissions.read.length > 0 && (<Permission>
            <Indicator />
            <Text key="read">
              {tct('[read] access to [resources] resources', {
            read: <strong>Read</strong>,
            resources: permissions.read.join(', '),
        })}
            </Text>
          </Permission>)}
        {permissions.write.length > 0 && (<Permission>
            <Indicator />
            <Text key="write">
              {tct('[read] and [write] access to [resources] resources', {
            read: <strong>Read</strong>,
            write: <strong>Write</strong>,
            resources: permissions.write.join(', '),
        })}
            </Text>
          </Permission>)}
        {permissions.admin.length > 0 && (<Permission>
            <Indicator />
            <Text key="admin">
              {tct('[admin] access to [resources] resources', {
            admin: <strong>Admin</strong>,
            resources: permissions.admin.join(', '),
        })}
            </Text>
          </Permission>)}
      </React.Fragment>);
    };
    SentryAppDetailsModal.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, sentryApp = _a.sentryApp, closeModal = _a.closeModal, isInstalled = _a.isInstalled, organization = _a.organization;
        var featureData = this.state.featureData;
        // Prepare the features list
        var features = (featureData || []).map(function (f) { return ({
            featureGate: f.featureGate,
            description: (<span dangerouslySetInnerHTML={{ __html: singleLineRenderer(f.description) }}/>),
        }); });
        var _b = getIntegrationFeatureGate(), FeatureList = _b.FeatureList, IntegrationFeatures = _b.IntegrationFeatures;
        var overview = sentryApp.overview || '';
        var featureProps = { organization: organization, features: features };
        return (<React.Fragment>
        <Heading>
          <PluginIcon pluginId={sentryApp.slug} size={50}/>

          <HeadingInfo>
            <Name>{sentryApp.name}</Name>
            <div>{features.length && this.featureTags(features)}</div>
          </HeadingInfo>
        </Heading>

        <Description dangerouslySetInnerHTML={{ __html: marked(overview) }}/>
        <FeatureList {...featureProps} provider={__assign(__assign({}, sentryApp), { key: sentryApp.slug })}/>

        <IntegrationFeatures {...featureProps}>
          {function (_a) {
            var disabled = _a.disabled, disabledReason = _a.disabledReason;
            return (<React.Fragment>
              {!disabled && _this.renderPermissions()}
              <Footer>
                <Author>{t('Authored By %s', sentryApp.author)}</Author>
                <div>
                  {disabled && <DisabledNotice reason={disabledReason}/>}
                  <Button size="small" onClick={closeModal}>
                    {t('Cancel')}
                  </Button>

                  <Access organization={organization} access={['org:integrations']}>
                    {function (_a) {
                var hasAccess = _a.hasAccess;
                return hasAccess && (<Button size="small" priority="primary" disabled={isInstalled || disabled} onClick={function () { return _this.onInstall(); }} style={{ marginLeft: space(1) }} data-test-id="install">
                          {t('Accept & Install')}
                        </Button>);
            }}
                  </Access>
                </div>
              </Footer>
            </React.Fragment>);
        }}
        </IntegrationFeatures>
      </React.Fragment>);
    };
    return SentryAppDetailsModal;
}(AsyncComponent));
export default SentryAppDetailsModal;
var Heading = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(1), space(2));
var HeadingInfo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: max-content max-content;\n  grid-gap: ", ";\n  align-items: start;\n"], ["\n  display: grid;\n  grid-template-rows: max-content max-content;\n  grid-gap: ", ";\n  align-items: start;\n"])), space(0.5));
var Name = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n  font-size: 1.4em;\n"], ["\n  font-weight: bold;\n  font-size: 1.4em;\n"])));
var Description = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"], ["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"])), space(2));
var Author = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var DisabledNotice = styled(function (_a) {
    var reason = _a.reason, p = __rest(_a, ["reason"]);
    return (<div {...p}>
    <IconFlag color="red300" size="1.5em"/>
    {reason}
  </div>);
})(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  flex: 1;\n  grid-template-columns: max-content 1fr;\n  color: ", ";\n  font-size: 0.9em;\n"], ["\n  display: grid;\n  align-items: center;\n  flex: 1;\n  grid-template-columns: max-content 1fr;\n  color: ", ";\n  font-size: 0.9em;\n"])), function (p) { return p.theme.red300; });
var StyledTag = styled(Tag)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"], ["\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"])), space(0.5));
var Text = styled('p')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin: 0px 6px;\n"], ["\n  margin: 0px 6px;\n"])));
var Permission = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Footer = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  padding: 20px 30px;\n  border-top: 1px solid #e2dee6;\n  margin: 20px -30px -30px;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  padding: 20px 30px;\n  border-top: 1px solid #e2dee6;\n  margin: 20px -30px -30px;\n  justify-content: space-between;\n"])));
var Title = styled('p')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-weight: bold;\n"], ["\n  margin-bottom: ", ";\n  font-weight: bold;\n"])), space(1));
var Indicator = styled(function (p) { return <CircleIndicator size={7} {...p}/>; })(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-top: 7px;\n  color: ", ";\n"], ["\n  margin-top: 7px;\n  color: ", ";\n"])), function (p) { return p.theme.success; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=sentryAppDetailsModal.jsx.map