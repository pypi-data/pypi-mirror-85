import Reflux from 'reflux';
import EnvironmentActions from 'app/actions/environmentActions';
import { getDisplayName, getUrlRoutingName } from 'app/utils/environment';
var storeConfig = {
    state: {
        environments: null,
        error: null,
    },
    init: function () {
        this.state = { environments: null, error: null };
        this.listenTo(EnvironmentActions.fetchEnvironments, this.onFetchEnvironments);
        this.listenTo(EnvironmentActions.fetchEnvironmentsSuccess, this.onFetchEnvironmentsSuccess);
        this.listenTo(EnvironmentActions.fetchEnvironmentsError, this.onFetchEnvironmentsError);
    },
    makeEnvironment: function (item) {
        return {
            id: item.id,
            name: item.name,
            get displayName() {
                return getDisplayName(item);
            },
            get urlRoutingName() {
                return getUrlRoutingName(item);
            },
        };
    },
    onFetchEnvironments: function () {
        this.state = { environments: null, error: null };
        this.trigger(this.state);
    },
    onFetchEnvironmentsSuccess: function (environments) {
        this.state = { error: null, environments: environments.map(this.makeEnvironment) };
        this.trigger(this.state);
    },
    onFetchEnvironmentsError: function (error) {
        this.state = { error: error, environments: null };
        this.trigger(this.state);
    },
    get: function () {
        return this.state;
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=organizationEnvironmentsStore.jsx.map