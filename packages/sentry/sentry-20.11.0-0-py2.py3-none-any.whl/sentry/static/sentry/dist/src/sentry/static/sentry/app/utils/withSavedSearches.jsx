import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import SavedSearchesStore from 'app/stores/savedSearchesStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Currently wraps component with organization from context
 */
var withSavedSearches = function (WrappedComponent) {
    return createReactClass({
        displayName: "withSavedSearches(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(SavedSearchesStore, 'onUpdate')],
        getInitialState: function () {
            return SavedSearchesStore.get();
        },
        onUpdate: function (newState) {
            this.setState(newState);
        },
        render: function () {
            var _a = this.props, params = _a.params, location = _a.location, savedSearchLoading = _a.savedSearchLoading, savedSearchProp = _a.savedSearch, savedSearchesProp = _a.savedSearches;
            var searchId = params.searchId;
            var _b = this.state, savedSearches = _b.savedSearches, isLoading = _b.isLoading;
            var savedSearch = null;
            // Switch to the current saved search or pinned result if available
            if (!isLoading && savedSearches) {
                if (searchId) {
                    var match = savedSearches.find(function (search) { return search.id === searchId; });
                    savedSearch = match ? match : null;
                }
                // If there's no direct saved search being requested (via URL route)
                // *AND* there's no query in URL, then check if there is pinned search
                //
                // Note: Don't use pinned searches when there is an empty query (query === empty string)
                if (!savedSearch && typeof location.query.query === 'undefined') {
                    var pin = savedSearches.find(function (search) { return search.isPinned; });
                    savedSearch = pin ? pin : null;
                }
            }
            return (<WrappedComponent {...this.props} savedSearches={savedSearchesProp !== null && savedSearchesProp !== void 0 ? savedSearchesProp : savedSearches} savedSearchLoading={savedSearchLoading !== null && savedSearchLoading !== void 0 ? savedSearchLoading : isLoading} savedSearch={savedSearchProp !== null && savedSearchProp !== void 0 ? savedSearchProp : savedSearch}/>);
        },
    });
};
export default withSavedSearches;
//# sourceMappingURL=withSavedSearches.jsx.map