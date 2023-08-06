import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { toggleKeyTransaction } from 'app/actionCreators/performance';
import { IconStar } from 'app/icons';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
var KeyTransactionField = /** @class */ (function (_super) {
    __extends(KeyTransactionField, _super);
    function KeyTransactionField(props) {
        var _this = _super.call(this, props) || this;
        _this.toggleKeyTransactionHandler = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, transactionName = _a.transactionName;
            var isKeyTransaction = _this.state.isKeyTransaction;
            var projectId = _this.getProjectId();
            // All the props are guaranteed to be not undefined at this point
            // as they have all been validated in the render method.
            toggleKeyTransaction(api, isKeyTransaction, organization.slug, [projectId], transactionName).then(function () {
                _this.setState({
                    isKeyTransaction: !isKeyTransaction,
                });
            });
        };
        _this.state = {
            isKeyTransaction: !!props.isKeyTransaction,
        };
        return _this;
    }
    KeyTransactionField.prototype.getProjectId = function () {
        var _a = this.props, projects = _a.projects, projectSlug = _a.projectSlug;
        var project = projects.find(function (proj) { return proj.slug === projectSlug; });
        if (!project) {
            return null;
        }
        return parseInt(project.id, 10);
    };
    KeyTransactionField.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug, transactionName = _a.transactionName;
        var isKeyTransaction = this.state.isKeyTransaction;
        var star = (<StyledKey color={isKeyTransaction ? 'yellow300' : 'gray200'} isSolid={isKeyTransaction} data-test-id="key-transaction-column"/>);
        // All these fields need to be defined in order to toggle a key transaction
        // Since they're not defined, we just render a plain star icon with no action
        // associated with it
        if (organization === undefined ||
            projectSlug === undefined ||
            transactionName === undefined ||
            this.getProjectId() === null) {
            return star;
        }
        return <KeyColumn onClick={this.toggleKeyTransactionHandler}>{star}</KeyColumn>;
    };
    return KeyTransactionField;
}(React.Component));
var KeyColumn = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var StyledKey = styled(IconStar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: pointer;\n  vertical-align: middle;\n"], ["\n  cursor: pointer;\n  vertical-align: middle;\n"])));
export default withApi(withProjects(KeyTransactionField));
var templateObject_1, templateObject_2;
//# sourceMappingURL=keyTransactionField.jsx.map