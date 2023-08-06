import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import groupBy from 'lodash/groupBy';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import DateTime from 'app/components/dateTime';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import Switch from 'app/components/switch';
import space from 'app/styles/space';
import TextBlock from 'app/views/settings/components/text/textBlock';
import { IconToggle } from 'app/icons';
var ENDPOINT = '/users/me/subscriptions/';
var AccountSubscriptions = /** @class */ (function (_super) {
    __extends(AccountSubscriptions, _super);
    function AccountSubscriptions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleToggle = function (subscription, index, _e) {
            var subscribed = !subscription.subscribed;
            var oldSubscriptions = _this.state.subscriptions;
            _this.setState(function (state) {
                var newSubscriptions = state.subscriptions.slice();
                newSubscriptions[index] = __assign(__assign({}, subscription), { subscribed: subscribed, subscribedDate: new Date().toString() });
                return __assign(__assign({}, state), { subscriptions: newSubscriptions });
            });
            _this.api.request(ENDPOINT, {
                method: 'PUT',
                data: {
                    listId: subscription.listId,
                    subscribed: subscribed,
                },
                success: function () {
                    addSuccessMessage((subscribed ? 'Subscribed' : 'Unsubscribed') + " to " + subscription.listName);
                },
                error: function () {
                    addErrorMessage("Unable to " + (subscribed ? '' : 'un') + "subscribe to " + subscription.listName);
                    _this.setState({ subscriptions: oldSubscriptions });
                },
            });
        };
        return _this;
    }
    AccountSubscriptions.prototype.getEndpoints = function () {
        return [['subscriptions', ENDPOINT]];
    };
    AccountSubscriptions.prototype.getTitle = function () {
        return 'Subscriptions';
    };
    AccountSubscriptions.prototype.renderBody = function () {
        var _this = this;
        var subGroups = Object.entries(groupBy(this.state.subscriptions, function (sub) { return sub.email; }));
        return (<div>
        <SettingsPageHeader title="Subscriptions"/>
        <TextBlock>
          {t("Sentry is committed to respecting your inbox. Our goal is to\n              provide useful content and resources that make fixing errors less\n              painful. Enjoyable even.")}
        </TextBlock>

        <TextBlock>
          {t("As part of our compliance with the EU\u2019s General Data Protection\n              Regulation (GDPR), starting on 25 May 2018, we\u2019ll only email you\n              according to the marketing categories to which you\u2019ve explicitly\n              opted-in.")}
        </TextBlock>

        <Panel>
          {this.state.subscriptions.length ? (<div>
              <PanelHeader>{t('Subscription')}</PanelHeader>
              <PanelBody>
                {subGroups.map(function (_a) {
            var _b = __read(_a, 2), email = _b[0], subscriptions = _b[1];
            return (<React.Fragment key={email}>
                    {subGroups.length > 1 && (<Heading>
                        <IconToggle /> {t('Subscriptions for %s', email)}
                      </Heading>)}

                    {subscriptions.map(function (subscription, index) { return (<PanelItem p={2} alignItems="center" key={subscription.listId}>
                        <SubscriptionDetails>
                          <SubscriptionName>{subscription.listName}</SubscriptionName>
                          {subscription.listDescription && (<Description>{subscription.listDescription}</Description>)}
                          {subscription.subscribed ? (<SubscribedDescription>
                              <div>
                                {tct('[email] on [date]', {
                email: subscription.email,
                date: (<DateTime shortDate date={moment(subscription.subscribedDate)}/>),
            })}
                              </div>
                            </SubscribedDescription>) : (<SubscribedDescription>
                              {t('Not currently subscribed')}
                            </SubscribedDescription>)}
                        </SubscriptionDetails>
                        <div>
                          <Switch isActive={subscription.subscribed} size="lg" toggle={_this.handleToggle.bind(_this, subscription, index)}/>
                        </div>
                      </PanelItem>); })}
                  </React.Fragment>);
        })}
              </PanelBody>
            </div>) : (<EmptyMessage>{t("There's no subscription backend present.")}</EmptyMessage>)}
        </Panel>
        <TextBlock>
          {t("We\u2019re applying GDPR consent and privacy policies to all Sentry\n              contacts, regardless of location. You\u2019ll be able to manage your\n              subscriptions here and from an Unsubscribe link in the footer of\n              all marketing emails.")}
        </TextBlock>

        <TextBlock>
          {tct('Please contact [email:learn@sentry.io] with any questions or suggestions.', { email: <a href="mailto:learn@sentry.io"/> })}
        </TextBlock>
      </div>);
    };
    return AccountSubscriptions;
}(AsyncView));
var Heading = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  padding: ", " ", ";\n  background: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  padding: ", " ", ";\n  background: ", ";\n  color: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeMedium; }, space(1.5), space(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; });
var SubscriptionDetails = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 50%;\n  padding-right: ", ";\n"], ["\n  width: 50%;\n  padding-right: ", ";\n"])), space(2));
var SubscriptionName = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var Description = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(0.75), function (p) { return p.theme.subText; });
var SubscribedDescription = styled(Description)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
export default AccountSubscriptions;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=accountSubscriptions.jsx.map