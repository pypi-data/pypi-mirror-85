import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import recreateRoute from 'app/utils/recreateRoute';
import SessionRow from './sessionRow';
import { tableLayout } from './utils';
var SessionHistory = /** @class */ (function (_super) {
    __extends(SessionHistory, _super);
    function SessionHistory() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SessionHistory.prototype.getTitle = function () {
        return t('Session History');
    };
    SessionHistory.prototype.getEndpoints = function () {
        return [['ipList', '/users/me/ips/']];
    };
    SessionHistory.prototype.renderBody = function () {
        var ipList = this.state.ipList;
        if (!ipList) {
            return null;
        }
        var _a = this.props, routes = _a.routes, params = _a.params, location = _a.location;
        var recreateRouteProps = { routes: routes, params: params, location: location };
        return (<React.Fragment>
        <SettingsPageHeader title={t('Security')} tabs={<NavTabs underlined>
              <ListLink to={recreateRoute('', __assign(__assign({}, recreateRouteProps), { stepBack: -1 }))} index>
                {t('Settings')}
              </ListLink>
              <ListLink to={recreateRoute('', recreateRouteProps)}>
                {t('Session History')}
              </ListLink>
            </NavTabs>}/>

        <Panel>
          <SessionPanelHeader>
            <div>{t('Sessions')}</div>
            <div>{t('First Seen')}</div>
            <div>{t('Last Seen')}</div>
          </SessionPanelHeader>

          <PanelBody>
            {ipList.map(function (_a) {
            var id = _a.id, ipObj = __rest(_a, ["id"]);
            return (<SessionRow key={id} {...ipObj}/>);
        })}
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    return SessionHistory;
}(AsyncView));
export default SessionHistory;
var SessionPanelHeader = styled(PanelHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n  justify-content: initial;\n"], ["\n  ", "\n  justify-content: initial;\n"])), tableLayout);
var templateObject_1;
//# sourceMappingURL=index.jsx.map