import { __makeTemplateObject, __read, __spread, __values } from "tslib";
import React from 'react';
import Jed from 'jed';
import { sprintf } from 'sprintf-js';
import isString from 'lodash/isString';
import isArray from 'lodash/isArray';
import isObject from 'lodash/isObject';
import { css } from '@emotion/core';
import { getTranslations } from 'app/translations';
var markerCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: #ff801790;\n  outline: 2px solid #ff801790;\n"], ["\n  background: #ff801790;\n  outline: 2px solid #ff801790;\n"])));
var sessionStorage = window.sessionStorage;
var LOCALE_DEBUG = sessionStorage && sessionStorage.getItem('localeDebug') === '1';
export function setLocaleDebug(value) {
    sessionStorage.setItem('localeDebug', value ? '1' : '0');
    // eslint-disable-next-line no-console
    console.log("Locale debug is: " + (value ? 'on' : 'off') + ". Reload page to apply changes!");
}
export function toggleLocaleDebug() {
    var currentValue = sessionStorage.getItem('localeDebug');
    setLocaleDebug(currentValue !== '1');
    window.location.reload();
}
/**
 * Global Jed locale object loaded with translations via setLocale
 */
var i18n = null;
/**
 * Set the current application locale.
 *
 * NOTE: This MUST be called early in the application before calls to any
 * translation functions, as this mutates a singleton translation object used
 * to lookup translations at runtime.
 */
export function setLocale(locale) {
    var translations = getTranslations(locale);
    i18n = new Jed({
        domain: 'sentry',
        missing_key_callback: function () { },
        locale_data: {
            sentry: translations,
        },
    });
}
setLocale('en');
/**
 * printf style string formatting which render as react nodes.
 */
function formatForReact(formatString, args) {
    var nodes = [];
    var cursor = 0;
    // always re-parse, do not cache, because we change the match
    sprintf.parse(formatString).forEach(function (match, idx) {
        if (isString(match)) {
            nodes.push(match);
            return;
        }
        var arg = null;
        if (match[2]) {
            arg = args[0][match[2][0]];
        }
        else if (match[1]) {
            arg = args[parseInt(match[1], 10) - 1];
        }
        else {
            arg = args[cursor++];
        }
        // this points to a react element!
        if (React.isValidElement(arg)) {
            nodes.push(React.cloneElement(arg, { key: idx }));
        }
        else {
            // not a react element, fuck around with it so that sprintf.format
            // can format it for us.  We make sure match[2] is null so that we
            // do not go down the object path, and we set match[1] to the first
            // index and then pass an array with two items in.
            match[2] = null;
            match[1] = 1;
            nodes.push(<span key={idx++}>{sprintf.format([match], [null, arg])}</span>);
        }
    });
    return nodes;
}
/**
 * Determine if any arguments include React elements.
 */
function argsInvolveReact(args) {
    if (args.some(React.isValidElement)) {
        return true;
    }
    if (args.length !== 1 || !isObject(args[0])) {
        return false;
    }
    var componentMap = args[0];
    return Object.keys(componentMap).some(function (key) { return React.isValidElement(componentMap[key]); });
}
/**
 * Parses a template string into groups.
 *
 * The top level group will be keyed as `root`. All other group names will have
 * been extracted from the template string.
 */
export function parseComponentTemplate(template) {
    var parsed = {};
    function process(startPos, group, inGroup) {
        var regex = /\[(.*?)(:|\])|\]/g;
        var buf = [];
        var satisfied = false;
        var match;
        var pos = (regex.lastIndex = startPos);
        // eslint-disable-next-line no-cond-assign
        while ((match = regex.exec(template)) !== null) {
            var substr = template.substr(pos, match.index - pos);
            if (substr !== '') {
                buf.push(substr);
            }
            var _a = __read(match, 3), fullMatch = _a[0], groupName = _a[1], closeBraceOrValueSeparator = _a[2];
            if (fullMatch === ']') {
                if (inGroup) {
                    satisfied = true;
                    break;
                }
                else {
                    pos = regex.lastIndex;
                    continue;
                }
            }
            if (closeBraceOrValueSeparator === ']') {
                pos = regex.lastIndex;
            }
            else {
                pos = regex.lastIndex = process(regex.lastIndex, groupName, true);
            }
            buf.push({ group: groupName });
        }
        var endPos = regex.lastIndex;
        if (!satisfied) {
            var rest = template.substr(pos);
            if (rest) {
                buf.push(rest);
            }
            endPos = template.length;
        }
        parsed[group] = buf;
        return endPos;
    }
    process(0, 'root', false);
    return parsed;
}
/**
 * Renders a parsed template into a React tree given a ComponentMap to use for
 * the parsed groups.
 */
