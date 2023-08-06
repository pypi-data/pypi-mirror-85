import { __assign, __extends } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import PropTypes from 'prop-types';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Field from 'app/views/settings/components/forms/field';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import Switch from 'app/components/switch';
import Truncate from 'app/components/truncate';
import { IconAdd, IconFlag } from 'app/icons';
function ServiceHookRow(_a) {
    var orgId = _a.orgId, projectId = _a.projectId, hook = _a.hook, onToggleActive = _a.onToggleActive;
    return (<Field label={<Link data-test-id="project-service-hook" to={"/settings/" + orgId + "/projects/" + projectId + "/hooks/" + hook.id + "/"}>
          <Truncate value={hook.url}/>
        </Link>} help={<small>
          {hook.events && hook.events.length !== 0 ? (hook.events.join(', ')) : (<em>{t('no events configured')}</em>)}
        </small>}>
      <Switch isActive={hook.status === 'active'} size="lg" toggle={onToggleActive}/>
    </Field>);
}
var ProjectServiceHooks = /** @class */ (function (_super) {
    __extends(ProjectServiceHooks, _super);
    function ProjectServiceHooks() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onToggleActive = function (hook) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            var hookList = _this.state.hookList;
            if (!hookList) {
                return;
            }
            addLoadingMessage(t('Saving changes\u2026'));
            _this.api.request("/projects/" + orgId + "/" + projectId + "/hooks/" + hook.id + "/", {
                method: 'PUT',
                data: {
                    isActive: hook.status !== 'active',
                },
                success: function (data) {
                    clearIndicators();
                    _this.setState({
                        hookList: hookList.map(function (h) {
                            if (h.id === data.id) {
                                return __assign(__assign({}, h), data);
                            }
                            return h;
                        }),
                    });
                },
                error: function () {
                    addErrorMessage(t('Unable to remove application. Please try again.'));
                },
            });
        };
        return _this;
    }
    ProjectServiceHooks.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['hookList', "/projects/" + orgId + "/" + projectId + "/hooks/"]];
    };
    ProjectServiceHooks.prototype.renderEmpty = function () {
        return (<EmptyMessage>
        {t('There are no service hooks associated with this project.')}
      </EmptyMessage>);
    };
    ProjectServiceHooks.prototype.renderResults = function () {
        var _this = this;
        var _a;
        var _b = this.props.params, orgId = _b.orgId, projectId = _b.projectId;
        return (<React.Fragment>
        <PanelHeader key="header">{t('Service Hook')}</PanelHeader>
        <PanelBody key="body">
          <PanelAlert type="info" icon={<IconFlag size="md"/>}>
            {t('Service Hooks are an early adopter preview feature and will change in the future.')}
          </PanelAlert>
          {(_a = this.state.hookList) === null || _a === void 0 ? void 0 : _a.map(function (hook) { return (<ServiceHookRow key={hook.id} orgId={orgId} projectId={projectId} hook={hook} onToggleActive={_this.onToggleActive.bind(_this, hook)}/>); })}
        </PanelBody>
      </React.Fragment>);
    };
    ProjectServiceHooks.prototype.renderBody = function () {
        var hookList = this.state.hookList;
        var body = hookList && hookList.length > 0 ? this.renderResults() : this.renderEmpty();
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var access = new Set(this.context.organization.access);
        return (<React.Fragment>
        <SettingsPageHeader title={t('Service Hooks')} action={access.has('project:write') ? (<Button data-test-id="new-service-hook" to={"/settings/" + orgId + "/projects/" + projectId + "/hooks/new/"} size="small" priority="primary" icon={<IconAdd size="xs" isCircled/>}>
                {t('Create New Hook')}
              </Button>) : null}/>
        <Panel>{body}</Panel>
      </React.Fragment>);
    };
    ProjectServiceHooks.contextTypes = {
        router: PropTypes.object,
        organization: PropTypes.object.isRequired,
    };
    return ProjectServiceHooks;
}(AsyncView));
export default ProjectServiceHooks;
//# sourceMappingURL=projectServiceHooks.jsx.map