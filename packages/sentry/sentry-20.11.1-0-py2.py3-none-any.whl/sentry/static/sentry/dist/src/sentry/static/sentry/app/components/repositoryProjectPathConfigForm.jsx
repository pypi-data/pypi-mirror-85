import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
var RepositoryProjectPathConfigForm = /** @class */ (function (_super) {
    __extends(RepositoryProjectPathConfigForm, _super);
    function RepositoryProjectPathConfigForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(RepositoryProjectPathConfigForm.prototype, "initialData", {
        get: function () {
            var existingConfig = this.props.existingConfig;
            return __assign({ defaultBranch: 'master', stackRoot: '', sourceRoot: '', repositoryId: existingConfig === null || existingConfig === void 0 ? void 0 : existingConfig.repoId }, pick(existingConfig, ['projectId', 'defaultBranch', 'stackRoot', 'sourceRoot']));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RepositoryProjectPathConfigForm.prototype, "formFields", {
        get: function () {
            var _a = this.props, projects = _a.projects, repos = _a.repos;
            var repoChoices = repos.map(function (_a) {
                var name = _a.name, id = _a.id;
                return ({ value: id, label: name });
            });
            return {
                title: t('Create Code Path'),
                fields: [
                    {
                        name: 'projectId',
                        type: 'sentry_project_selector',
                        required: true,
                        label: t('Project'),
                        inline: false,
                        projects: projects,
                    },
                    {
                        name: 'repositoryId',
                        type: 'select',
                        required: true,
                        label: t('Repo'),
                        inline: false,
                        placeholder: t('Choose repo'),
                        options: repoChoices,
                        deprecatedSelectControl: false,
                    },
                    {
                        name: 'defaultBranch',
                        type: 'string',
                        required: true,
                        label: t('Branch'),
                        placeholder: t('Type your branch'),
                        inline: false,
                        showHelpInTooltip: true,
                        help: t('If an event does not have a release tied to a commit, we will use this branch when linking to your source code.'),
                    },
                    {
                        name: 'stackRoot',
                        type: 'string',
                        required: false,
                        label: t('Stack Trace Root'),
                        placeholder: t('Type root path of your stack traces'),
                        inline: false,
                        showHelpInTooltip: true,
                        help: t('Any stack trace starting with this path will be mapped with this rule. An empty string will match all paths.'),
                    },
                    {
                        name: 'sourceRoot',
                        type: 'string',
                        required: false,
                        label: t('Source Code Root'),
                        placeholder: t('Type root path of your source code'),
                        inline: false,
                        showHelpInTooltip: true,
                        help: t('When a rule matches, the stack trace root is replaced with this path to get the path in your repository. Leaving this empty means replacing the stack trace root with an empty string.'),
                    },
                ],
            };
        },
        enumerable: false,
        configurable: true
    });
    RepositoryProjectPathConfigForm.prototype.render = function () {
        var _a = this.props, organization = _a.organization, integration = _a.integration, onSubmitSuccess = _a.onSubmitSuccess, existingConfig = _a.existingConfig;
        // endpoint changes if we are making a new row or updating an existing one
        var baseEndpoint = "/organizations/" + organization.slug + "/integrations/" + integration.id + "/repo-project-path-configs/";
        var endpoint = existingConfig
            ? "" + baseEndpoint + existingConfig.id + "/"
            : baseEndpoint;
        var apiMethod = existingConfig ? 'PUT' : 'POST';
        return (<StyledForm onSubmitSuccess={onSubmitSuccess} initialData={this.initialData} apiEndpoint={endpoint} apiMethod={apiMethod}>
        <JsonForm forms={[this.formFields]}/>
      </StyledForm>);
    };
    return RepositoryProjectPathConfigForm;
}(React.Component));
export default RepositoryProjectPathConfigForm;
var StyledForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  label {\n    color: ", ";\n    font-family: Rubik;\n    font-size: 12px;\n    font-weight: 500;\n    text-transform: uppercase;\n  }\n"], ["\n  label {\n    color: ", ";\n    font-family: Rubik;\n    font-size: 12px;\n    font-weight: 500;\n    text-transform: uppercase;\n  }\n"])), function (p) { return p.theme.subText; });
var templateObject_1;
//# sourceMappingURL=repositoryProjectPathConfigForm.jsx.map