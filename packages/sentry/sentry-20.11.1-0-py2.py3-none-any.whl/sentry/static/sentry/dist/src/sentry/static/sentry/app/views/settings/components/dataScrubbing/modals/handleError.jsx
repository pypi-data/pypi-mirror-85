import { __values } from "tslib";
import { t } from 'app/locale';
export var ErrorType;
(function (ErrorType) {
    ErrorType["Unknown"] = "unknown";
    ErrorType["InvalidSelector"] = "invalid-selector";
    ErrorType["RegexParse"] = "regex-parse";
})(ErrorType || (ErrorType = {}));
function handleError(error) {
    var e_1, _a, e_2, _b;
    var _c;
    var errorMessage = (_c = error.responseJSON) === null || _c === void 0 ? void 0 : _c.relayPiiConfig[0];
    if (!errorMessage) {
        return {
            type: ErrorType.Unknown,
            message: t('Unknown error occurred while saving data scrubbing rule'),
        };
    }
    if (errorMessage.startsWith('invalid selector: ')) {
        try {
            for (var _d = __values(errorMessage.split('\n')), _e = _d.next(); !_e.done; _e = _d.next()) {
                var line = _e.value;
                if (line.startsWith('1 | ')) {
                    var selector = line.slice(3);
                    return {
                        type: ErrorType.InvalidSelector,
                        message: t('Invalid source value: %s', selector),
                    };
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    if (errorMessage.startsWith('regex parse error:')) {
        try {
            for (var _f = __values(errorMessage.split('\n')), _g = _f.next(); !_g.done; _g = _f.next()) {
                var line = _g.value;
                if (line.startsWith('error:')) {
                    var regex = line.slice(6).replace(/at line \d+ column \d+/, '');
                    return {
                        type: ErrorType.RegexParse,
                        message: t('Invalid regex: %s', regex),
                    };
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
            }
            finally { if (e_2) throw e_2.error; }
        }
    }
    return {
        type: ErrorType.Unknown,
        message: t('An unknown error occurred while saving data scrubbing rule'),
    };
}
export default handleError;
//# sourceMappingURL=handleError.jsx.map