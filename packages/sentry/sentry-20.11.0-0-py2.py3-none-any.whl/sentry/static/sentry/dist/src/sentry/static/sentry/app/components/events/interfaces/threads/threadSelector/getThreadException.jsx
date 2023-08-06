import { __values } from "tslib";
import { defined } from 'app/utils';
function getThreadException(thread, event) {
    var e_1, _a;
    var exceptionEntry = event.entries.find(function (entry) { return entry.type === 'exception'; });
    if (!exceptionEntry) {
        return undefined;
    }
    var exceptionData = exceptionEntry.data;
    var exceptionDataValues = exceptionEntry.data.values;
    if (!(exceptionDataValues === null || exceptionDataValues === void 0 ? void 0 : exceptionDataValues.length)) {
        return undefined;
    }
    if (exceptionDataValues.length === 1 && !defined(exceptionDataValues[0].threadId)) {
        return exceptionData;
    }
    try {
        for (var exceptionDataValues_1 = __values(exceptionDataValues), exceptionDataValues_1_1 = exceptionDataValues_1.next(); !exceptionDataValues_1_1.done; exceptionDataValues_1_1 = exceptionDataValues_1.next()) {
            var exc = exceptionDataValues_1_1.value;
            if (exc.threadId === thread.id) {
                return exceptionData;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (exceptionDataValues_1_1 && !exceptionDataValues_1_1.done && (_a = exceptionDataValues_1.return)) _a.call(exceptionDataValues_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return undefined;
}
export default getThreadException;
//# sourceMappingURL=getThreadException.jsx.map