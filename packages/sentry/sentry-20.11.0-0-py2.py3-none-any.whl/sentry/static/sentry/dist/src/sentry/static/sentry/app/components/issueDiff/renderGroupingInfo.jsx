import { __values } from "tslib";
import { t } from 'app/locale';
function renderGroupingInfo(groupingInfo) {
    return Object.values(groupingInfo).map(renderGroupVariant).flat();
}
function renderGroupVariant(variant) {
    var title = [t('Type: %s', variant.type)];
    if (variant.hash) {
        title.push(t('Hash: %s', variant.hash));
    }
    if (variant.description) {
        title.push(t('Description: %s', variant.description));
    }
    var rv = [title.join('\n')];
    if (variant.component) {
        rv.push(renderComponent(variant.component).join('\n'));
    }
    return rv;
}
function renderComponent(component) {
    var e_1, _a, e_2, _b;
    if (!component.contributes) {
        return [];
    }
    var name = component.name, id = component.id, hint = component.hint;
    var name_or_id = name || id;
    var title = name_or_id && hint ? name_or_id + " (" + hint + ")" : name_or_id;
    var rv = title ? [title] : [];
    if (component.values) {
        try {
            for (var _c = __values(component.values), _d = _c.next(); !_d.done; _d = _c.next()) {
                var value = _d.value;
                if (typeof value === 'string') {
                    rv.push("  " + value);
                    continue;
                }
                try {
                    for (var _e = (e_2 = void 0, __values(renderComponent(value))), _f = _e.next(); !_f.done; _f = _e.next()) {
                        var line = _f.value;
                        rv.push("  " + line);
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    return rv;
}
export default renderGroupingInfo;
//# sourceMappingURL=renderGroupingInfo.jsx.map