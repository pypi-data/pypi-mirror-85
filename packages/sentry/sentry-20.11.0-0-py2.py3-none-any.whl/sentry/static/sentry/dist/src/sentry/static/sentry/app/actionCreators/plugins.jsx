import { __assign, __read, __rest } from "tslib";
import { Client } from 'app/api';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import PluginActions from 'app/actions/pluginActions';
var activeFetch = {};
// PluginsStore always exists, so api client should be independent of component lifecycle
var api = new Client();
function doUpdate(_a) {
    var orgId = _a.orgId, projectId = _a.projectId, pluginId = _a.pluginId, update = _a.update, params = __rest(_a, ["orgId", "projectId", "pluginId", "update"]);
    PluginActions.update(pluginId, update);
    var request = api.requestPromise("/projects/" + orgId + "/" + projectId + "/plugins/" + pluginId + "/", __assign({}, params));
    // This is intentionally not chained because we want the unhandled promise to be returned
    request
        .then(function () {
        PluginActions.updateSuccess(pluginId, update);
    })
        .catch(function (resp) {
        var err = resp && resp.responseJSON && typeof resp.responseJSON.detail === 'string'
            ? new Error(resp.responseJSON.detail)
            : new Error('Unable to update plugin');
        PluginActions.updateError(pluginId, update, err);
    });
    return request;
}
/**
 * Fetches list of available plugins for a project
 */
export function fetchPlugins(_a, options) {
    var orgId = _a.orgId, projectId = _a.projectId;
    var path = "/projects/" + orgId + "/" + projectId + "/plugins/";
    // Make sure we throttle fetches
    if (activeFetch[path]) {
        return activeFetch[path];
    }
    PluginActions.fetchAll(options);
    var request = api.requestPromise(path, {
        method: 'GET',
        includeAllArgs: true,
    });
    activeFetch[path] = request;
    // This is intentionally not chained because we want the unhandled promise to be returned
    request
        .then(function (_a) {
        var _b = __read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
        PluginActions.fetchAllSuccess(data, {
            pageLinks: jqXHR && jqXHR.getResponseHeader('Link'),
        });
        return data;
    })
        .catch(function (err) {
        PluginActions.fetchAllError(err);
        throw new Error('Unable to fetch plugins');
    })
        .then(function () { return (activeFetch[path] = null); });
    return request;
}
/**
 * Enables a plugin
 */
export function enablePlugin(params) {
    addLoadingMessage(t('Enabling...'));
    return doUpdate(__assign(__assign({}, params), { update: { enabled: true }, method: 'POST' }))
        .then(function () { return addSuccessMessage(t('Plugin was enabled')); })
        .catch(function () { return addErrorMessage(t('Unable to enable plugin')); });
}
/**
 * Disables a plugin
 */
export function disablePlugin(params) {
    addLoadingMessage(t('Disabling...'));
    return doUpdate(__assign(__assign({}, params), { update: { enabled: false }, method: 'DELETE' }))
        .then(function () { return addSuccessMessage(t('Plugin was disabled')); })
        .catch(function () { return addErrorMessage(t('Unable to disable plugin')); });
}
//# sourceMappingURL=plugins.jsx.map