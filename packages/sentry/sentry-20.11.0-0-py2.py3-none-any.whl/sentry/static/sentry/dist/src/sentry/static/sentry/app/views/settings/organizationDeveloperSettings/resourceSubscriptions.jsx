import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import SubscriptionBox from 'app/views/settings/organizationDeveloperSettings/subscriptionBox';
import { EVENT_CHOICES, PERMISSIONS_MAP, } from 'app/views/settings/organizationDeveloperSettings/constants';
var Subscriptions = /** @class */ (function (_super) {
    __extends(Subscriptions, _super);
    function Subscriptions(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.onChange = function (resource, checked) {
            var events = new Set(_this.props.events);
            checked ? events.add(resource) : events.delete(resource);
            _this.save(Array.from(events));
        };
        _this.save = function (events) {
            _this.props.onChange(events);
            _this.context.form.setValue('events', events);
        };
        _this.context.form.setValue('events', _this.props.events);
        return _this;
    }
    Subscriptions.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // if webhooks are disabled, unset the events
        if (nextProps.webhookDisabled && this.props.events.length) {
            this.save([]);
        }
    };
    Subscriptions.prototype.componentDidUpdate = function () {
        var _a = this.props, permissions = _a.permissions, events = _a.events;
        var permittedEvents = events.filter(function (resource) { return permissions[PERMISSIONS_MAP[resource]] !== 'no-access'; });
        if (JSON.stringify(events) !== JSON.stringify(permittedEvents)) {
            this.save(permittedEvents);
        }
    };
    Subscriptions.prototype.render = function () {
        var _this = this;
        var _a = this.props, permissions = _a.permissions, webhookDisabled = _a.webhookDisabled, events = _a.events;
        return (<SubscriptionGrid>
        {EVENT_CHOICES.map(function (choice) {
            var disabledFromPermissions = permissions[PERMISSIONS_MAP[choice]] === 'no-access';
            return (<React.Fragment key={choice}>
              <SubscriptionBox key={choice} disabledFromPermissions={disabledFromPermissions} webhookDisabled={webhookDisabled} checked={events.includes(choice) && !disabledFromPermissions} resource={choice} onChange={_this.onChange}/>
            </React.Fragment>);
        })}
      </SubscriptionGrid>);
    };
    Subscriptions.propTypes = {
        permissions: PropTypes.object.isRequired,
        events: PropTypes.array.isRequired,
        onChange: PropTypes.func.isRequired,
        webhookDisabled: PropTypes.bool.isRequired,
    };
    Subscriptions.contextTypes = {
        router: PropTypes.object.isRequired,
        form: PropTypes.object,
    };
    Subscriptions.defaultProps = {
        webhookDisabled: false,
    };
    return Subscriptions;
}(React.Component));
export default Subscriptions;
var SubscriptionGrid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var templateObject_1;
//# sourceMappingURL=resourceSubscriptions.jsx.map