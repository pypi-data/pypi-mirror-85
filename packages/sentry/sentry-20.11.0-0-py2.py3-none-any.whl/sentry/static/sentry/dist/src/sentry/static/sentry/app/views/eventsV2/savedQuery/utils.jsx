import { __assign } from "tslib";
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { createSavedQuery, deleteSavedQuery, updateSavedQuery, } from 'app/actionCreators/discoverSavedQueries';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
export function handleCreateQuery(api, organization, eventView, 
// True if this is a brand new query being saved
// False if this is a modification from a saved query
isNewQuery) {
    if (isNewQuery === void 0) { isNewQuery = true; }
    var payload = eventView.toNewQuery();
    trackAnalyticsEvent(__assign(__assign(__assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'request')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)));
    var promise = createSavedQuery(api, organization.slug, payload);
    promise
        .then(function (savedQuery) {
        addSuccessMessage(t('Query saved'));
        trackAnalyticsEvent(__assign(__assign(__assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'success')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)));
        return savedQuery;
    })
        .catch(function (err) {
        addErrorMessage(t('Query not saved'));
        trackAnalyticsEvent(__assign(__assign(__assign(__assign({}, getAnalyticsCreateEventKeyName(isNewQuery, 'failed')), { organization_id: parseInt(organization.id, 10) }), extractAnalyticsQueryFields(payload)), { error: (err && err.message) ||
                "Could not save a " + (isNewQuery ? 'new' : 'existing') + " query" }));
    });
    return promise;
}
var EVENT_NAME_EXISTING_MAP = {
    request: 'Discoverv2: Request to save a saved query as a new query',
    success: 'Discoverv2: Successfully saved a saved query as a new query',
    failed: 'Discoverv2: Failed to save a saved query as a new query',
};
var EVENT_NAME_NEW_MAP = {
    request: 'Discoverv2: Request to save a new query',
    success: 'Discoverv2: Successfully saved a new query',
    failed: 'Discoverv2: Failed to save a new query',
};
export function handleUpdateQuery(api, organization, eventView) {
    var payload = eventView.toNewQuery();
    if (!eventView.name) {
        addErrorMessage(t('Please name your query'));
        return Promise.reject();
    }
    trackAnalyticsEvent(__assign({ eventKey: 'discover_v2.update_query_request', eventName: 'Discoverv2: Request to update a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    var promise = updateSavedQuery(api, organization.slug, payload);
    promise
        .then(function (savedQuery) {
        addSuccessMessage(t('Query updated'));
        trackAnalyticsEvent(__assign({ eventKey: 'discover_v2.update_query_success', eventName: 'Discoverv2: Successfully updated a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
        // NOTE: there is no need to convert _saved into an EventView and push it
        //       to the browser history, since this.props.eventView already
        //       derives from location.
        return savedQuery;
    })
        .catch(function (err) {
        addErrorMessage(t('Query not updated'));
        trackAnalyticsEvent(__assign(__assign({ eventKey: 'discover_v2.update_query_failed', eventName: 'Discoverv2: Failed to update a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)), { error: (err && err.message) || 'Failed to update a query' }));
    });
    return promise;
}
/**
 * Essentially the same as handleUpdateQuery, but specifically for changing the
 * name of the query
 */
export function handleUpdateQueryName(api, organization, eventView) {
    var payload = eventView.toNewQuery();
    trackAnalyticsEvent(__assign({ eventKey: 'discover_v2.update_query_name_request', eventName: "Discoverv2: Request to update a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    var promise = updateSavedQuery(api, organization.slug, payload);
    promise
        .then(function (_saved) {
        addSuccessMessage(t('Query name saved'));
        trackAnalyticsEvent(__assign({ eventKey: 'discover_v2.update_query_name_success', eventName: "Discoverv2: Successfully updated a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)));
    })
        .catch(function (err) {
        addErrorMessage(t('Query name not saved'));
        trackAnalyticsEvent(__assign(__assign({ eventKey: 'discover_v2.update_query_failed', eventName: "Discoverv2: Failed to update a saved query's name", organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(payload)), { error: (err && err.message) || 'Failed to update a query name' }));
    });
    return promise;
}
export function handleDeleteQuery(api, organization, eventView) {
    trackAnalyticsEvent(__assign({ eventKey: 'discover_v2.delete_query_request', eventName: 'Discoverv2: Request to delete a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())));
    var promise = deleteSavedQuery(api, organization.slug, eventView.id);
    promise
        .then(function () {
        addSuccessMessage(t('Query deleted'));
        trackAnalyticsEvent(__assign({ eventKey: 'discover_v2.delete_query_success', eventName: 'Discoverv2: Successfully deleted a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())));
    })
        .catch(function (err) {
        addErrorMessage(t('Query not deleted'));
        trackAnalyticsEvent(__assign(__assign({ eventKey: 'discover_v2.delete_query_failed', eventName: 'Discoverv2: Failed to delete a saved query', organization_id: parseInt(organization.id, 10) }, extractAnalyticsQueryFields(eventView.toNewQuery())), { error: (err && err.message) || 'Failed to delete query' }));
    });
    return promise;
}
export function getAnalyticsCreateEventKeyName(
// True if this is a brand new query being saved
// False if this is a modification from a saved query
isNewQuery, type) {
    var eventKey = isNewQuery
        ? 'discover_v2.save_new_query_' + type
        : 'discover_v2.save_existing_query_' + type;
    var eventName = isNewQuery ? EVENT_NAME_NEW_MAP[type] : EVENT_NAME_EXISTING_MAP[type];
    return {
        eventKey: eventKey,
        eventName: eventName,
    };
}
/**
 * Takes in a DiscoverV2 NewQuery object and returns a Partial containing
 * the desired fields to populate into reload analytics
 */
export function extractAnalyticsQueryFields(payload) {
    var projects = payload.projects, fields = payload.fields, query = payload.query;
    return {
        projects: projects,
        fields: fields,
        query: query,
    };
}
//# sourceMappingURL=utils.jsx.map