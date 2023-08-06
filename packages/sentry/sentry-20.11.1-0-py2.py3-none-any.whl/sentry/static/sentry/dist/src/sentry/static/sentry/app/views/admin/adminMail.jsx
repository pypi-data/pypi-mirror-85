import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
var AdminMail = /** @class */ (function (_super) {
    __extends(AdminMail, _super);
    function AdminMail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.sendTestEmail = function () { return __awaiter(_this, void 0, void 0, function () {
            var testMailEmail, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        testMailEmail = this.state.data.testMailEmail;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise('/internal/mail/', { method: 'POST' })];
                    case 2:
                        _a.sent();
                        addSuccessMessage(t('A test email has been sent to %s', testMailEmail));
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        addErrorMessage(error_1.responseJSON
                            ? error_1.responseJSON.error
                            : t('Unable to send test email. Check your server logs'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AdminMail.prototype.getEndpoints = function () {
        return [['data', '/internal/mail/']];
    };
    AdminMail.prototype.renderBody = function () {
        var data = this.state.data;
        var mailHost = data.mailHost, mailPassword = data.mailPassword, mailUsername = data.mailUsername, mailPort = data.mailPort, mailUseTls = data.mailUseTls, mailFrom = data.mailFrom, mailListNamespace = data.mailListNamespace, testMailEmail = data.testMailEmail;
        return (<div>
        <h3>{t('SMTP Settings')}</h3>

        <dl className="vars">
          <dt>{t('From Address')}</dt>
          <dd>
            <pre className="val">{mailFrom}</pre>
          </dd>

          <dt>{t('Host')}</dt>
          <dd>
            <pre className="val">
              {mailHost}:{mailPort}
            </pre>
          </dd>

          <dt>{t('Username')}</dt>
          <dd>
            <pre className="val">{mailUsername || <em>{t('not set')}</em>}</pre>
          </dd>

          <dt>{t('Password')}</dt>
          <dd>
            <pre className="val">
              {mailPassword ? '********' : <em>{t('not set')}</em>}
            </pre>
          </dd>

          <dt>{t('TLS?')}</dt>
          <dd>
            <pre className="val">{mailUseTls ? t('Yes') : t('No')}</pre>
          </dd>

          <dt>{t('Mailing List Namespace')}</dt>
          <dd>
            <pre className="val">{mailListNamespace}</pre>
          </dd>
        </dl>

        <h3>{t('Test Settings')}</h3>

        <p>
          {t("Send an email to your account's email address to confirm that everything is configured correctly.")}
        </p>

        <Button onClick={this.sendTestEmail}>
          {t('Send a test email to %s', testMailEmail)}
        </Button>
      </div>);
    };
    return AdminMail;
}(AsyncView));
export default AdminMail;
//# sourceMappingURL=adminMail.jsx.map