import { __assign, __read, __spread } from "tslib";
import findIndex from 'lodash/findIndex';
import Reflux from 'reflux';
import SavedSearchesActions from 'app/actions/savedSearchesActions';
var savedSearchesStoreConfig = {
    state: {
        savedSearches: [],
        hasError: false,
        isLoading: true,
    },
    init: function () {
        var startFetchSavedSearches = SavedSearchesActions.startFetchSavedSearches, fetchSavedSearchesSuccess = SavedSearchesActions.fetchSavedSearchesSuccess, fetchSavedSearchesError = SavedSearchesActions.fetchSavedSearchesError, createSavedSearchSuccess = SavedSearchesActions.createSavedSearchSuccess, deleteSavedSearchSuccess = SavedSearchesActions.deleteSavedSearchSuccess, pinSearch = SavedSearchesActions.pinSearch, pinSearchSuccess = SavedSearchesActions.pinSearchSuccess, resetSavedSearches = SavedSearchesActions.resetSavedSearches, unpinSearch = SavedSearchesActions.unpinSearch;
        this.listenTo(startFetchSavedSearches, this.onStartFetchSavedSearches);
        this.listenTo(fetchSavedSearchesSuccess, this.onFetchSavedSearchesSuccess);
        this.listenTo(fetchSavedSearchesError, this.onFetchSavedSearchesError);
        this.listenTo(resetSavedSearches, this.onReset);
        this.listenTo(createSavedSearchSuccess, this.onCreateSavedSearchSuccess);
        this.listenTo(deleteSavedSearchSuccess, this.onDeleteSavedSearchSuccess);
        this.listenTo(pinSearch, this.onPinSearch);
        this.listenTo(pinSearchSuccess, this.onPinSearchSuccess);
        this.listenTo(unpinSearch, this.onUnpinSearch);
        this.reset();
    },
    reset: function () {
        this.state = {
            savedSearches: [],
            hasError: false,
            isLoading: true,
        };
    },
    get: function () {
        return this.state;
    },
    /**
     * If pinned search, remove from list if user created pin (e.g. not org saved search and not global)
     * Otherwise change `isPinned` to false (e.g. if it's default or org saved search)
     */
    getFilteredSearches: function (type, existingSearchId) {
        return this.state.savedSearches
            .filter(function (savedSearch) {
            return !(savedSearch.isPinned &&
                savedSearch.type === type &&
                !savedSearch.isOrgCustom &&
                !savedSearch.isGlobal &&
                savedSearch.id !== existingSearchId);
        })
            .map(function (savedSearch) {
            if (typeof existingSearchId !== 'undefined' &&
                existingSearchId === savedSearch.id) {
                // Do not update existing search
                return savedSearch;
            }
            return __assign(__assign({}, savedSearch), { isPinned: false });
        });
    },
    updateExistingSearch: function (id, updateObj) {
        var index = findIndex(this.state.savedSearches, function (savedSearch) { return savedSearch.id === id; });
        if (index === -1) {
            return null;
        }
        var existingSavedSearch = this.state.savedSearches[index];
        var newSavedSearch = __assign(__assign({}, existingSavedSearch), updateObj);
        this.state.savedSearches[index] = newSavedSearch;
        return newSavedSearch;
    },
    /**
     * Find saved search by query string
     */
    findByQuery: function (query) {
        return this.state.savedSearches.find(function (savedSearch) { return query === savedSearch.query; });
    },
    /**
     * Reset store to initial state
     */
    onReset: function () {
        this.reset();
        this.trigger(this.state);
    },
    onStartFetchSavedSearches: function () {
        this.state = __assign(__assign({}, this.state), { isLoading: true });
        this.trigger(this.state);
    },
    onFetchSavedSearchesSuccess: function (data) {
        if (!Array.isArray(data)) {
            data = [];
        }
        this.state = __assign(__assign({}, this.state), { savedSearches: data, isLoading: false });
        this.trigger(this.state);
    },
    onFetchSavedSearchesError: function (_resp) {
        this.state = __assign(__assign({}, this.state), { savedSearches: [], isLoading: false, hasError: true });
        this.trigger(this.state);
    },
    onCreateSavedSearchSuccess: function (resp) {
        this.state = __assign(__assign({}, this.state), { savedSearches: __spread(this.state.savedSearches, [resp]) });
        this.trigger(this.state);
    },
    onDeleteSavedSearchSuccess: function (search) {
        this.state = __assign(__assign({}, this.state), { savedSearches: this.state.savedSearches.filter(function (item) { return item.id !== search.id; }) });
        this.trigger(this.state);
    },
    onPinSearch: function (type, query) {
        var existingSearch = this.findByQuery(query);
        if (existingSearch) {
            this.updateExistingSearch(existingSearch.id, { isPinned: true });
        }
        var newPinnedSearch = (!existingSearch && [
            {
                id: null,
                name: 'My Pinned Search',
                type: type,
                query: query,
                isPinned: true,
            },
        ]) ||
            [];
        this.state = __assign(__assign({}, this.state), { savedSearches: __spread(newPinnedSearch, this.getFilteredSearches(type, existingSearch && existingSearch.id)) });
        this.trigger(this.state);
    },
    onPinSearchSuccess: function (resp) {
        var existingSearch = this.findByQuery(resp.query);
        if (existingSearch) {
            this.updateExistingSearch(existingSearch.id, resp);
        }
        this.trigger(this.state);
    },
    onUnpinSearch: function (type) {
        this.state = __assign(__assign({}, this.state), { 
            // Design decision that there can only be 1 pinned search per `type`
            savedSearches: this.getFilteredSearches(type) });
        this.trigger(this.state);
    },
};
export default Reflux.createStore(savedSearchesStoreConfig);
//# sourceMappingURL=savedSearchesStore.jsx.map