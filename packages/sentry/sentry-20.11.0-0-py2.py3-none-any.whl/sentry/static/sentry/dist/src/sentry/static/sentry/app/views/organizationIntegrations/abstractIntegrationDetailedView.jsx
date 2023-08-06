import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import startCase from 'lodash/startCase';
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import ExternalLink from 'app/components/links/externalLink';
import { Panel } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconClose, IconDocs, IconGeneric, IconGithub, IconProject } from 'app/icons';
import { t } from 'app/locale';
import PluginIcon from 'app/plugins/components/pluginIcon';
import space from 'app/styles/space';
import { getCategories, getIntegrationFeatureGate, trackIntegrationEvent, } from 'app/utils/integrationUtil';
import marked, { singleLineRenderer } from 'app/utils/marked';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Tag from 'app/components/tagDeprecated';
import IntegrationStatus from './integrationStatus';
import RequestIntegrationButton from './integrationRequest/RequestIntegrationButton';
var AbstractIntegrationDetailedView = /** @class */ (function (_super) {
    __extends(AbstractIntegrationDetailedView, _super);
    function AbstractIntegrationDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tabs = ['overview', 'configurations'];
        _this.onTabChange = function (value) {
            _this.trackIntegrationEvent({
                eventKey: 'integrations.integration_tab_clicked',
                eventName: 'Integrations: Integration Tab Clicked',
                integration_tab: value,
            });
            _this.setState({ tab: value });
        };
        //Wrapper around trackIntegrationEvent that automatically provides many fields and the org
        _this.trackIntegrationEvent = function (options) {
            //If we use this intermediate type we get type checking on the things we care about
            var params = __assign({ view: 'integrations_directory_integration_detail', integration: _this.integrationSlug, integration_type: _this.integrationType, already_installed: _this.installationStatus !== 'Not Installed' }, options);
            //type cast here so TS won't complain
            var typeCasted = params;
            trackIntegrationEvent(typeCasted, _this.props.organization);
        };
        return _this;
    }
    AbstractIntegrationDetailedView.prototype.componentDidMount = function () {
        var location = this.props.location;
        var value = location.query.tab === 'configurations' ? 'configurations' : 'overview';
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState({ tab: value });
    };
    AbstractIntegrationDetailedView.prototype.onLoadAllEndpointsSuccess = function () {
        this.trackIntegrationEvent({
            eventKey: 'integrations.integration_viewed',
            eventName: 'Integrations: Integration Viewed',
            integration_tab: this.state.tab,
        });
    };
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "integrationType", {
        /***
         * Abstract methods defined below
         */
        //The analytics type used in analytics which is snake case
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "description", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "author", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "alerts", {
        get: function () {
            //default is no alerts
            return [];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "resourceLinks", {
        //Returns a list of the resources displayed at the bottom of the overview card
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "installationStatus", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "integrationName", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "featureData", {
        // Returns an array of RawIntegrationFeatures which is used in feature gating
        // and displaying what the integration does
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    AbstractIntegrationDetailedView.prototype.getIcon = function (title) {
        switch (title) {
            case 'View Source':
                return <IconProject />;
            case 'Report Issue':
                return <IconGithub />;
            case 'Documentation':
            case 'Splunk Setup Instructions':
            case 'Trello Setup Instructions':
                return <IconDocs />;
            default:
                return <IconGeneric />;
        }
    };
    //Returns the string that is shown as the title of a tab
    AbstractIntegrationDetailedView.prototype.getTabDisplay = function (tab) {
        //default is return the tab
        return tab;
    };
    //Render the button at the top which is usually just an installation button
    AbstractIntegrationDetailedView.prototype.renderTopButton = function (_disabledFromFeatures, //from the feature gate
    _userHasAccess //from user permissions
    ) {
        // Allow children to implement this
        throw new Error('Not implemented');
    };
    //Returns the permission descriptions, only use by Sentry Apps
    AbstractIntegrationDetailedView.prototype.renderPermissions = function () {
        //default is don't render permissions
        return null;
    };
    AbstractIntegrationDetailedView.prototype.renderEmptyConfigurations = function () {
        return (<Panel>
        <EmptyMessage title={t("You haven't set anything up yet")} description={t('But that doesn’t have to be the case for long! Add an installation to get started.')} action={this.renderAddInstallButton(true)}/>
      </Panel>);
    };
    //Returns the list of configurations for the integration
    AbstractIntegrationDetailedView.prototype.renderConfigurations = function () {
        // Allow children to implement this
        throw new Error('Not implemented');
    };
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "integrationSlug", {
        /***
         * Actually implemented methods below
         */
        get: function () {
            return this.props.params.integrationSlug;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "featureProps", {
        //Returns the props as needed by the hooks integrations:feature-gates
        get: function () {
            var organization = this.props.organization;
            var featureData = this.featureData;
            // Prepare the features list
            var features = featureData.map(function (f) { return ({
                featureGate: f.featureGate,
                description: (<FeatureListItem dangerouslySetInnerHTML={{ __html: singleLineRenderer(f.description) }}/>),
            }); });
            return { organization: organization, features: features };
        },
        enumerable: false,
        configurable: true
    });
    AbstractIntegrationDetailedView.prototype.cleanTags = function () {
        return getCategories(this.featureData);
    };
    AbstractIntegrationDetailedView.prototype.renderRequestIntegrationButton = function () {
        return (<RequestIntegrationButton organization={this.props.organization} name={this.integrationName} slug={this.integrationSlug} type={this.integrationType}/>);
    };
    AbstractIntegrationDetailedView.prototype.renderAddInstallButton = function (hideButtonIfDisabled) {
        var _this = this;
        if (hideButtonIfDisabled === void 0) { hideButtonIfDisabled = false; }
        var organization = this.props.organization;
        var IntegrationDirectoryFeatures = getIntegrationFeatureGate().IntegrationDirectoryFeatures;
        return (<IntegrationDirectoryFeatures {...this.featureProps}>
        {function (_a) {
            var disabled = _a.disabled, disabledReason = _a.disabledReason;
            return (<DisableWrapper>
            <Access organization={organization} access={['org:integrations']}>
              {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<Tooltip title={t('You must be an organization owner, manager or admin to install this.')} disabled={hasAccess}>
                  {!hideButtonIfDisabled && disabled ? (<div />) : (_this.renderTopButton(disabled, hasAccess))}
                </Tooltip>);
            }}
            </Access>
            {disabled && <DisabledNotice reason={disabledReason}/>}
          </DisableWrapper>);
        }}
      </IntegrationDirectoryFeatures>);
    };
    //Returns the content shown in the top section of the integration detail
    AbstractIntegrationDetailedView.prototype.renderTopSection = function () {
        var tags = this.cleanTags();
        return (<Flex>
        <PluginIcon pluginId={this.integrationSlug} size={50}/>
        <NameContainer>
          <Flex>
            <Name>{this.integrationName}</Name>
            <StatusWrapper>
              {this.installationStatus && (<IntegrationStatus status={this.installationStatus}/>)}
            </StatusWrapper>
          </Flex>
          <Flex>
            {tags.map(function (feature) { return (<StyledTag key={feature}>{startCase(feature)}</StyledTag>); })}
          </Flex>
        </NameContainer>
        {this.renderAddInstallButton()}
      </Flex>);
    };
    //Returns the tabs divider with the clickable tabs
    AbstractIntegrationDetailedView.prototype.renderTabs = function () {
        var _this = this;
        //TODO: Convert to styled component
        return (<ul className="nav nav-tabs border-bottom" style={{ paddingTop: '30px' }}>
        {this.tabs.map(function (tabName) { return (<li key={tabName} className={_this.state.tab === tabName ? 'active' : ''} onClick={function () { return _this.onTabChange(tabName); }}>
            <CapitalizedLink>{t(_this.getTabDisplay(tabName))}</CapitalizedLink>
          </li>); })}
      </ul>);
    };
    //Returns the information about the integration description and features
    AbstractIntegrationDetailedView.prototype.renderInformationCard = function () {
        var _this = this;
        var IntegrationDirectoryFeatureList = getIntegrationFeatureGate().IntegrationDirectoryFeatureList;
        return (<React.Fragment>
        <Flex>
          <FlexContainer>
            <Description dangerouslySetInnerHTML={{ __html: marked(this.description) }}/>
            <IntegrationDirectoryFeatureList {...this.featureProps} provider={{ key: this.props.params.integrationSlug }}/>
            {this.renderPermissions()}
            {this.alerts.map(function (alert, i) { return (<Alert key={i} type={alert.type} icon={alert.icon}>
                <span dangerouslySetInnerHTML={{ __html: singleLineRenderer(alert.text) }}/>
              </Alert>); })}
          </FlexContainer>
          <Metadata>
            {!!this.author && (<AuthorInfo>
                <CreatedContainer>{t('Created By')}</CreatedContainer>
                <div>{this.author}</div>
              </AuthorInfo>)}
            {this.resourceLinks.map(function (_a) {
            var title = _a.title, url = _a.url;
            return (<ExternalLinkContainer key={url}>
                {_this.getIcon(title)}
                <ExternalLink href={url}>{t(title)}</ExternalLink>
              </ExternalLinkContainer>);
        })}
          </Metadata>
        </Flex>
      </React.Fragment>);
    };
    AbstractIntegrationDetailedView.prototype.renderBody = function () {
        return (<React.Fragment>
        {this.renderTopSection()}
        {this.renderTabs()}
        {this.state.tab === 'overview'
            ? this.renderInformationCard()
            : this.renderConfigurations()}
      </React.Fragment>);
    };
    return AbstractIntegrationDetailedView;
}(AsyncComponent));
var Flex = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var FlexContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var CapitalizedLink = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-transform: capitalize;\n"], ["\n  text-transform: capitalize;\n"])));
var StyledTag = styled(Tag)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-transform: none;\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"], ["\n  text-transform: none;\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"])), space(0.5));
var NameContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  flex-direction: column;\n  justify-content: center;\n  padding-left: ", ";\n"], ["\n  display: flex;\n  align-items: flex-start;\n  flex-direction: column;\n  justify-content: center;\n  padding-left: ", ";\n"])), space(2));
var Name = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-weight: bold;\n  font-size: 1.4em;\n  margin-bottom: ", ";\n"], ["\n  font-weight: bold;\n  font-size: 1.4em;\n  margin-bottom: ", ";\n"])), space(1));
var IconCloseCircle = styled(IconClose)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.red300; }, space(1));
var DisabledNotice = styled(function (_a) {
    var reason = _a.reason, p = __rest(_a, ["reason"]);
    return (<div style={{
        display: 'flex',
        alignItems: 'center',
    }} {...p}>
    <IconCloseCircle isCircled/>
    <span>{reason}</span>
  </div>);
})(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  padding-top: ", ";\n  font-size: 0.9em;\n"], ["\n  padding-top: ", ";\n  font-size: 0.9em;\n"])), space(0.5));
var FeatureListItem = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  line-height: 24px;\n"], ["\n  line-height: 24px;\n"])));
var Description = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"], ["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"])), space(2));
var Metadata = styled(Flex)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  font-size: 0.9em;\n  margin-left: ", ";\n  margin-right: 100px;\n"], ["\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  font-size: 0.9em;\n  margin-left: ", ";\n  margin-right: 100px;\n"])), space(2), space(4));
var AuthorInfo = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var ExternalLinkContainer = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var StatusWrapper = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  padding-left: ", ";\n  line-height: 1.5em;\n"], ["\n  margin-bottom: ", ";\n  padding-left: ", ";\n  line-height: 1.5em;\n"])), space(1), space(2));
var DisableWrapper = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
var CreatedContainer = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  text-transform: uppercase;\n  padding-bottom: ", ";\n  color: ", ";\n  font-weight: 600;\n  font-size: 12px;\n"], ["\n  text-transform: uppercase;\n  padding-bottom: ", ";\n  color: ", ";\n  font-weight: 600;\n  font-size: 12px;\n"])), space(1), function (p) { return p.theme.gray300; });
export default AbstractIntegrationDetailedView;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=abstractIntegrationDetailedView.jsx.map