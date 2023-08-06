import { __extends, __makeTemplateObject, __rest } from "tslib";
import { components } from 'react-select';
import React from 'react';
import ReactDOM from 'react-dom';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import LoadingIndicator from 'app/components/loadingIndicator';
import OrganizationStore from 'app/stores/organizationStore';
import OrganizationsStore from 'app/stores/organizationsStore';
import Projects from 'app/utils/projects';
import SelectControl from 'app/components/forms/selectControl';
import replaceRouterParams from 'app/utils/replaceRouterParams';
import space from 'app/styles/space';
import Link from 'app/components/links/link';
import IdBadge from 'app/components/idBadge';
var ContextPickerModal = /** @class */ (function (_super) {
    __extends(ContextPickerModal, _super);
    function ContextPickerModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.orgSelect = null;
        _this.projectSelect = null;
        // Performs checks to see if we need to prompt user
        // i.e. When there is only 1 org and no project is needed or
        // there is only 1 org and only 1 project (which should be rare)
        _this.navigateIfFinish = function (organizations, projects, latestOrg) {
            var _a;
            if (latestOrg === void 0) { latestOrg = _this.props.organization; }
            var _b = _this.props, needProject = _b.needProject, onFinish = _b.onFinish, nextPath = _b.nextPath;
            // If no project is needed and theres only 1 org OR
            // if we need a project and there's only 1 project
            // then return because we can't navigate anywhere yet
            if ((!needProject && organizations.length !== 1) ||
                (needProject && projects.length !== 1)) {
                return;
            }
            // If there is only one org and we dont need a project slug, then call finish callback
            if (!needProject) {
                onFinish(replaceRouterParams(nextPath, {
                    orgId: organizations[0].slug,
                }));
                return;
            }
            // Use latest org or if only 1 org, use that
            var org = latestOrg;
            if (!org && organizations.length === 1) {
                org = organizations[0].slug;
            }
            onFinish(replaceRouterParams(nextPath, {
                orgId: org,
                projectId: projects[0].slug,
                project: (_a = _this.props.projects.find(function (p) { return p.slug === projects[0].slug; })) === null || _a === void 0 ? void 0 : _a.id,
            }));
        };
        _this.doFocus = function (ref) {
            if (!ref || _this.props.loading) {
                return;
            }
            // eslint-disable-next-line react/no-find-dom-node
            var el = ReactDOM.findDOMNode(ref);
            if (el !== null) {
                var input = el.querySelector('input');
                input && input.focus();
            }
        };
        _this.focusProjectSelector = function () {
            _this.doFocus(_this.projectSelect);
        };
        _this.focusOrganizationSelector = function () {
            _this.doFocus(_this.orgSelect);
        };
        _this.handleSelectOrganization = function (_a) {
            var value = _a.value;
            // If we do not need to select a project, we can early return after selecting an org
            // No need to fetch org details
            if (!_this.props.needProject) {
                _this.navigateIfFinish([{ slug: value }], []);
                return;
            }
            _this.props.onSelectOrganization(value);
        };
        _this.handleSelectProject = function (_a) {
            var value = _a.value;
            var organization = _this.props.organization;
            if (!value || !organization) {
                return;
            }
            _this.navigateIfFinish([{ slug: organization }], [{ slug: value }]);
        };
        _this.onProjectMenuOpen = function () {
            var _a = _this.props, projects = _a.projects, comingFromProjectId = _a.comingFromProjectId;
            // Hacky way to pre-focus to an item with newer versions of react select
            // See https://github.com/JedWatson/react-select/issues/3648
            setTimeout(function () {
                var ref = _this.projectSelect;
                if (ref) {
                    var projectChoices = ref.select.state.menuOptions.focusable;
                    var projectToBeFocused_1 = projects.find(function (_a) {
                        var id = _a.id;
                        return id === comingFromProjectId;
                    });
                    var selectedIndex = projectChoices.findIndex(function (option) { return option.value === (projectToBeFocused_1 === null || projectToBeFocused_1 === void 0 ? void 0 : projectToBeFocused_1.slug); });
                    if (selectedIndex >= 0 && projectToBeFocused_1) {
                        // Focusing selected option only if it exists
                        ref.select.scrollToFocusedOptionOnUpdate = true;
                        ref.select.inputIsHiddenAfterUpdate = false;
                        ref.select.setState({
                            focusedValue: null,
                            focusedOption: projectChoices[selectedIndex],
                        });
                    }
                }
            });
        };
        //TODO(TS): Fix typings
        _this.customOptionProject = function (_a) {
            var label = _a.label, props = __rest(_a, ["label"]);
            var project = _this.props.projects.find(function (_a) {
                var slug = _a.slug;
                return props.value === slug;
            });
            if (!project) {
                return null;
            }
            return (<components.Option label={label} {...props}>
        <IdBadge project={project} avatarSize={20} displayName={label} avatarProps={{ consistentWidth: true }}/>
      </components.Option>);
        };
        return _this;
    }
    ContextPickerModal.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, organizations = _a.organizations;
        // Don't make any assumptions if there are multiple organizations
        if (organizations.length !== 1) {
            return;
        }
        // If there is an org in context (and there's only 1 org available),
        // attempt to see if we need more info from user and redirect otherwise
        if (organization) {
            // This will handle if we can intelligently move the user forward
            this.navigateIfFinish([{ slug: organization }], projects);
            return;
        }
    };
    ContextPickerModal.prototype.componentDidUpdate = function (prevProps) {
        // Component may be mounted before projects is fetched, check if we can finish when
        // component is updated with projects
        if (JSON.stringify(prevProps.projects) !== JSON.stringify(this.props.projects)) {
            this.navigateIfFinish(this.props.organizations, this.props.projects);
        }
    };
    Object.defineProperty(ContextPickerModal.prototype, "headerText", {
        get: function () {
            var _a = this.props, needOrg = _a.needOrg, needProject = _a.needProject;
            if (needOrg && needProject) {
                return t('Select an organization and a project to continue');
            }
            if (needOrg) {
                return t('Select an organization to continue');
            }
            if (needProject) {
                return t('Select a project to continue');
            }
            //if neither project nor org needs to be selected, nothing will render anyways
            return '';
        },
        enumerable: false,
        configurable: true
    });
    ContextPickerModal.prototype.renderProjectSelectOrMessage = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects;
        if (!projects.length) {
            return (<div>
          {tct('You have no projects. Click [link] to make one.', {
                link: (<Link to={"/organizations/" + organization + "/projects/new/"}>{t('here')}</Link>),
            })}
        </div>);
        }
        return (<StyledSelectControl ref={function (ref) {
            _this.projectSelect = ref;
            _this.focusProjectSelector();
        }} placeholder={t('Select a Project')} name="project" options={projects.map(function (_a) {
            var slug = _a.slug;
            return ({ label: slug, value: slug });
        })} onChange={this.handleSelectProject} onMenuOpen={this.onProjectMenuOpen} components={{ Option: this.customOptionProject }}/>);
    };
    ContextPickerModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, needOrg = _a.needOrg, needProject = _a.needProject, organization = _a.organization, organizations = _a.organizations, loading = _a.loading, Header = _a.Header, Body = _a.Body;
        var shouldShowPicker = needOrg || needProject;
        if (!shouldShowPicker) {
            return null;
        }
        var shouldShowProjectSelector = organization && needProject && !loading;
        var orgChoices = organizations
            .filter(function (_a) {
            var status = _a.status;
            return status.id !== 'pending_deletion';
        })
            .map(function (_a) {
            var slug = _a.slug;
            return ({ label: slug, value: slug });
        });
        return (<React.Fragment>
        <Header closeButton>{this.headerText}</Header>
        <Body>
          {loading && <StyledLoadingIndicator overlay/>}
          {needOrg && (<StyledSelectControl ref={function (ref) {
            _this.orgSelect = ref;
            if (shouldShowProjectSelector) {
                return;
            }
            _this.focusOrganizationSelector();
        }} placeholder={t('Select an Organization')} name="organization" options={orgChoices} value={organization} onChange={this.handleSelectOrganization}/>)}

          {shouldShowProjectSelector && this.renderProjectSelectOrMessage()}
        </Body>
      </React.Fragment>);
    };
    return ContextPickerModal;
}(React.Component));
var ContextPickerModalContainer = createReactClass({
    displayName: 'ContextPickerModalContainer',
    mixins: [Reflux.connect(OrganizationsStore, 'organizations')],
    getInitialState: function () {
        var _a;
        var storeState = OrganizationStore.get();
        return {
            selectedOrganization: (_a = storeState.organization) === null || _a === void 0 ? void 0 : _a.slug,
        };
    },
    handleSelectOrganization: function (organizationSlug) {
        this.setState({ selectedOrganization: organizationSlug });
    },
    renderModal: function (_a) {
        var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded;
        return (<ContextPickerModal {...this.props} projects={projects || []} loading={!initiallyLoaded} organizations={this.state.organizations} organization={this.state.selectedOrganization} onSelectOrganization={this.handleSelectOrganization}/>);
    },
    render: function () {
        var _this = this;
        var projectSlugs = this.props.projectSlugs; // eslint-disable-line react/prop-types
        if (this.state.selectedOrganization) {
            return (<Projects orgId={this.state.selectedOrganization} allProjects={!(projectSlugs === null || projectSlugs === void 0 ? void 0 : projectSlugs.length)} slugs={projectSlugs}>
          {function (renderProps) { return _this.renderModal(renderProps); }}
        </Projects>);
        }
        return this.renderModal({});
    },
});
export default ContextPickerModalContainer;
var StyledSelectControl = styled(SelectControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(1));
var StyledLoadingIndicator = styled(LoadingIndicator)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  z-index: 1;\n"], ["\n  z-index: 1;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=contextPickerModal.jsx.map