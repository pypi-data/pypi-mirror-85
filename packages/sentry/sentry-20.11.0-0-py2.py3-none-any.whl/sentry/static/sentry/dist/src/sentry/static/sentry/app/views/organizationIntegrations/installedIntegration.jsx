import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import CircleIndicator from 'app/components/circleIndicator';
import Confirm from 'app/components/confirm';
import Tooltip from 'app/components/tooltip';
import { IconDelete, IconFlag, IconSettings, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import AddIntegrationButton from './addIntegrationButton';
import IntegrationItem from './integrationItem';
var InstalledIntegration = /** @class */ (function (_super) {
    __extends(InstalledIntegration, _super);
    function InstalledIntegration() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleReAuthIntegration = function (integration) {
            _this.props.onReAuthIntegration(integration);
        };
        _this.handleUninstallClick = function () {
            _this.props.trackIntegrationEvent({
                eventKey: 'integrations.uninstall_clicked',
                eventName: 'Integrations: Uninstall Clicked',
            });
        };
        return _this;
    }
    InstalledIntegration.prototype.getRemovalBodyAndText = function (aspects) {
        if (aspects && aspects.removal_dialog) {
            return {
                body: aspects.removal_dialog.body,
                actionText: aspects.removal_dialog.actionText,
            };
        }
        else {
            return {
                body: t('Deleting this integration will remove any project associated data. This action cannot be undone. Are you sure you want to delete this integration?'),
                actionText: t('Delete'),
            };
        }
    };
    InstalledIntegration.prototype.handleRemove = function (integration) {
        this.props.onRemove(integration);
        this.props.trackIntegrationEvent({
            eventKey: 'integrations.uninstall_completed',
            eventName: 'Integrations: Uninstall Completed',
        });
    };
    Object.defineProperty(InstalledIntegration.prototype, "removeConfirmProps", {
        get: function () {
            var _this = this;
            var integration = this.props.integration;
            var _a = this.getRemovalBodyAndText(integration.provider.aspects), body = _a.body, actionText = _a.actionText;
            var message = (<React.Fragment>
        <Alert type="error" icon={<IconFlag size="md"/>}>
          {t('Deleting this integration has consequences!')}
        </Alert>
        {body}
      </React.Fragment>);
            return {
                message: message,
                confirmText: actionText,
                onConfirm: function () { return _this.handleRemove(integration); },
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InstalledIntegration.prototype, "disableConfirmProps", {
        get: function () {
            var _this = this;
            var integration = this.props.integration;
            var _a = integration.provider.aspects.disable_dialog || {}, body = _a.body, actionText = _a.actionText;
            var message = (<React.Fragment>
        <Alert type="error" icon={<IconFlag size="md"/>}>
          {t('This integration cannot be removed in Sentry')}
        </Alert>
        {body}
      </React.Fragment>);
            return {
                message: message,
                confirmText: actionText,
                onConfirm: function () { return _this.props.onDisable(integration); },
            };
        },
        enumerable: false,
        configurable: true
    });
    InstalledIntegration.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, integration = _a.integration, provider = _a.provider, organization = _a.organization, showReauthMessage = _a.showReauthMessage;
        var removeConfirmProps = integration.status === 'active' && integration.provider.canDisable
            ? this.disableConfirmProps
            : this.removeConfirmProps;
        return (<Access access={['org:integrations']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<IntegrationFlex key={integration.id} className={className}>
            <IntegrationItemBox>
              <IntegrationItem integration={integration}/>
            </IntegrationItemBox>
            <div>
              {showReauthMessage && (<Tooltip disabled={hasAccess} title={t('You must be an organization owner, manager or admin to upgrade')}>
                  <AddIntegrationButton disabled={!hasAccess} provider={provider} onAddIntegration={_this.handleReAuthIntegration} integrationId={integration.id} priority="primary" size="small" buttonText={t('Upgrade Now')} organization={organization} icon={<IconWarning size="sm"/>}/>
                </Tooltip>)}
              <Tooltip disabled={hasAccess} position="left" title={t('You must be an organization owner, manager or admin to configure')}>
                <StyledButton borderless icon={<IconSettings />} disabled={!hasAccess || integration.status !== 'active'} to={"/settings/" + organization.slug + "/integrations/" + provider.key + "/" + integration.id + "/"} data-test-id="integration-configure-button">
                  {t('Configure')}
                </StyledButton>
              </Tooltip>
            </div>
            <div>
              <Tooltip disabled={hasAccess} title={t('You must be an organization owner, manager or admin to uninstall')}>
                <Confirm priority="danger" onConfirming={_this.handleUninstallClick} disabled={!hasAccess} {...removeConfirmProps}>
                  <StyledButton disabled={!hasAccess} borderless icon={<IconDelete />} data-test-id="integration-remove-button">
                    {t('Uninstall')}
                  </StyledButton>
                </Confirm>
              </Tooltip>
            </div>

            <IntegrationStatus status={integration.status}/>
          </IntegrationFlex>);
        }}
      </Access>);
    };
    return InstalledIntegration;
}(React.Component));
export default InstalledIntegration;
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var IntegrationFlex = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IntegrationItemBox = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var IntegrationStatus = styled(function (props) {
    var status = props.status, p = __rest(props, ["status"]);
    var color = status === 'active' ? theme.success : theme.gray300;
    var titleText = status === 'active'
        ? t('This Integration can be disabled by clicking the Uninstall button')
        : t('This Integration has been disconnected from the external provider');
    return (<Tooltip title={titleText}>
        <div {...p}>
          <CircleIndicator size={6} color={color}/>
          <IntegrationStatusText>{"" + (status === 'active' ? t('enabled') : t('disabled'))}</IntegrationStatusText>
        </div>
      </Tooltip>);
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-weight: light;\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-weight: light;\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray200; }, space(1));
var IntegrationStatusText = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0 ", " 0 ", ";\n"], ["\n  margin: 0 ", " 0 ", ";\n"])), space(0.75), space(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=installedIntegration.jsx.map