import { __values } from "tslib";
import getThreadException from './getThreadException';
// TODO(ts): define raw type
function getThreadStacktrace(thread, event, raw) {
    var e_1, _a;
    var exc = getThreadException(thread, event);
    if (exc) {
        var rv = undefined;
        if (!exc.values) {
            return rv;
        }
        try {
            for (var _b = __values(exc.values), _c = _b.next(); !_c.done; _c = _b.next()) {
                var singleExc = _c.value;
                if (singleExc.threadId === thread.id) {
                    rv = (raw && singleExc.rawStacktrace) || singleExc.stacktrace;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return rv;
    }
    if (raw && thread.rawStacktrace) {
        return thread.rawStacktrace;
    }
    if (thread.stacktrace) {
        return thread.stacktrace;
    }
    return undefined;
}
export default getThreadStacktrace;
//# sourceMappingURL=getThreadStacktrace.jsx.map