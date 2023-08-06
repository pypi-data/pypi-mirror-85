import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { ALL_ENVIRONMENTS_KEY } from 'app/constants';
import { Panel, PanelHeader, PanelBody, PanelItem } from 'app/components/panels';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import Access from 'app/components/acl/access';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import withApi from 'app/utils/withApi';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ListLink from 'app/components/links/listLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import NavTabs from 'app/components/navTabs';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
import { getUrlRoutingName, getDisplayName } from 'app/utils/environment';
var ProjectEnvironments = /** @class */ (function (_super) {
    __extends(ProjectEnvironments, _super);
    function ProjectEnvironments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            project: null,
            environments: null,
            isLoading: true,
        };
        // Toggle visibility of environment
        _this.toggleEnv = function (env, shouldHide) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/environments/" + getUrlRoutingName(env) + "/", {
                method: 'PUT',
                data: {
                    name: env.name,
                    isHidden: shouldHide,
                },
                success: function () {
                    addSuccessMessage(tct('Updated [environment]', {
                        environment: getDisplayName(env),
                    }));
                },
                error: function () {
                    addErrorMessage(tct('Unable to update [environment]', {
                        environment: getDisplayName(env),
                    }));
                },
                complete: _this.fetchData.bind(_this),
            });
        };
        return _this;
    }
    ProjectEnvironments.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectEnvironments.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.location.pathname.endsWith('hidden/') !==
            prevProps.location.pathname.endsWith('hidden/')) {
            this.fetchData();
        }
    };
    ProjectEnvironments.prototype.fetchData = function () {
        var _this = this;
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        if (!this.state.isLoading) {
            this.setState({ isLoading: true });
        }
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        this.props.api.request("/projects/" + orgId + "/" + projectId + "/environments/", {
            query: {
                visibility: isHidden ? 'hidden' : 'visible',
            },
            success: function (environments) {
                _this.setState({ environments: environments, isLoading: false });
            },
        });
    };
    ProjectEnvironments.prototype.fetchProjectDetails = function () {
        var _this = this;
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        this.props.api.request("/projects/" + orgId + "/" + projectId + "/", {
            success: function (project) {
                _this.setState({ project: project });
            },
        });
    };
    ProjectEnvironments.prototype.renderEmpty = function () {
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        var message = isHidden
            ? t("You don't have any hidden environments.")
            : t("You don't have any environments yet.");
        return <EmptyMessage>{message}</EmptyMessage>;
    };
    /**
     * Renders rows for "system" environments:
     * - "All Environments"
     * - "No Environment"
     *
     */
    ProjectEnvironments.prototype.renderAllEnvironmentsSystemRow = function () {
        // Not available in "Hidden" tab
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        if (isHidden) {
            return null;
        }
        return (<EnvironmentRow name={ALL_ENVIRONMENTS_KEY} environment={{
            id: ALL_ENVIRONMENTS_KEY,
            name: ALL_ENVIRONMENTS_KEY,
            displayName: ALL_ENVIRONMENTS_KEY,
        }} isSystemRow/>);
    };
    ProjectEnvironments.prototype.renderEnvironmentList = function (envs) {
        var _this = this;
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        var buttonText = isHidden ? t('Show') : t('Hide');
        return (<React.Fragment>
        {this.renderAllEnvironmentsSystemRow()}
        {envs.map(function (env) { return (<EnvironmentRow key={env.id} name={env.name} environment={env} isHidden={isHidden} onHide={_this.toggleEnv} actionText={buttonText} shouldShowAction/>); })}
      </React.Fragment>);
    };
    ProjectEnvironments.prototype.renderBody = function () {
        var _a = this.state, environments = _a.environments, isLoading = _a.isLoading;
        if (isLoading) {
            return <LoadingIndicator />;
        }
        return (<PanelBody>
        {(environments === null || environments === void 0 ? void 0 : environments.length) ? this.renderEnvironmentList(environments)
            : this.renderEmpty()}
      </PanelBody>);
    };
    ProjectEnvironments.prototype.render = function () {
        var _a = this.props, routes = _a.routes, params = _a.params, location = _a.location;
        var isHidden = location.pathname.endsWith('hidden/');
        var baseUrl = recreateRoute('', { routes: routes, params: params, stepBack: -1 });
        return (<div>
        <SentryDocumentTitle title={t('Environments')} objSlug={params.projectId}/>
        <SettingsPageHeader title={t('Manage Environments')} tabs={<NavTabs underlined>
              <ListLink to={baseUrl} index isActive={function () { return !isHidden; }}>
                {t('Environments')}
              </ListLink>
              <ListLink to={baseUrl + "hidden/"} index isActive={function () { return isHidden; }}>
                {t('Hidden')}
              </ListLink>
            </NavTabs>}/>
        <PermissionAlert />

        <Panel>
          <PanelHeader>{isHidden ? t('Hidden') : t('Active Environments')}</PanelHeader>
          {this.renderBody()}
        </Panel>
      </div>);
    };
    return ProjectEnvironments;
}(React.Component));
function EnvironmentRow(_a) {
    var environment = _a.environment, name = _a.name, onHide = _a.onHide, _b = _a.shouldShowAction, shouldShowAction = _b === void 0 ? false : _b, _c = _a.isSystemRow, isSystemRow = _c === void 0 ? false : _c, _d = _a.isHidden, isHidden = _d === void 0 ? false : _d, _e = _a.actionText, actionText = _e === void 0 ? '' : _e;
    return (<EnvironmentItem>
      <Name>{isSystemRow ? t('All Environments') : name}</Name>
      <Access access={['project:write']}>
        {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<React.Fragment>
            {shouldShowAction && onHide && (<EnvironmentButton size="xsmall" disabled={!hasAccess} onClick={function () { return onHide(environment, !isHidden); }}>
                {actionText}
              </EnvironmentButton>)}
          </React.Fragment>);
    }}
      </Access>
    </EnvironmentItem>);
}
var EnvironmentItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
var Name = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var EnvironmentButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.5));
export { ProjectEnvironments };
export default withApi(ProjectEnvironments);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectEnvironments.jsx.map