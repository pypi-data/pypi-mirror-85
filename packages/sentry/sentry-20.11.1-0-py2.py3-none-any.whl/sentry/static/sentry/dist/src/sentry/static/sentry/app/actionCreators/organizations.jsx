import { __awaiter, __generator } from "tslib";
import { browserHistory } from 'react-router';
import { Client } from 'app/api';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { resetGlobalSelection } from 'app/actionCreators/globalSelection';
import OrganizationActions from 'app/actions/organizationActions';
import OrganizationsActions from 'app/actions/organizationsActions';
import OrganizationsStore from 'app/stores/organizationsStore';
import ProjectsStore from 'app/stores/projectsStore';
import TeamStore from 'app/stores/teamStore';
/**
 * After removing an organization, this will redirect to a remaining active organization or
 * the screen to create a new organization.
 *
 * Can optionally remove organization from organizations store.
 */
export function redirectToRemainingOrganization(_a) {
    var orgId = _a.orgId, removeOrg = _a.removeOrg;
    // Remove queued, should redirect
    var allOrgs = OrganizationsStore.getAll().filter(function (org) { return org.status.id === 'active' && org.slug !== orgId; });
    if (!allOrgs.length) {
        browserHistory.push('/organizations/new/');
        return;
    }
    // Let's be smart and select the best org to redirect to
    var firstRemainingOrg = allOrgs[0];
    browserHistory.push("/" + firstRemainingOrg.slug + "/");
    // Remove org from SidebarDropdown
    if (removeOrg) {
        OrganizationsStore.remove(orgId);
    }
}
export function remove(api, _a) {
    var successMessage = _a.successMessage, errorMessage = _a.errorMessage, orgId = _a.orgId;
    var endpoint = "/organizations/" + orgId + "/";
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(function () {
        OrganizationsActions.removeSuccess(orgId);
        if (successMessage) {
            addSuccessMessage(successMessage);
        }
    })
        .catch(function () {
        OrganizationsActions.removeError();
        if (errorMessage) {
            addErrorMessage(errorMessage);
        }
    });
}
export function switchOrganization() {
    resetGlobalSelection();
}
export function removeAndRedirectToRemainingOrganization(api, params) {
    remove(api, params).then(function () { return redirectToRemainingOrganization(params); });
}
/**
 * Set active organization
 */
export function setActiveOrganization(org) {
    OrganizationsActions.setActive(org);
}
export function changeOrganizationSlug(prev, next) {
    OrganizationsActions.changeSlug(prev, next);
}
/**
 * Updates an organization for the store
 *
 * Accepts a partial organization as it will merge will existing organization
 */
export function updateOrganization(org) {
    OrganizationsActions.update(org);
    OrganizationActions.update(org);
}
export function fetchOrganizationByMember(memberId, _a) {
    var addOrg = _a.addOrg, fetchOrgDetails = _a.fetchOrgDetails;
    return __awaiter(this, void 0, void 0, function () {
        var api, data, org;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new Client();
                    return [4 /*yield*/, api.requestPromise("/organizations/?query=member_id:" + memberId)];
                case 1:
                    data = _b.sent();
                    if (!data.length) {
                        return [2 /*return*/, null];
                    }
                    org = data[0];
                    if (addOrg) {
                        // add org to SwitchOrganization dropdown
                        OrganizationsStore.add(org);
                    }
                    if (!fetchOrgDetails) return [3 /*break*/, 3];
                    // load SidebarDropdown with org details including `access`
                    return [4 /*yield*/, fetchOrganizationDetails(org.slug, { setActive: true, loadProjects: true })];
                case 2:
                    // load SidebarDropdown with org details including `access`
                    _b.sent();
                    _b.label = 3;
                case 3: return [2 /*return*/, org];
            }
        });
    });
}
export function fetchOrganizationDetails(orgId, _a) {
    var setActive = _a.setActive, loadProjects = _a.loadProjects, loadTeam = _a.loadTeam;
    return __awaiter(this, void 0, void 0, function () {
        var api, data;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new Client();
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/")];
                case 1:
                    data = _b.sent();
                    if (setActive) {
                        setActiveOrganization(data);
                    }
                    if (loadTeam) {
                        TeamStore.loadInitialData(data.teams);
                    }
                    if (loadProjects) {
                        ProjectsStore.loadInitialData(data.projects || []);
                    }
                    return [2 /*return*/, data];
            }
        });
    });
}
//# sourceMappingURL=organizations.jsx.map