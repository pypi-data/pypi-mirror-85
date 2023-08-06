import { __assign } from "tslib";
import Reflux from 'reflux';
import RepoActions from 'app/actions/repositoryActions';
export var RepositoryStoreConfig = {
    listenables: RepoActions,
    state: {
        orgSlug: undefined,
        repositories: undefined,
        repositoriesLoading: undefined,
        repositoriesError: undefined,
    },
    init: function () {
        this.resetRepositories();
    },
    resetRepositories: function () {
        this.state = {
            orgSlug: undefined,
            repositories: undefined,
            repositoriesLoading: undefined,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositories: function (orgSlug) {
        this.state = {
            orgSlug: orgSlug,
            repositories: orgSlug === this.state.orgSlug ? this.state.repositories : undefined,
            repositoriesLoading: true,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositoriesError: function (err) {
        this.state = __assign(__assign({}, this.state), { repositories: undefined, repositoriesLoading: false, repositoriesError: err });
        this.trigger(this.state);
    },
    loadRepositoriesSuccess: function (data) {
        this.state = __assign(__assign({}, this.state), { repositories: data, repositoriesLoading: false, repositoriesError: undefined });
        this.trigger(this.state);
    },
    get: function () {
        return __assign({}, this.state);
    },
};
export default Reflux.createStore(RepositoryStoreConfig);
//# sourceMappingURL=repositoryStore.jsx.map