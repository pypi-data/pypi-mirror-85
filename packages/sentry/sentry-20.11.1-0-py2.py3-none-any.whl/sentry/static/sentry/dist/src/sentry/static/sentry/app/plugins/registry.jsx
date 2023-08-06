/*eslint no-console:0*/
import { DefaultPlugin } from 'app/plugins/defaultPlugin';
import { DefaultIssuePlugin } from 'app/plugins/defaultIssuePlugin';
import { defined } from 'app/utils';
var Registry = /** @class */ (function () {
    function Registry() {
        this.plugins = {};
        this.assetCache = {};
    }
    Registry.prototype.isLoaded = function (data) {
        return defined(this.plugins[data.id]);
    };
    Registry.prototype.load = function (data, callback) {
        var _this = this;
        var remainingAssets = data.assets.length;
        // TODO(dcramer): we should probably register all valid plugins
        var finishLoad = function () {
            if (!defined(_this.plugins[data.id])) {
                if (data.type === 'issue-tracking') {
                    _this.plugins[data.id] = DefaultIssuePlugin;
                }
                else {
                    _this.plugins[data.id] = DefaultPlugin;
                }
            }
            console.info('[plugins] Loaded ' + data.id + ' as {' + _this.plugins[data.id].name + '}');
            callback(_this.get(data));
        };
        if (remainingAssets === 0) {
            finishLoad();
            return;
        }
        var onAssetLoaded = function () {
            remainingAssets--;
            if (remainingAssets === 0) {
                finishLoad();
            }
        };
        var onAssetFailed = function (asset) {
            remainingAssets--;
            console.error('[plugins] Failed to load asset ' + asset.url);
            if (remainingAssets === 0) {
                finishLoad();
            }
        };
        // TODO(dcramer): what do we do on failed asset loading?
        data.assets.forEach(function (asset) {
            if (!defined(_this.assetCache[asset.url])) {
                console.info('[plugins] Loading asset for ' + data.id + ': ' + asset.url);
                var s = document.createElement('script');
                s.src = asset.url;
                s.onload = onAssetLoaded.bind(_this);
                s.onerror = onAssetFailed.bind(_this, asset);
                s.async = true;
                document.body.appendChild(s);
                _this.assetCache[asset.url] = s;
            }
            else {
                onAssetLoaded();
            }
        });
    };
    Registry.prototype.get = function (data) {
        var cls = this.plugins[data.id];
        if (!defined(cls)) {
            throw new Error('Attempted to ``get`` an unloaded plugin: ' + data.id);
        }
        return new cls(data);
    };
    Registry.prototype.add = function (id, cls) {
        this.plugins[id] = cls;
    };
    return Registry;
}());
export default Registry;
//# sourceMappingURL=registry.jsx.map