export function renderTemplate(template, components) {
    var idx = 0;
    function renderGroup(groupKey) {
        var e_1, _a;
        var _b;
        var children = [];
        var group = template[groupKey] || [];
        try {
            for (var group_1 = __values(group), group_1_1 = group_1.next(); !group_1_1.done; group_1_1 = group_1.next()) {
                var item = group_1_1.value;
                if (isString(item)) {
                    children.push(<span key={idx++}>{item}</span>);
                }
                else {
                    children.push(renderGroup(item.group));
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (group_1_1 && !group_1_1.done && (_a = group_1.return)) _a.call(group_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        // In case we cannot find our component, we call back to an empty
        // span so that stuff shows up at least.
        var reference = (_b = components[groupKey]) !== null && _b !== void 0 ? _b : <span key={idx++}/>;
        if (!React.isValidElement(reference)) {
            reference = <span key={idx++}>{reference}</span>;
        }
        var element = reference;
        return children.length === 0
            ? React.cloneElement(element, { key: idx++ })
            : React.cloneElement(element, { key: idx++ }, children);
    }
    return <React.Fragment>{renderGroup('root')}</React.Fragment>;
}
/**
 * mark is used to debug translations by visually marking translated strings.
 *
 * NOTE: This is a no-op and will return the node if LOCALE_DEBUG is not
 * currently enabled. See setLocaleDebug and toggleLocaleDebug.
 */
function mark(node) {
    if (!LOCALE_DEBUG) {
        return node;
    }
    // TODO(epurkhiser): Explain why we manually create a react node and assign
    // the toString function. This could likely also use better typing, but will
    // require some understanding of reacts internal types.
    var proxy = {
        $$typeof: Symbol.for('react.element'),
        type: 'span',
        key: null,
        ref: null,
        props: {
            className: markerCss,
            children: isArray(node) ? node : [node],
        },
        _owner: null,
        _store: {},
    };
    proxy.toString = function () { return '✅' + node + '✅'; };
    return proxy;
}
/**
 * sprintf style string formatting. Does not handle translations.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
export function format(formatString, args) {
    if (argsInvolveReact(args)) {
        return formatForReact(formatString, args);
    }
    return sprintf.apply(void 0, __spread([formatString], args));
}
/**
 * Translates a string to the current locale.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
export function gettext(string) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    var val = i18n.gettext(string);
    if (args.length === 0) {
        return mark(val);
    }
    // XXX(ts): It IS possible to use gettext in such a way that it will return a
    // React.ReactNodeArray, however we currently rarely (if at all) use it in
    // this way, and usually just expect strings back.
    return mark(format(val, args));
}
/**
 * Translates a singular and plural string to the current locale. Supports
 * argument parameterization, and will use the first argument as the counter to
 * determine which message to use.
 *
 * See the sprintf-js library [0] for specifics on the argument
 * parameterization format.
 *
 * [0]: https://github.com/alexei/sprintf.js
 */
export function ngettext(singular, plural) {
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    var countArg = 0;
    if (args.length > 0) {
        countArg = args[0] || 0;
        // `toLocaleString` will render `999` as `"999"` but `9999` as `"9,999"`. This means that any call with `tn` or `ngettext` cannot use `%d` in the codebase but has to use `%s`.
        // This means a string is always being passed in as an argument, but `sprintf-js` implicitly coerces strings that can be parsed as integers into an integer.
        // This would break under any locale that used different formatting and other undesirable behaviors.
        if ((singular + plural).includes('%d')) {
            // eslint-disable-next-line no-console
            console.error(new Error('You should not use %d within tn(), use %s instead'));
        }
        else {
            args = __spread([countArg.toLocaleString()], args.slice(1));
        }
    }
    // XXX(ts): See XXX in gettext.
    return mark(format(i18n.ngettext(singular, plural, countArg), args));
}
/**
 * special form of gettext where you can render nested react components in
 * template strings.
 *
 * ```jsx
 * gettextComponentTemplate('Welcome. Click [link:here]', {
 *   root: <p/>,
 *   link: <a href="#" />,
 * });
 * ```
 *
 * The root string is always called "root", the rest is prefixed with the name
 * in the brackets
 *
 * You may recursively nest additional groups within the grouped string values.
 */
export function gettextComponentTemplate(template, components) {
    var tmpl = parseComponentTemplate(i18n.gettext(template));
    return mark(renderTemplate(tmpl, components));
}
/**
 * Shorthand versions should primarily be used.
 */
export { gettext as t, ngettext as tn, gettextComponentTemplate as tct };
var templateObject_1;
//# sourceMappingURL=locale.jsx.map