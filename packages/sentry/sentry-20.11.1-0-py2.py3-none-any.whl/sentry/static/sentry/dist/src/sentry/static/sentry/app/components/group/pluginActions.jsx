import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import Modal from 'react-bootstrap/lib/Modal';
import withApi from 'app/utils/withApi';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import NavTabs from 'app/components/navTabs';
import plugins from 'app/plugins';
import { t, tct } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import IssueSyncListElement from 'app/components/issueSyncListElement';
import withOrganization from 'app/utils/withOrganization';
var PluginActions = /** @class */ (function (_super) {
    __extends(PluginActions, _super);
    function PluginActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showModal: false,
            actionType: null,
            issue: null,
            pluginLoading: false,
        };
        _this.deleteIssue = function () {
            var plugin = __assign(__assign({}, _this.props.plugin), { issue: null });
            // override plugin.issue so that 'create/link' Modal
            // doesn't think the plugin still has an issue linked
            var endpoint = "/issues/" + _this.props.group.id + "/plugins/" + plugin.slug + "/unlink/";
            _this.props.api.request(endpoint, {
                success: function () {
                    _this.loadPlugin(plugin);
                    addSuccessMessage(t('Successfully unlinked issue.'));
                },
                error: function () {
                    addErrorMessage(t('Unable to unlink issue'));
                },
            });
        };
        _this.loadPlugin = function (data) {
            _this.setState({
                pluginLoading: true,
            }, function () {
                plugins.load(data, function () {
                    var issue = data.issue || null;
                    _this.setState({ pluginLoading: false, issue: issue });
                });
            });
        };
        _this.openModal = function () {
            _this.setState({
                showModal: true,
                actionType: 'create',
            });
        };
        _this.closeModal = function (data) {
            _this.setState({
                issue: data && data.id && data.link
                    ? { issue_id: data.id, url: data.link, label: data.label }
                    : null,
                showModal: false,
            });
        };
        _this.handleClick = function (actionType) {
            _this.setState({ actionType: actionType });
        };
        return _this;
    }
    PluginActions.prototype.componentDidMount = function () {
        this.loadPlugin(this.props.plugin);
    };
    PluginActions.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.plugin.id !== nextProps.plugin.id) {
            this.loadPlugin(nextProps.plugin);
        }
    };
    PluginActions.prototype.render = function () {
        var _this = this;
        var _a = this.state, actionType = _a.actionType, issue = _a.issue;
        var plugin = __assign(__assign({}, this.props.plugin), { issue: issue });
        return (<React.Fragment>
        <IssueSyncListElement onOpen={this.openModal} externalIssueDisplayName={issue ? issue.label : null} externalIssueId={issue ? issue.issue_id : null} externalIssueLink={issue ? issue.url : null} onClose={this.deleteIssue} integrationType={plugin.id}/>
        <Modal show={this.state.showModal} onHide={this.closeModal} animation={false} enforceFocus={false}>
          <Modal.Header closeButton>
            <Modal.Title>
              {tct('[name] Issue', { name: plugin.name || plugin.title })}
            </Modal.Title>
          </Modal.Header>
          <NavTabs underlined>
            <li className={actionType === 'create' ? 'active' : ''}>
              <a onClick={function () { return _this.handleClick('create'); }}>{t('Create')}</a>
            </li>
            <li className={actionType === 'link' ? 'active' : ''}>
              <a onClick={function () { return _this.handleClick('link'); }}>{t('Link')}</a>
            </li>
          </NavTabs>
          {this.state.showModal && actionType && !this.state.pluginLoading && (
        // need the key here so React will re-render
        // with new action prop
        <Modal.Body key={actionType}>
              {plugins.get(plugin).renderGroupActions({
            plugin: plugin,
            group: this.props.group,
            project: this.props.project,
            organization: this.props.organization,
            actionType: actionType,
            onSuccess: this.closeModal,
        })}
            </Modal.Body>)}
        </Modal>
      </React.Fragment>);
    };
    PluginActions.propTypes = {
        api: PropTypes.object,
        group: SentryTypes.Group.isRequired,
        organization: SentryTypes.Organization.isRequired,
        project: SentryTypes.Project.isRequired,
        plugin: PropTypes.object.isRequired,
    };
    return PluginActions;
}(React.Component));
export { PluginActions };
export default withApi(withOrganization(PluginActions));
//# sourceMappingURL=pluginActions.jsx.map