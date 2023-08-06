import { __assign } from "tslib";
import Reflux from 'reflux';
import isEqual from 'lodash/isEqual';
import { LOCAL_STORAGE_KEY } from 'app/constants/globalSelectionHeader';
import { getDefaultSelection } from 'app/components/organizations/globalSelectionHeader/utils';
import { isEqualWithDates } from 'app/utils/isEqualWithDates';
import GlobalSelectionActions from 'app/actions/globalSelectionActions';
import OrganizationsStore from 'app/stores/organizationsStore';
import localStorage from 'app/utils/localStorage';
var storeConfig = {
    state: getDefaultSelection(),
    init: function () {
        this.reset(this.state);
        this.listenTo(GlobalSelectionActions.reset, this.onReset);
        this.listenTo(GlobalSelectionActions.initializeUrlState, this.onInitializeUrlState);
        this.listenTo(GlobalSelectionActions.setOrganization, this.onSetOrganization);
        this.listenTo(GlobalSelectionActions.save, this.onSave);
        this.listenTo(GlobalSelectionActions.updateProjects, this.updateProjects);
        this.listenTo(GlobalSelectionActions.updateDateTime, this.updateDateTime);
        this.listenTo(GlobalSelectionActions.updateEnvironments, this.updateEnvironments);
    },
    reset: function (state) {
        // Has passed the enforcement state
        this._hasEnforcedProject = false;
        this._hasInitialState = false;
        this.state = state || getDefaultSelection();
    },
    isReady: function () {
        return this._hasInitialState;
    },
    onSetOrganization: function (organization) {
        this.organization = organization;
    },
    /**
     * Initializes the global selection store data
     */
    onInitializeUrlState: function (newSelection) {
        this._hasInitialState = true;
        this.state = newSelection;
        this.trigger(this.get());
    },
    get: function () {
        return {
            selection: this.state,
            isReady: this.isReady(),
        };
    },
    onReset: function () {
        this.reset();
        this.trigger(this.get());
    },
    updateProjects: function (projects, environments) {
        if (projects === void 0) { projects = []; }
        if (environments === void 0) { environments = null; }
        if (isEqual(this.state.projects, projects)) {
            return;
        }
        this.state = __assign(__assign({}, this.state), { projects: projects, environments: environments === null ? this.state.environments : environments });
        this.trigger(this.get());
    },
    updateDateTime: function (datetime) {
        if (isEqualWithDates(this.state.datetime, datetime)) {
            return;
        }
        this.state = __assign(__assign({}, this.state), { datetime: datetime });
        this.trigger(this.get());
    },
    updateEnvironments: function (environments) {
        if (isEqual(this.state.environments, environments)) {
            return;
        }
        this.state = __assign(__assign({}, this.state), { environments: environments !== null && environments !== void 0 ? environments : [] });
        this.trigger(this.get());
    },
    /**
     * Save to local storage when user explicitly changes header values.
     *
     * e.g. if localstorage is empty, user loads issue details for project "foo"
     * this should not consider "foo" as last used and should not save to local storage.
     *
     * However, if user then changes environment, it should...? Currently it will
     * save the current project alongside environment to local storage. It's debatable if
     * this is the desired behavior.
     */
    onSave: function (updateObj) {
        // Do nothing if no org is loaded or user is not an org member. Only
        // organizations that a user has membership in will be available via the
        // organizations store
        if (!this.organization || !OrganizationsStore.get(this.organization.slug)) {
            return;
        }
        var project = updateObj.project, environment = updateObj.environment;
        var validatedProject = typeof project === 'string' ? [Number(project)] : project;
        var validatedEnvironment = typeof environment === 'string' ? [environment] : environment;
        try {
            var localStorageKey = LOCAL_STORAGE_KEY + ":" + this.organization.slug;
            var dataToSave = {
                projects: validatedProject || this.selection.projects,
                environments: validatedEnvironment || this.selection.environments,
            };
            localStorage.setItem(localStorageKey, JSON.stringify(dataToSave));
        }
        catch (ex) {
            // Do nothing
        }
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=globalSelectionStore.jsx.map