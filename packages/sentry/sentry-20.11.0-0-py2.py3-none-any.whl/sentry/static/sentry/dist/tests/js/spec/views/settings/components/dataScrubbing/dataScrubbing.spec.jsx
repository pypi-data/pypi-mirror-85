import { __assign, __awaiter, __generator, __rest } from "tslib";
import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import DataScrubbing from 'app/views/settings/components/dataScrubbing';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
jest.mock('app/actionCreators/modal');
// @ts-expect-error
var relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
var stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
var organizationSlug = 'sentry';
var handleUpdateOrganization = jest.fn();
var additionalContext = 'These rules can be configured for each project.';
jest.mock('app/actionCreators/indicator');
function getOrganization(piiConfig) {
    // @ts-expect-error
    return TestStubs.Organization(piiConfig ? { id: '123', relayPiiConfig: piiConfig } : { id: '123' });
}
function renderComponent(_a) {
    var _b;
    var disabled = _a.disabled, projectId = _a.projectId, endpoint = _a.endpoint, props = __rest(_a, ["disabled", "projectId", "endpoint"]);
    var organization = (_b = props.organization) !== null && _b !== void 0 ? _b : getOrganization();
    if (projectId) {
        return mountWithTheme(<DataScrubbing additionalContext={additionalContext} endpoint={endpoint} projectId={projectId} relayPiiConfig={stringRelayPiiConfig} disabled={disabled} organization={organization} onSubmitSuccess={handleUpdateOrganization}/>);
    }
    return mountWithTheme(<DataScrubbing additionalContext={additionalContext} endpoint={endpoint} relayPiiConfig={stringRelayPiiConfig} disabled={disabled} organization={organization} onSubmitSuccess={handleUpdateOrganization}/>);
}
describe('Data Scrubbing', function () {
    describe('Organization level', function () {
        var endpoint = "organization/" + organizationSlug + "/";
        it('default render', function () {
            var wrapper = renderComponent({ disabled: false, endpoint: endpoint });
            // PanelHeader
            expect(wrapper.find('PanelHeader').text()).toEqual('Advanced Data Scrubbing');
            //PanelAlert
            var panelAlert = wrapper.find('PanelAlert');
            expect(panelAlert.text()).toEqual(additionalContext + " The new rules will only apply to upcoming events.  For more details, see full documentation on data scrubbing.");
            var readDocsLink = panelAlert.find('a');
            expect(readDocsLink.text()).toEqual('full documentation on data scrubbing');
            expect(readDocsLink.prop('href')).toEqual('https://docs.sentry.io/data-management/advanced-datascrubbing/');
            //PanelBody
            var panelBody = wrapper.find('PanelBody');
            expect(panelBody).toHaveLength(1);
            expect(panelBody.find('ListItem')).toHaveLength(3);
            // OrganizationRules
            var organizationRules = panelBody.find('OrganizationRules');
            expect(organizationRules).toHaveLength(0);
            // PanelAction
            var actionButtons = wrapper.find('PanelAction').find('Button');
            expect(actionButtons).toHaveLength(2);
            expect(actionButtons.at(0).text()).toEqual('Read the docs');
            expect(actionButtons.at(1).text()).toEqual('Add Rule');
            expect(actionButtons.at(1).prop('disabled')).toEqual(false);
        });
        it('render disabled', function () {
            var wrapper = renderComponent({ disabled: true, endpoint: endpoint });
            //PanelBody
            var panelBody = wrapper.find('PanelBody');
            expect(panelBody).toHaveLength(1);
            expect(panelBody.find('List').prop('isDisabled')).toEqual(true);
            // PanelAction
            var actionButtons = wrapper.find('PanelAction').find('Button');
            expect(actionButtons).toHaveLength(2);
            expect(actionButtons.at(0).prop('disabled')).toEqual(false);
            expect(actionButtons.at(1).prop('disabled')).toEqual(true);
        });
    });
    describe('Project level', function () {
        var projectId = 'foo';
        var endpoint = "/projects/" + organizationSlug + "/" + projectId + "/";
        it('default render', function () {
            var wrapper = renderComponent({
                disabled: false,
                projectId: projectId,
                endpoint: endpoint,
            });
            // PanelHeader
            expect(wrapper.find('PanelHeader').text()).toEqual('Advanced Data Scrubbing');
            //PanelAlert
            var panelAlert = wrapper.find('PanelAlert');
            expect(panelAlert.text()).toEqual(additionalContext + " The new rules will only apply to upcoming events.  For more details, see full documentation on data scrubbing.");
            var readDocsLink = panelAlert.find('a');
            expect(readDocsLink.text()).toEqual('full documentation on data scrubbing');
            expect(readDocsLink.prop('href')).toEqual('https://docs.sentry.io/data-management/advanced-datascrubbing/');
            //PanelBody
            var panelBody = wrapper.find('PanelBody');
            expect(panelBody).toHaveLength(1);
            expect(panelBody.find('ListItem')).toHaveLength(3);
            // OrganizationRules
            var organizationRules = panelBody.find('OrganizationRules');
            expect(organizationRules).toHaveLength(1);
            expect(organizationRules.text()).toEqual('There are no data scrubbing rules at the organization level');
            // PanelAction
            var actionButtons = wrapper.find('PanelAction').find('Button');
            expect(actionButtons).toHaveLength(2);
            expect(actionButtons.at(0).text()).toEqual('Read the docs');
            expect(actionButtons.at(1).text()).toEqual('Add Rule');
            expect(actionButtons.at(1).prop('disabled')).toEqual(false);
        });
        it('render disabled', function () {
            var wrapper = renderComponent({ disabled: true, endpoint: endpoint });
            //PanelBody
            var panelBody = wrapper.find('PanelBody');
            expect(panelBody).toHaveLength(1);
            expect(panelBody.find('List').prop('isDisabled')).toEqual(true);
            // PanelAction
            var actionButtons = wrapper.find('PanelAction').find('Button');
            expect(actionButtons).toHaveLength(2);
            expect(actionButtons.at(0).prop('disabled')).toEqual(false);
            expect(actionButtons.at(1).prop('disabled')).toEqual(true);
        });
        it('OrganizationRules has content', function () {
            var wrapper = renderComponent({
                disabled: false,
                organization: getOrganization(stringRelayPiiConfig),
                projectId: projectId,
                endpoint: endpoint,
            });
            // OrganizationRules
            var organizationRules = wrapper.find('OrganizationRules');
            expect(organizationRules).toHaveLength(1);
            expect(organizationRules.find('Header').text()).toEqual('Organization Rules');
            var listItems = organizationRules.find('ListItem');
            expect(listItems).toHaveLength(3);
            expect(listItems.at(0).find('[role="button"]')).toHaveLength(0);
        });
        it('Delete rule successfully', function () { return __awaiter(void 0, void 0, void 0, function () {
            var mockDelete, wrapper, listItems, deleteButton;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        mockDelete = MockApiClient.addMockResponse({
                            url: endpoint,
                            method: 'PUT',
                            body: getOrganization(JSON.stringify(__assign(__assign({}, relayPiiConfig), { rules: { 0: relayPiiConfig.rules[0] } }))),
                        });
                        wrapper = renderComponent({
                            disabled: false,
                            projectId: projectId,
                            endpoint: endpoint,
                        });
                        listItems = wrapper.find('ListItem');
                        deleteButton = listItems.at(0).find('[aria-label="Delete Rule"]').hostNodes();
                        deleteButton.simulate('click');
                        expect(mockDelete).toHaveBeenCalled();
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _a.sent();
                        wrapper.update();
                        expect(wrapper.find('ListItem')).toHaveLength(1);
                        expect(addSuccessMessage).toHaveBeenCalled();
                        return [2 /*return*/];
                }
            });
        }); });
        it('Open Add Rule Modal', function () {
            var wrapper = renderComponent({
                disabled: false,
                projectId: projectId,
                endpoint: endpoint,
            });
            var addbutton = wrapper
                .find('PanelAction')
                .find('[aria-label="Add Rule"]')
                .hostNodes();
            addbutton.simulate('click');
            expect(openModal).toHaveBeenCalled();
        });
        it('Open Edit Rule Modal', function () {
            var wrapper = renderComponent({
                disabled: false,
                projectId: projectId,
                endpoint: endpoint,
            });
            var editButton = wrapper
                .find('PanelBody')
                .find('[aria-label="Edit Rule"]')
                .hostNodes();
            editButton.at(0).simulate('click');
            expect(openModal).toHaveBeenCalled();
        });
    });
});
//# sourceMappingURL=dataScrubbing.spec.jsx.map