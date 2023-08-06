import { __extends } from "tslib";
import React from 'react';
import { ApiForm, RadioBooleanField } from 'app/components/forms';
import { tct, t } from 'app/locale';
import NarrowLayout from 'app/components/narrowLayout';
import ExternalLink from 'app/components/links/externalLink';
var NewsletterConsent = /** @class */ (function (_super) {
    __extends(NewsletterConsent, _super);
    function NewsletterConsent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NewsletterConsent.prototype.componentDidMount = function () {
        document.body.classList.add('auth');
    };
    NewsletterConsent.prototype.componentWillUnmount = function () {
        document.body.classList.remove('auth');
    };
    // NOTE: the text here is duplicated within ``RegisterForm`` on the backend
    NewsletterConsent.prototype.render = function () {
        var _this = this;
        return (<NarrowLayout>
        <p>
          {t('Pardon the interruption, we just need to get a quick answer from you.')}
        </p>

        <ApiForm apiMethod="POST" apiEndpoint="/users/me/subscriptions/" onSubmitSuccess={function () { var _a, _b; return (_b = (_a = _this.props).onSubmitSuccess) === null || _b === void 0 ? void 0 : _b.call(_a); }} submitLabel={t('Continue')}>
          <RadioBooleanField key="subscribed" name="subscribed" label={t('Email Updates')} help={<span>
                {tct("We'd love to keep you updated via email with product and feature\n                   announcements, promotions, educational materials, and events. Our updates\n                   focus on relevant information, and we'll never sell your data to third\n                   parties. See our [link:Privacy Policy] for more details.\n                   ", { link: <ExternalLink href="https://sentry.io/privacy/"/> })}
              </span>} yesLabel={t('Yes, I would like to receive updates via email')} noLabel={t("No, I'd prefer not to receive these updates")} required/>
        </ApiForm>
      </NarrowLayout>);
    };
    return NewsletterConsent;
}(React.Component));
export default NewsletterConsent;
//# sourceMappingURL=newsletterConsent.jsx.map