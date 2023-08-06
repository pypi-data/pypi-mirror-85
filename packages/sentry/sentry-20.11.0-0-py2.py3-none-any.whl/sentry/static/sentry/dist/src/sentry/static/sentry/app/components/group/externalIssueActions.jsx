import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import Modal from 'react-bootstrap/lib/Modal';
import styled from '@emotion/styled';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import IssueSyncListElement from 'app/components/issueSyncListElement';
import ExternalIssueForm from 'app/components/group/externalIssueForm';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';
import NavTabs from 'app/components/navTabs';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var ExternalIssueActions = /** @class */ (function (_super) {
    __extends(ExternalIssueActions, _super);
    function ExternalIssueActions(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.openModal = function (integration) {
            _this.setState({
                showModal: true,
                selectedIntegration: integration,
                action: 'create',
            });
        };
        _this.closeModal = function () {
            _this.setState({
                showModal: false,
                action: null,
                selectedIntegration: null,
            });
        };
        _this.handleClick = function (action) {
            _this.setState({ action: action });
        };
        _this.linkIssueSuccess = function (onSuccess) {
            _this.props.onChange(function () { return onSuccess(); });
            _this.closeModal();
        };
        _this.state = __assign({ showModal: false, action: 'create', selectedIntegration: null }, _this.getDefaultState());
        return _this;
    }
    ExternalIssueActions.prototype.getEndpoints = function () {
        return [];
    };
    ExternalIssueActions.prototype.linkedIssuesFilter = function () {
        return this.props.configurations
            .sort(function (a, b) { return a.name.toLowerCase().localeCompare(b.name.toLowerCase()); })
            .reduce(function (acc, curr) {
            if (curr.externalIssues.length) {
                acc.linked.push(curr);
            }
            else {
                acc.unlinked.push(curr);
            }
            return acc;
        }, { linked: [], unlinked: [] });
    };
    ExternalIssueActions.prototype.deleteIssue = function (integration) {
        var _this = this;
        var group = this.props.group;
        var externalIssues = integration.externalIssues;
        // Currently we do not support a case where there is multiple external issues.
        // For example, we shouldn't have more than 1 jira ticket created for an issue for each jira configuration.
        var issue = externalIssues[0];
        var id = issue.id;
        var endpoint = "/groups/" + group.id + "/integrations/" + integration.id + "/?externalIssue=" + id;
        this.api.request(endpoint, {
            method: 'DELETE',
            success: function () {
                _this.props.onChange(function () { return addSuccessMessage(t('Successfully unlinked issue.')); }, function () { return addErrorMessage(t('Unable to unlink issue.')); });
                _this.setState({
                    selectedIntegration: null,
                });
            },
            error: function () {
                addErrorMessage(t('Unable to unlink issue.'));
                _this.setState({
                    selectedIntegration: null,
                });
            },
        });
    };
    ExternalIssueActions.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, action = _a.action, selectedIntegration = _a.selectedIntegration;
        var _b = this.linkedIssuesFilter(), linked = _b.linked, unlinked = _b.unlinked;
        return (<React.Fragment>
        {linked.length > 0 &&
            linked.map(function (config) {
                var provider = config.provider, externalIssues = config.externalIssues;
                var issue = externalIssues[0];
                return (<IssueSyncListElement key={issue.id} externalIssueLink={issue.url} externalIssueId={issue.id} externalIssueKey={issue.key} externalIssueDisplayName={issue.displayName} onClose={function () { return _this.deleteIssue(config); }} integrationType={provider.key} hoverCardHeader={t('Linked %s Integration', provider.name)} hoverCardBody={<div>
                    <IssueTitle>{issue.title}</IssueTitle>
                    {issue.description && (<IssueDescription>{issue.description}</IssueDescription>)}
                  </div>}/>);
            })}

        {unlinked.length > 0 && (<IssueSyncListElement integrationType={unlinked[0].provider.key} hoverCardHeader={t('Linked %s Integration', unlinked[0].provider.name)} hoverCardBody={<Container>
                {unlinked.map(function (config) { return (<Wrapper onClick={function () { return _this.openModal(config); }} key={config.id}>
                    <IntegrationItem integration={config}/>
                  </Wrapper>); })}
              </Container>} onOpen={unlinked.length === 1 ? function () { return _this.openModal(unlinked[0]); } : undefined} showHoverCard={this.state.showModal ? false : undefined}/>)}
        {selectedIntegration && (<Modal show={this.state.showModal} onHide={this.closeModal} animation={false} enforceFocus={false} backdrop="static">
            <Modal.Header closeButton>
              <Modal.Title>{selectedIntegration.provider.name + " Issue"}</Modal.Title>
            </Modal.Header>
            <NavTabs underlined>
              <li className={action === 'create' ? 'active' : ''}>
                <a onClick={function () { return _this.handleClick('create'); }}>{t('Create')}</a>
              </li>
              <li className={action === 'link' ? 'active' : ''}>
                <a onClick={function () { return _this.handleClick('link'); }}>{t('Link')}</a>
              </li>
            </NavTabs>
            <Modal.Body>
              {action && (<ExternalIssueForm 
        // need the key here so React will re-render
        // with a new action prop
        key={action} group={this.props.group} integration={selectedIntegration} action={action} onSubmitSuccess={function (_, onSuccess) { return _this.linkIssueSuccess(onSuccess); }}/>)}
            </Modal.Body>
          </Modal>)}
      </React.Fragment>);
    };
    return ExternalIssueActions;
}(AsyncComponent));
var IssueTitle = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"], ["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"])), overflowEllipsis);
var IssueDescription = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  ", ";\n"], ["\n  margin-top: ", ";\n  ", ";\n"])), space(1), overflowEllipsis);
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  cursor: pointer;\n"], ["\n  margin-bottom: ", ";\n  cursor: pointer;\n"])), space(2));
var Container = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  & > div:last-child {\n    margin-bottom: ", ";\n  }\n"], ["\n  & > div:last-child {\n    margin-bottom: ", ";\n  }\n"])), space(1));
export default ExternalIssueActions;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=externalIssueActions.jsx.map