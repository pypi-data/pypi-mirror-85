import isEmpty from 'lodash/isEmpty';
import isNull from 'lodash/isNull';
var GET_META = Symbol('GET_META');
var IS_PROXY = Symbol('IS_PROXY');
function isAnnotated(meta) {
    if (isEmpty(meta)) {
        return false;
    }
    return !isEmpty(meta.rem) || !isEmpty(meta.err);
}
var MetaProxy = /** @class */ (function () {
    function MetaProxy(local) {
        this.local = local;
    }
    MetaProxy.prototype.get = function (obj, prop, receiver) {
        var _this = this;
        // trap calls to `getMeta` to return meta object
        if (prop === GET_META) {
            return function (key) {
                if (_this.local && _this.local[key] && _this.local[key]['']) {
                    // TODO: Error checks
                    var meta = _this.local[key][''];
                    return isAnnotated(meta) ? meta : undefined;
                }
                return undefined;
            };
        }
        // this is how  we can determine if current `obj` is a proxy
        if (prop === IS_PROXY) {
            return true;
        }
        var value = Reflect.get(obj, prop, receiver);
        if (!Reflect.has(obj, prop) || typeof value !== 'object' || isNull(value)) {
            return value;
        }
        // This is so we don't create a new Proxy from an object that is
        // already a proxy. Otherwise we can get into very deep recursive calls
        if (Reflect.get(obj, IS_PROXY, receiver)) {
            return value;
        }
        // Make sure we apply proxy to all children (objects and arrays)
        // Do we need to check for annotated inside of objects?
        return new Proxy(value, new MetaProxy(this.local && this.local[prop]));
    };
    return MetaProxy;
}());
export { MetaProxy };
export function withMeta(event) {
    if (!event) {
        return event;
    }
    // Return unproxied `event` if browser does not support `Proxy`
    if (typeof window.Proxy === 'undefined' || typeof window.Reflect === 'undefined') {
        return event;
    }
    // withMeta returns a type that is supposed to be 100% compatible with its
    // input type. Proxy typing on typescript is not really functional enough to
    // make this work without casting.
    //
    // https://github.com/microsoft/TypeScript/issues/20846
    return new Proxy(event, new MetaProxy(event._meta));
}
export function getMeta(obj, prop) {
    if (!obj || typeof obj[GET_META] !== 'function') {
        return undefined;
    }
    return obj[GET_META](prop);
}
//# sourceMappingURL=metaProxy.jsx.map