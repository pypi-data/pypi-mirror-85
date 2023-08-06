/**
 * Parses the "marked" html strings into a {key, value, indices} (similar to
 * Fuse.js) object, where the indices are a set of zero indexed [start, end]
 * indices for what should be highlighted.
 *
 * @param key The key of the field, this mimics the Fuse match object
 * @param htmlString The html string to parse
 * @param markTags.highlightPreTag The left tag
 * @param markTags.highlightPostTag The right tag
 */
export default function parseHtmlMarks(_a) {
    var key = _a.key, htmlString = _a.htmlString, markTags = _a.markTags;
    var highlightPreTag = markTags.highlightPreTag, highlightPostTag = markTags.highlightPostTag;
    var indices = [];
    var value = htmlString;
    // eslint-disable-next-line no-constant-condition
    while (true) {
        var openIndex = value.indexOf(highlightPreTag);
        var openIndexEnd = openIndex + highlightPreTag.length;
        if (openIndex === -1 || value.indexOf(highlightPostTag) === -1) {
            break;
        }
        value = value.slice(0, openIndex) + value.slice(openIndexEnd);
        var closeIndex = value.indexOf(highlightPostTag);
        var closeIndexEnd = closeIndex + highlightPostTag.length;
        value = value.slice(0, closeIndex) + value.slice(closeIndexEnd);
        indices.push([openIndex, closeIndex - 1]);
    }
    return { key: key, value: value, indices: indices };
}
//# sourceMappingURL=parseHtmlMarks.jsx.map