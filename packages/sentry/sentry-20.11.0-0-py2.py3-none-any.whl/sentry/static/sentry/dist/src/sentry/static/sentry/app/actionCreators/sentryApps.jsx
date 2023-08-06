import { addErrorMessage, addLoadingMessage, addSuccessMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
/**
 * Remove a Sentry Application
 *
 * @param {Object} client ApiClient
 * @param {Object} app SentryApp
 */
export function removeSentryApp(client, app) {
    addLoadingMessage();
    var promise = client.requestPromise("/sentry-apps/" + app.slug + "/", {
        method: 'DELETE',
    });
    promise.then(function () {
        addSuccessMessage(t('%s successfully removed.', app.slug));
    }, function () {
        clearIndicators();
        addErrorMessage(t('Unable to remove %s integration', app.slug));
    });
    return promise;
}
//# sourceMappingURL=sentryApps.jsx.map