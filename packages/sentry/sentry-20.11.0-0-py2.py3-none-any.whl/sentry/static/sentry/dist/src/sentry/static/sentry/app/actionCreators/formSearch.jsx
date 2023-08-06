import { __assign, __rest } from "tslib";
import flatten from 'lodash/flatten';
import flatMap from 'lodash/flatMap';
import FormSearchActions from 'app/actions/formSearchActions';
/**
 * Creates a list of objects to be injected by a search source
 *
 * @param route The route a form field belongs on
 * @param formGroups An array of `FormGroup: {title: String, fields: [Field]}`
 * @param fields An object whose key is field name and value is a `Field`
 */
var createSearchMap = function (_a) {
    var route = _a.route, formGroups = _a.formGroups, fields = _a.fields, other = __rest(_a, ["route", "formGroups", "fields"]);
    // There are currently two ways to define forms (TODO(billy): Turn this into one):
    // If `formGroups` is defined, then return a flattened list of fields in all formGroups
    // Otherwise `fields` is a map of fieldName -> fieldObject -- create a list of fields
    var listOfFields = formGroups
        ? flatMap(formGroups, function (formGroup) { return formGroup.fields; })
        : Object.keys(fields).map(function (fieldName) { return fields[fieldName]; });
    return listOfFields.map(function (field) { return (__assign(__assign({}, other), { route: route, title: typeof field !== 'function' ? field.label : null, description: typeof field !== 'function' ? field.help : null, field: field })); });
};
export function loadSearchMap() {
    // Load all form configuration files via webpack that export a named `route`
    // as well as either `fields` or `formGroups`
    // @ts-ignore This fails on cloud builder, but not in CI...
    var context = require.context('../data/forms', true, /\.[tj]sx?$/);
    // Get a list of all form fields defined in `../data/forms`
    var allFormFields = flatten(context
        .keys()
        .map(function (key) {
        var mod = context(key);
        // Since we're dynamically importing an entire directly, there could be malformed modules defined?
        if (!mod) {
            return null;
        }
        // Only look for module that have `route` exported
        if (!mod.route) {
            return null;
        }
        return createSearchMap({
            // `formGroups` can be a default export or a named export :<
            formGroups: mod.default || mod.formGroups,
            fields: mod.fields,
            route: mod.route,
        });
    })
        .filter(function (i) { return !!i; }));
    FormSearchActions.loadSearchMap(allFormFields);
}
//# sourceMappingURL=formSearch.jsx.map