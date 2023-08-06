import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Hovercard from 'app/components/hovercard';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import { OnboardingTaskKey } from 'app/types';
import { updateOnboardingTask } from 'app/actionCreators/onboardingTasks';
var OnboardingHovercard = /** @class */ (function (_super) {
    __extends(OnboardingHovercard, _super);
    function OnboardingHovercard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dismissed: false,
        };
        _this.skipTask = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            updateOnboardingTask(api, organization, {
                task: OnboardingTaskKey.ALERT_RULE,
                status: 'complete',
                data: { accepted_defaults: true },
            });
            _this.setState({ dismissed: true });
        };
        return _this;
    }
    Object.defineProperty(OnboardingHovercard.prototype, "shouldShowHovercard", {
        get: function () {
            var _a;
            var organization = this.props.organization;
            var dismissed = this.state.dismissed;
            var hasCompletedTask = organization.onboardingTasks.find(function (task) { return task.task === OnboardingTaskKey.ALERT_RULE && task.status === 'complete'; });
            var query = ((_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) || {};
            return (!hasCompletedTask &&
                !dismissed &&
                Object.prototype.hasOwnProperty.call(query, 'onboardingTask'));
        },
        enumerable: false,
        configurable: true
    });
    OnboardingHovercard.prototype.render = function () {
        var _a = this.props, children = _a.children, _org = _a.organization, _location = _a.location, props = __rest(_a, ["children", "organization", "location"]);
        if (!this.shouldShowHovercard) {
            return children;
        }
        var hovercardBody = (<HovercardBody>
        <h1>{t('Configure custom alerting')}</h1>

        <p>
          {t("Add custom alert rules to configure under what conditions\n             you receive notifications from Sentry.")}
        </p>

        <Button size="xsmall" onClick={this.skipTask}>
          {t('The default rule looks good!')}
        </Button>
      </HovercardBody>);
        return (<Hovercard show position="left" body={hovercardBody} {...props}>
        {children}
      </Hovercard>);
    };
    return OnboardingHovercard;
}(React.Component));
var HovercardBody = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  h1 {\n    font-size: ", ";\n    margin-bottom: ", ";\n  }\n  p {\n    font-size: ", ";\n  }\n"], ["\n  h1 {\n    font-size: ", ";\n    margin-bottom: ", ";\n  }\n  p {\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space(1.5), function (p) { return p.theme.fontSizeMedium; });
export default withApi(OnboardingHovercard);
var templateObject_1;
//# sourceMappingURL=onboardingHovercard.jsx.map