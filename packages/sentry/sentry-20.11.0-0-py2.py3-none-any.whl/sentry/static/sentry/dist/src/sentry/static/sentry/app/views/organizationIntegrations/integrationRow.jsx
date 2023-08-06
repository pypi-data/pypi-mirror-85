import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import startCase from 'lodash/startCase';
import { IconWarning } from 'app/icons';
import Button from 'app/components/button';
import Alert from 'app/components/alert';
import Link from 'app/components/links/link';
import { PanelItem } from 'app/components/panels';
import PluginIcon from 'app/plugins/components/pluginIcon';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { trackIntegrationEvent, convertIntegrationTypeToSnakeCase, } from 'app/utils/integrationUtil';
import IntegrationStatus from './integrationStatus';
var urlMap = {
    plugin: 'plugins',
    firstParty: 'integrations',
    sentryApp: 'sentry-apps',
    documentIntegration: 'document-integrations',
};
var IntegrationRow = function (props) {
    var organization = props.organization, type = props.type, slug = props.slug, displayName = props.displayName, status = props.status, publishStatus = props.publishStatus, configurations = props.configurations, categories = props.categories, alertText = props.alertText;
    var baseUrl = publishStatus === 'internal'
        ? "/settings/" + organization.slug + "/developer-settings/" + slug + "/"
        : "/settings/" + organization.slug + "/" + urlMap[type] + "/" + slug + "/";
    var renderDetails = function () {
        if (type === 'sentryApp') {
            return publishStatus !== 'published' && <PublishStatus status={publishStatus}/>;
        }
        //TODO: Use proper translations
        return configurations > 0 ? (<StyledLink to={baseUrl + "?tab=configurations"}>{configurations + " Configuration" + (configurations > 1 ? 's' : '')}</StyledLink>) : null;
    };
    var renderStatus = function () {
        //status should be undefined for document integrations
        if (status) {
            return <IntegrationStatus status={status}/>;
        }
        return <LearnMore to={baseUrl}>{t('Learn More')}</LearnMore>;
    };
    return (<PanelItem p={0} flexDirection="column" data-test-id={slug}>
      <FlexContainer>
        <PluginIcon size={36} pluginId={slug}/>
        <Container>
          <IntegrationName to={baseUrl}>{displayName}</IntegrationName>
          <IntegrationDetails>
            {renderStatus()}
            {renderDetails()}
          </IntegrationDetails>
        </Container>
        <InternalContainer>
          {categories === null || categories === void 0 ? void 0 : categories.map(function (category) { return (<CategoryTag key={category} category={startCase(category)} priority={category === publishStatus}/>); })}
        </InternalContainer>
      </FlexContainer>
      {alertText && (<AlertContainer>
          <Alert type="warning" icon={<IconWarning size="sm"/>}>
            <span>{alertText}</span>
            <ResolveNowButton href={baseUrl + "?tab=configurations&referrer=directory_resolve_now"} size="xsmall" onClick={function () {
        return trackIntegrationEvent({
            eventKey: 'integrations.resolve_now_clicked',
            eventName: 'Integrations: Resolve Now Clicked',
            integration_type: convertIntegrationTypeToSnakeCase(type),
            integration: slug,
        }, organization);
    }}>
              {t('Resolve Now')}
            </ResolveNowButton>
          </Alert>
        </AlertContainer>)}
    </PanelItem>);
};
var FlexContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space(2));
var InternalContainer = styled(FlexContainer)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 0 ", ";\n"], ["\n  padding: 0 ", ";\n"])), space(2));
var Container = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex: 1;\n  padding: 0 16px;\n"], ["\n  flex: 1;\n  padding: 0 16px;\n"])));
var IntegrationName = styled(Link)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.blue300; });
var IntegrationDetails = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"], ["\n  display: flex;\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"])));
var StyledLink = styled(Link)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"], ["\n  color: ", ";\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray200; }, space(0.75));
var LearnMore = styled(Link)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var PublishStatus = styled(function (_a) {
    var status = _a.status, props = __rest(_a, ["status"]);
    return (<div {...props}>{t("" + status)}</div>);
})(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: light;\n  margin-right: ", ";\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"], ["\n  color: ",
    ";\n  font-weight: light;\n  margin-right: ", ";\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"])), function (props) {
    return props.status === 'published' ? props.theme.success : props.theme.gray300;
}, space(0.75), function (p) { return p.theme.gray200; }, space(0.75));
var CategoryTag = styled(function (_a) {
    var _priority = _a.priority, category = _a.category, p = __rest(_a, ["priority", "category"]);
    return <div {...p}>{category}</div>;
})(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  padding: 1px 10px;\n  background: ", ";\n  border-radius: 20px;\n  font-size: ", ";\n  margin-right: ", ";\n  line-height: ", ";\n  text-align: center;\n  color: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  padding: 1px 10px;\n  background: ", ";\n  border-radius: 20px;\n  font-size: ", ";\n  margin-right: ", ";\n  line-height: ", ";\n  text-align: center;\n  color: ", ";\n"])), function (p) { return (p.priority ? p.theme.purple200 : p.theme.gray100); }, space(1.5), space(1), space(3), function (p) { return (p.priority ? p.theme.white : p.theme.gray500); });
var ResolveNowButton = styled(Button)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  color: ", ";\n  float: right;\n"], ["\n  color: ", ";\n  float: right;\n"])), function (p) { return p.theme.subText; });
var AlertContainer = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  padding: 0px ", " 0px 68px;\n"], ["\n  padding: 0px ", " 0px 68px;\n"])), space(3));
export default IntegrationRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=integrationRow.jsx.map