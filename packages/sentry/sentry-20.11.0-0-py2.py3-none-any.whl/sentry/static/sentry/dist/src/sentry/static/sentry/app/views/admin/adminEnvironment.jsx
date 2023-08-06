import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import moment from 'moment';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import ConfigStore from 'app/stores/configStore';
import { IconQuestion } from 'app/icons';
import space from 'app/styles/space';
var AdminEnvironment = /** @class */ (function (_super) {
    __extends(AdminEnvironment, _super);
    function AdminEnvironment() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminEnvironment.prototype.getEndpoints = function () {
        return [['data', '/internal/environment/']];
    };
    AdminEnvironment.prototype.renderBody = function () {
        var data = this.state.data;
        var environment = data.environment, config = data.config, pythonVersion = data.pythonVersion;
        var version = ConfigStore.getConfig().version;
        return (<div>
        <h3>{t('Environment')}</h3>

        {environment ? (<dl className="vars">
            <VersionLabel>
              {t('Server Version')}
              {version.upgradeAvailable && (<Button title={t("You're running an old version of Sentry, did you know %s is available?", version.latest)} priority="link" href="https://github.com/getsentry/sentry/releases" icon={<IconQuestion size="sm"/>} size="small" external/>)}
            </VersionLabel>
            <dd>
              <pre className="val">{version.current}</pre>
            </dd>

            <dt>{t('Python Version')}</dt>
            <dd>
              <pre className="val">{pythonVersion}</pre>
            </dd>
            <dt>{t('Configuration File')}</dt>
            <dd>
              <pre className="val">{environment.config}</pre>
            </dd>
            <dt>{t('Uptime')}</dt>
            <dd>
              <pre className="val">
                {moment(environment.start_date).toNow(true)} (since{' '}
                {environment.start_date})
              </pre>
            </dd>
          </dl>) : (<p>
            {t('Environment not found (are you using the builtin Sentry webserver?).')}
          </p>)}

        <h3>
          {tct('Configuration [configPath]', {
            configPath: environment.config && <small>{environment.config}</small>,
        })}
        </h3>

        <dl className="vars">
          {config.map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return (<React.Fragment key={key}>
              <dt>{key}</dt>
              <dd>
                <pre className="val">{value}</pre>
              </dd>
            </React.Fragment>);
        })}
        </dl>
      </div>);
    };
    return AdminEnvironment;
}(AsyncView));
export default AdminEnvironment;
var VersionLabel = styled('dt')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=adminEnvironment.jsx.map