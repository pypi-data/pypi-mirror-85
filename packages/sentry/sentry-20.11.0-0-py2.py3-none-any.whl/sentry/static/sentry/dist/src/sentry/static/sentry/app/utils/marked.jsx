import { __assign, __extends, __read, __spread } from "tslib";
import marked from 'marked'; // eslint-disable-line no-restricted-imports
import dompurify from 'dompurify';
import { IS_ACCEPTANCE_TEST, NODE_ENV } from 'app/constants';
// Only https and mailto, (e.g. no javascript, vbscript, data protocols)
var safeLinkPattern = /^(https?:|mailto:)/i;
var safeImagePattern = /^https?:\/\/./i;
function isSafeHref(href, pattern) {
    try {
        return pattern.test(decodeURIComponent(unescape(href)));
    }
    catch (_a) {
        return false;
    }
}
/**
 * Implementation of marked.Renderer which additonally sanitizes URLs.
 */
var SafeRenderer = /** @class */ (function (_super) {
    __extends(SafeRenderer, _super);
    function SafeRenderer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SafeRenderer.prototype.link = function (href, title, text) {
        // For a bad link, just return the plain text href
        if (!isSafeHref(href, safeLinkPattern)) {
            return href;
        }
        var out = "<a href=\"" + href + "\"" + (title ? " title=\"" + title + "\"" : '') + ">" + text + "</a>";
        return dompurify.sanitize(out);
    };
    SafeRenderer.prototype.image = function (href, title, text) {
        // For a bad image, return an empty string
        if (this.options.sanitize && !isSafeHref(href, safeImagePattern)) {
            return '';
        }
        return "<img src=\"" + href + "\" alt=\"" + text + "\"" + (title ? " title=\"" + title + "\"" : '') + " />";
    };
    return SafeRenderer;
}(marked.Renderer));
var NoParagraphRenderer = /** @class */ (function (_super) {
    __extends(NoParagraphRenderer, _super);
    function NoParagraphRenderer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NoParagraphRenderer.prototype.paragraph = function (text) {
        return text;
    };
    return NoParagraphRenderer;
}(SafeRenderer));
marked.setOptions({
    renderer: new SafeRenderer(),
    sanitize: true,
    // Silence sanitize deprecation warning in test / ci (CI sets NODE_NV
    // to production, but specifies `CI`).
    //
    // [!!] This has the side effect of causing failed markdown content to render
    //      as a html error, instead of throwing an exception, however none of
    //      our tests are rendering failed markdown so this is likely a safe
    //      tradeoff to turn off off the deprecation warning.
    silent: !!IS_ACCEPTANCE_TEST || NODE_ENV === 'test',
});
var sanitizedMarked = function () {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
    }
    return dompurify.sanitize(marked.apply(void 0, __spread(args)));
};
var singleLineRenderer = function (text, options) {
    if (options === void 0) { options = {}; }
    return sanitizedMarked(text, __assign(__assign({}, options), { renderer: new NoParagraphRenderer() }));
};
export { singleLineRenderer };
export default sanitizedMarked;
//# sourceMappingURL=marked.jsx.map