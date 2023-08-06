import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Modal from 'react-bootstrap/lib/Modal';
import sortBy from 'lodash/sortBy';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import { IconAdd } from 'app/icons';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import RepositoryProjectPathConfigRow, { NameRepoColumn, OutputPathColumn, InputPathColumn, ButtonColumn, } from 'app/components/repositoryProjectPathConfigRow';
import RepositoryProjectPathConfigForm from 'app/components/repositoryProjectPathConfigForm';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import space from 'app/styles/space';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
var IntegrationCodeMappings = /** @class */ (function (_super) {
    __extends(IntegrationCodeMappings, _super);
    function IntegrationCodeMappings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.openModal = function (pathConfig) {
            _this.setState({
                showModal: true,
                configInEdit: pathConfig,
            });
        };
        _this.closeModal = function () {
            _this.setState({
                showModal: false,
                pathConfig: undefined,
            });
        };
        _this.handleEdit = function (pathConfig) {
            _this.openModal(pathConfig);
        };
        _this.handleDelete = function (pathConfig) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, integration, endpoint, pathConfigs, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, integration = _a.integration;
                        endpoint = "/organizations/" + organization.slug + "/integrations/" + integration.id + "/repo-project-path-configs/" + pathConfig.id + "/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _c.sent();
                        pathConfigs = this.state.pathConfigs;
                        pathConfigs = pathConfigs.filter(function (config) { return config.id !== pathConfig.id; });
                        this.setState({ pathConfigs: pathConfigs });
                        addSuccessMessage(t('Deletion successful'));
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        //no 4xx errors should happen on delete
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmitSuccess = function (pathConfig) {
            var pathConfigs = _this.state.pathConfigs;
            pathConfigs = pathConfigs.filter(function (config) { return config.id !== pathConfig.id; });
            // our getter handles the order of the configs
            pathConfigs = pathConfigs.concat([pathConfig]);
            _this.setState({ pathConfigs: pathConfigs });
            _this.closeModal();
        };
        return _this;
    }
    IntegrationCodeMappings.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { pathConfigs: [], repos: [], showModal: false });
    };
    Object.defineProperty(IntegrationCodeMappings.prototype, "integrationId", {
        get: function () {
            return this.props.integration.id;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "projects", {
        get: function () {
            return this.props.organization.projects;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "pathConfigs", {
        get: function () {
            // we want to sort by the project slug and the
            // id of the config
            return sortBy(this.state.pathConfigs, [
                function (_a) {
                    var projectSlug = _a.projectSlug;
                    return projectSlug;
                },
                function (_a) {
                    var id = _a.id;
                    return parseInt(id, 10);
                },
            ]);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "repos", {
        get: function () {
            var _this = this;
            //endpoint doesn't support loading only the repos for this integration
            //but most people only have one source code repo so this should be fine
            return this.state.repos.filter(function (repo) { return repo.integrationId === _this.integrationId; });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationCodeMappings.prototype.getEndpoints = function () {
        var orgSlug = this.props.organization.slug;
        return [
            [
                'pathConfigs',
                "/organizations/" + orgSlug + "/integrations/" + this.integrationId + "/repo-project-path-configs/",
            ],
            ['repos', "/organizations/" + orgSlug + "/repos/", { query: { status: 'active' } }],
        ];
    };
    IntegrationCodeMappings.prototype.getMatchingProject = function (pathConfig) {
        return this.projects.find(function (project) { return project.id === pathConfig.projectId; });
    };
    IntegrationCodeMappings.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, integration = _a.integration;
        var _b = this.state, showModal = _b.showModal, configInEdit = _b.configInEdit;
        var pathConfigs = this.pathConfigs;
        return (<React.Fragment>
        <Panel>
          <PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <NameRepoColumn>{t('Code Path Mappings')}</NameRepoColumn>
              <InputPathColumn>{t('Stack Trace Root')}</InputPathColumn>
              <OutputPathColumn>{t('Source Code Root')}</OutputPathColumn>
              <ButtonColumn>
                <AddButton onClick={function () { return _this.openModal(); }} size="xsmall" icon={<IconAdd size="xs" isCircled/>}>
                  {t('Add Mapping')}
                </AddButton>
              </ButtonColumn>
            </HeaderLayout>
          </PanelHeader>
          <PanelBody>
            {pathConfigs.length === 0 && (<EmptyMessage description={t('No code path mappings')}/>)}
            {pathConfigs
            .map(function (pathConfig) {
            var project = _this.getMatchingProject(pathConfig);
            // this should never happen since our pathConfig would be deleted
            // if project was deleted
            if (!project) {
                return null;
            }
            return (<ConfigPanelItem key={pathConfig.id}>
                    <Layout>
                      <RepositoryProjectPathConfigRow pathConfig={pathConfig} project={project} onEdit={_this.handleEdit} onDelete={_this.handleDelete}/>
                    </Layout>
                  </ConfigPanelItem>);
        })
            .filter(function (item) { return !!item; })}
          </PanelBody>
        </Panel>

        <Modal show={showModal} onHide={this.closeModal} enforceFocus={false} backdrop="static" animation={false}>
          <Modal.Header closeButton/>
          <Modal.Body>
            <RepositoryProjectPathConfigForm organization={organization} integration={integration} projects={this.projects} repos={this.repos} onSubmitSuccess={this.handleSubmitSuccess} existingConfig={configInEdit}/>
          </Modal.Body>
        </Modal>
      </React.Fragment>);
    };
    return IntegrationCodeMappings;
}(AsyncComponent));
export default withOrganization(IntegrationCodeMappings);
var AddButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var Layout = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;\n  grid-template-areas: 'name-repo input-path output-path button';\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;\n  grid-template-areas: 'name-repo input-path output-path button';\n"])), space(1));
var HeaderLayout = styled(Layout)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: flex-end;\n  margin: ", ";\n"], ["\n  align-items: flex-end;\n  margin: ", ";\n"])), space(1));
var ConfigPanelItem = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=integrationCodeMappings.jsx.map