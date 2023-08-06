import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { DESCRIPTIONS, } from 'app/views/settings/organizationDeveloperSettings/constants';
import Checkbox from 'app/components/checkbox';
import Tooltip from 'app/components/tooltip';
import withOrganization from 'app/utils/withOrganization';
import SentryTypes from 'app/sentryTypes';
var SubscriptionBox = /** @class */ (function (_super) {
    __extends(SubscriptionBox, _super);
    function SubscriptionBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (evt) {
            var checked = evt.target.checked;
            var resource = _this.props.resource;
            _this.props.onChange(resource, checked);
        };
        return _this;
    }
    SubscriptionBox.prototype.render = function () {
        var _a = this.props, resource = _a.resource, organization = _a.organization, webhookDisabled = _a.webhookDisabled, checked = _a.checked;
        var features = new Set(organization.features);
        var disabled = this.props.disabledFromPermissions || webhookDisabled;
        var message = "Must have at least 'Read' permissions enabled for " + resource;
        if (resource === 'error' && !features.has('integrations-event-hooks')) {
            disabled = true;
            message =
                'Your organization does not have access to the error subscription resource.';
        }
        if (webhookDisabled) {
            message = 'Cannot enable webhook subscription without specifying a webhook url';
        }
        return (<React.Fragment>
        <SubscriptionGridItemWrapper key={resource}>
          <Tooltip disabled={!disabled} title={message}>
            <SubscriptionGridItem disabled={disabled}>
              <SubscriptionInfo>
                <SubscriptionTitle>{t("" + resource)}</SubscriptionTitle>
                <SubscriptionDescription>
                  {t("" + DESCRIPTIONS[resource])}
                </SubscriptionDescription>
              </SubscriptionInfo>
              <Checkbox key={"" + resource + checked} disabled={disabled} id={resource} value={resource} checked={checked} onChange={this.onChange}/>
            </SubscriptionGridItem>
          </Tooltip>
        </SubscriptionGridItemWrapper>
      </React.Fragment>);
    };
    SubscriptionBox.propTypes = {
        resource: PropTypes.string.isRequired,
        disabledFromPermissions: PropTypes.bool.isRequired,
        webhookDisabled: PropTypes.bool.isRequired,
        checked: PropTypes.bool.isRequired,
        onChange: PropTypes.func.isRequired,
        organization: SentryTypes.Organization,
    };
    SubscriptionBox.defaultProps = {
        webhookDisabled: false,
    };
    return SubscriptionBox;
}(React.Component));
export { SubscriptionBox };
export default withOrganization(SubscriptionBox);
var SubscriptionInfo = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var SubscriptionGridItem = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  background: ", ";\n  opacity: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"], ["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  background: ", ";\n  opacity: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"])), function (p) { return p.theme.backgroundSecondary; }, function (_a) {
    var disabled = _a.disabled;
    return (disabled ? 0.3 : 1);
});
var SubscriptionGridItemWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 12px;\n  width: 33%;\n"], ["\n  padding: 12px;\n  width: 33%;\n"])));
var SubscriptionDescription = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 12px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n"], ["\n  font-size: 12px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.gray300; });
var SubscriptionTitle = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 16px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n  margin-bottom: 5px;\n"], ["\n  font-size: 16px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n  margin-bottom: 5px;\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=subscriptionBox.jsx.map