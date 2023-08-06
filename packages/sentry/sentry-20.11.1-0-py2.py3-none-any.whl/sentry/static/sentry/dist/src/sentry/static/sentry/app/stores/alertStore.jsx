import Reflux from 'reflux';
import AlertActions from 'app/actions/alertActions';
import localStorage from 'app/utils/localStorage';
import { defined } from 'app/utils';
var storeConfig = {
    listenables: AlertActions,
    alerts: [],
    count: 0,
    init: function () {
        this.alerts = [];
        this.count = 0;
    },
    onAddAlert: function (alert) {
        var _this = this;
        var alertAlreadyExists = this.alerts.some(function (a) { return a.id === alert.id; });
        if (alertAlreadyExists && alert.noDuplicates) {
            return;
        }
        if (defined(alert.id)) {
            var mutedData = localStorage.getItem('alerts:muted');
            if (typeof mutedData === 'string' && mutedData.length) {
                var expirations = JSON.parse(mutedData);
                // Remove any objects that have passed their mute duration.
                var now = Math.floor(new Date().valueOf() / 1000);
                for (var key in expirations) {
                    if (expirations.hasOwnProperty(key) && expirations[key] < now) {
                        delete expirations[key];
                    }
                }
                localStorage.setItem('alerts:muted', JSON.stringify(expirations));
                if (expirations.hasOwnProperty(alert.id)) {
                    return;
                }
            }
        }
        else {
            if (!defined(alert.expireAfter)) {
                alert.expireAfter = 5000;
            }
        }
        if (alert.expireAfter && !alert.neverExpire) {
            window.setTimeout(function () {
                _this.onCloseAlert(alert);
            }, alert.expireAfter);
        }
        alert.key = this.count++;
        // intentionally recreate array via concat because of Reflux
        // "bug" where React components are given same reference to tracked
        // data objects, and don't *see* that values have changed
        this.alerts = this.alerts.concat([alert]);
        this.trigger(this.alerts);
    },
    onCloseAlert: function (alert, duration) {
        if (duration === void 0) { duration = 60 * 60 * 7 * 24; }
        if (defined(alert.id) && defined(duration)) {
            var expiry = Math.floor(new Date().valueOf() / 1000) + duration;
            var mutedData = localStorage.getItem('alerts:muted');
            var expirations = {};
            if (typeof mutedData === 'string' && expirations.length) {
                expirations = JSON.parse(mutedData);
            }
            expirations[alert.id] = expiry;
            localStorage.setItem('alerts:muted', JSON.stringify(expirations));
        }
        // TODO(dcramer): we need some animations here for closing alerts
        this.alerts = this.alerts.filter(function (item) { return alert !== item; });
        this.trigger(this.alerts);
    },
};
export default Reflux.createStore(storeConfig);
//# sourceMappingURL=alertStore.jsx.map