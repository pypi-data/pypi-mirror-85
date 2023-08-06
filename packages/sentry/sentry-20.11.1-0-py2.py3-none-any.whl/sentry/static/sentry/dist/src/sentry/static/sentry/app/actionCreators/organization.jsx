import { __awaiter, __generator, __read } from "tslib";
import * as Sentry from '@sentry/react';
import { Client } from 'app/api';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { setActiveOrganization } from 'app/actionCreators/organizations';
import GlobalSelectionActions from 'app/actions/globalSelectionActions';
import OrganizationActions from 'app/actions/organizationActions';
import ProjectActions from 'app/actions/projectActions';
import ProjectsStore from 'app/stores/projectsStore';
import TeamActions from 'app/actions/teamActions';
import TeamStore from 'app/stores/teamStore';
/**
 * Fetches an organization's details with an option for the detailed representation
 * with teams and projects
 *
 * @param api A reference to the api client
 * @param slug The organization slug
 * @param detailed Whether or not the detailed org details should be retrieved
 * @param silent Should we silently update the organization (do not clear the
 *               current organization in the store)
 */
export function fetchOrganizationDetails(api, slug, detailed, silent) {
    var _a, _b, _c, _d, _e;
    return __awaiter(this, void 0, void 0, function () {
        var org, uncancelableApi, _f, projects, teams, err_1, err_2, errMessage;
        return __generator(this, function (_g) {
            switch (_g.label) {
                case 0:
                    if (!silent) {
                        OrganizationActions.fetchOrg();
                        ProjectActions.reset();
                        GlobalSelectionActions.reset();
                    }
                    _g.label = 1;
                case 1:
                    _g.trys.push([1, 8, , 9]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + slug + "/", {
                            query: { detailed: detailed ? 1 : 0 },
                        })];
                case 2:
                    org = _g.sent();
                    if (!org) {
                        OrganizationActions.fetchOrgError(new Error('retrieved organization is falsey'));
                        return [2 /*return*/];
                    }
                    OrganizationActions.update(org, { replace: true });
                    setActiveOrganization(org);
                    if (!detailed) return [3 /*break*/, 3];
                    // TODO(davidenwang): Change these to actions after organization.projects
                    // and organization.teams no longer exists. Currently if they were changed
                    // to actions it would cause OrganizationContext to rerender many times
                    TeamStore.loadInitialData(org.teams);
                    ProjectsStore.loadInitialData(org.projects);
                    return [3 /*break*/, 7];
                case 3:
                    uncancelableApi = new Client();
                    _g.label = 4;
                case 4:
                    _g.trys.push([4, 6, , 7]);
                    return [4 /*yield*/, Promise.all([
                            uncancelableApi.requestPromise("/organizations/" + slug + "/projects/", {
                                query: {
                                    all_projects: 1,
                                },
                            }),
                            uncancelableApi.requestPromise("/organizations/" + slug + "/teams/"),
                        ])];
                case 5:
                    _f = __read.apply(void 0, [_g.sent(), 2]), projects = _f[0], teams = _f[1];
                    ProjectActions.loadProjects(projects);
                    TeamActions.loadTeams(teams);
                    return [3 /*break*/, 7];
                case 6:
                    err_1 = _g.sent();
                    // It's possible these requests fail with a 403 if the user has a role with insufficient access
                    // to projects and teams, but *can* access org details (e.g. billing).
                    // An example of this is in org settings.
                    //
                    // Ignore 403s and bubble up other API errors
                    if (err_1.status !== 403) {
                        throw err_1;
                    }
                    return [3 /*break*/, 7];
                case 7: return [3 /*break*/, 9];
                case 8:
                    err_2 = _g.sent();
                    if (!err_2) {
                        return [2 /*return*/];
                    }
                    OrganizationActions.fetchOrgError(err_2);
                    if (err_2.status === 403 || err_2.status === 401) {
                        errMessage = typeof ((_a = err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === 'string'
                            ? (_b = err_2.responseJSON) === null || _b === void 0 ? void 0 : _b.detail : typeof ((_d = (_c = err_2.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.message) === 'string'
                            ? (_e = err_2.responseJSON) === null || _e === void 0 ? void 0 : _e.detail.message : null;
                        if (errMessage) {
                            addErrorMessage(errMessage);
                        }
                        return [2 /*return*/];
                    }
                    Sentry.captureException(err_2);
                    return [3 /*break*/, 9];
                case 9: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=organization.jsx.map