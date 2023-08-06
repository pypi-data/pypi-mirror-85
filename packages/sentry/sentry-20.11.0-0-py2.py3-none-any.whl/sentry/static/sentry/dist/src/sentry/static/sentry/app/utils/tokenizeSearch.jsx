import { __assign, __read, __spread, __values } from "tslib";
import { escapeDoubleQuotes } from 'app/utils';
export var TokenType;
(function (TokenType) {
    TokenType[TokenType["OP"] = 0] = "OP";
    TokenType[TokenType["TAG"] = 1] = "TAG";
    TokenType[TokenType["QUERY"] = 2] = "QUERY";
})(TokenType || (TokenType = {}));
function isOp(t) {
    return t.type === TokenType.OP;
}
var QueryResults = /** @class */ (function () {
    function QueryResults(strTokens) {
        var e_1, _a;
        var _this = this;
        this.tokens = [];
        this.tagValues = {};
        try {
            for (var strTokens_1 = __values(strTokens), strTokens_1_1 = strTokens_1.next(); !strTokens_1_1.done; strTokens_1_1 = strTokens_1.next()) {
                var token = strTokens_1_1.value;
                var tokenState = TokenType.QUERY;
                if (['OR', 'AND'].includes(token.toUpperCase())) {
                    this.addOp(token.toUpperCase());
                    continue;
                }
                if (token.startsWith('(')) {
                    var parenMatch = token.match(/^\(+/g);
                    if (parenMatch) {
                        parenMatch[0].split('').map(function (paren) { return _this.addOp(paren); });
                        token = token.replace(/^\(+/g, '');
                    }
                }
                // Traverse the token and determine if it is a tag
                // condition or bare words.
                for (var i = 0, len = token.length; i < len; i++) {
                    var char = token[i];
                    if (i === 0 && (char === '"' || char === ':')) {
                        break;
                    }
                    // We may have entered a tag condition
                    if (char === ':') {
                        var nextChar = token[i + 1] || '';
                        if ([':', ' '].includes(nextChar)) {
                            tokenState = TokenType.QUERY;
                        }
                        else {
                            tokenState = TokenType.TAG;
                        }
                        break;
                    }
                }
                var trailingParen = '';
                if (token.endsWith(')') && !token.includes('(')) {
                    var parenMatch = token.match(/\)+$/g);
                    if (parenMatch) {
                        trailingParen = parenMatch[0];
                        token = token.replace(/\)+$/g, '');
                    }
                }
                if (tokenState === TokenType.QUERY && token.length) {
                    this.addQuery(token);
                }
                else if (tokenState === TokenType.TAG) {
                    this.addStringTag(token);
                }
                if (trailingParen !== '') {
                    trailingParen.split('').map(function (paren) { return _this.addOp(paren); });
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (strTokens_1_1 && !strTokens_1_1.done && (_a = strTokens_1.return)) _a.call(strTokens_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    QueryResults.prototype.formatString = function () {
        var e_2, _a;
        var formattedTokens = [];
        try {
            for (var _b = __values(this.tokens), _c = _b.next(); !_c.done; _c = _b.next()) {
                var token = _c.value;
                switch (token.type) {
                    case TokenType.TAG:
                        if (token.value === '' || token.value === null) {
                            formattedTokens.push(token.key + ":\"\"");
                        }
                        else if (/[\s\(\)\\"]/g.test(token.value)) {
                            formattedTokens.push(token.key + ":\"" + escapeDoubleQuotes(token.value) + "\"");
                        }
                        else {
                            formattedTokens.push(token.key + ":" + token.value);
                        }
                        break;
                    default:
                        formattedTokens.push(token.value);
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return formattedTokens.join(' ').trim();
    };
    QueryResults.prototype.addStringTag = function (value) {
        var _a = __read(formatTag(value), 2), key = _a[0], tag = _a[1];
        this.addTagValues(key, [tag]);
        return this;
    };
    QueryResults.prototype.addTagValues = function (tag, tagValues) {
        var e_3, _a;
        try {
            for (var tagValues_1 = __values(tagValues), tagValues_1_1 = tagValues_1.next(); !tagValues_1_1.done; tagValues_1_1 = tagValues_1.next()) {
                var t = tagValues_1_1.value;
                this.tagValues[tag] = Array.isArray(this.tagValues[tag])
                    ? __spread(this.tagValues[tag], [t]) : [t];
                var token = { type: TokenType.TAG, key: tag, value: t };
                this.tokens.push(token);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (tagValues_1_1 && !tagValues_1_1.done && (_a = tagValues_1.return)) _a.call(tagValues_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return this;
    };
    QueryResults.prototype.setTagValues = function (tag, tagValues) {
        this.removeTag(tag);
        this.addTagValues(tag, tagValues);
        return this;
    };
    QueryResults.prototype.getTagValues = function (tag) {
        return this.tagValues[tag];
    };
    QueryResults.prototype.hasTag = function (tag) {
        var tags = this.getTagValues(tag);
        return tags && tags.length;
    };
    QueryResults.prototype.removeTag = function (key) {
        this.tokens = this.tokens.filter(function (token) { return token.key !== key; });
        delete this.tagValues[key];
        // Now the really complicated part: removing parens that only have one element in them.
        // Since parens are themselves tokens, this gets tricky. In summary, loop through the
        // tokens until we find the innermost open paren. Then forward search through the rest of the tokens
        // to see if that open paren corresponds to a closed paren with one or fewer items inside.
        // If it does, delete those parens, and loop again until there are no more parens to delete.
        var parensToDelete = [];
        var cleanParens = function (_, idx) { return !parensToDelete.includes(idx); };
        do {
            if (parensToDelete.length) {
                this.tokens = this.tokens.filter(cleanParens);
            }
            parensToDelete = [];
            for (var i = 0; i < this.tokens.length; i++) {
                var token = this.tokens[i];
                if (!isOp(token) || token.value !== '(') {
                    continue;
                }
                var alreadySeen = false;
                for (var j = i + 1; j < this.tokens.length; j++) {
                    var nextToken = this.tokens[j];
                    if (isOp(nextToken) && nextToken.value === '(') {
                        // Continue down to the nested parens. We can skip i forward since we know
                        // everything between i and j is NOT an open paren.
                        i = j - 1;
                        break;
                    }
                    else if (!isOp(nextToken)) {
                        if (alreadySeen) {
                            // This has more than one term, no need to delete
                            break;
                        }
                        alreadySeen = true;
                    }
                    else if (isOp(nextToken) && nextToken.value === ')') {
                        // We found another paren with zero or one terms inside. Delete the pair.
                        parensToDelete = [i, j];
                        break;
                    }
                }
                if (parensToDelete.length > 0) {
                    break;
                }
            }
        } while (parensToDelete.length > 0);
        // Now that all erroneous parens are removed we need to remove dangling OR/AND operators.
        // I originally removed all the dangling properties in a single loop, but that meant that
        // cases like `a OR OR b` would remove both operators, when only one should be removed. So
        // instead, we loop until we find an operator to remove, then go back to the start and loop
        // again.
        var toRemove = -1;
        do {
            if (toRemove >= 0) {
                this.tokens.splice(toRemove, 1);
                toRemove = -1;
            }
            for (var i = 0; i < this.tokens.length; i++) {
                var token = this.tokens[i];
                var prev = this.tokens[i - 1];
                var next = this.tokens[i + 1];
                if (isOp(token) && ['OR', 'AND'].includes(token.value)) {
                    if (prev === undefined || isOp(prev) || next === undefined || isOp(next)) {
                        toRemove = i;
                        break;
                    }
                }
            }
        } while (toRemove >= 0);
        return this;
    };
    QueryResults.prototype.removeTagValue = function (key, value) {
        var values = this.getTagValues(key);
        if (Array.isArray(values) && values.length) {
            this.setTagValues(key, values.filter(function (item) { return item !== value; }));
        }
    };
    QueryResults.prototype.addQuery = function (value) {
        var token = { type: TokenType.QUERY, value: formatQuery(value) };
        this.tokens.push(token);
        return this;
    };
    QueryResults.prototype.addOp = function (value) {
        var token = { type: TokenType.OP, value: value };
        this.tokens.push(token);
        return this;
    };
    Object.defineProperty(QueryResults.prototype, "query", {
        get: function () {
            return this.tokens.filter(function (t) { return t.type === TokenType.QUERY; }).map(function (t) { return t.value; });
        },
        set: function (values) {
            var e_4, _a;
            this.tokens = this.tokens.filter(function (t) { return t.type !== TokenType.QUERY; });
            try {
                for (var values_1 = __values(values), values_1_1 = values_1.next(); !values_1_1.done; values_1_1 = values_1.next()) {
                    var v = values_1_1.value;
                    this.addQuery(v);
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (values_1_1 && !values_1_1.done && (_a = values_1.return)) _a.call(values_1);
                }
                finally { if (e_4) throw e_4.error; }
            }
        },
        enumerable: false,
        configurable: true
    });
    QueryResults.prototype.copy = function () {
        var q = new QueryResults([]);
        q.tagValues = __assign({}, this.tagValues);
        q.tokens = __spread(this.tokens);
        return q;
    };
    return QueryResults;
}());
export { QueryResults };
/**
 * Tokenize a search into a QueryResult
 *
 *
 * Should stay in sync with src.sentry.search.utils:tokenize_query
 */
export function tokenizeSearch(query) {
    var tokens = splitSearchIntoTokens(query);
    return new QueryResults(tokens);
}
/**
 * Convert a QueryResults object back to a query string
 */
export function stringifyQueryObject(results) {
    return results.formatString();
}
/**
 * Splits search strings into tokens for parsing by tokenizeSearch.
 */
function splitSearchIntoTokens(query) {
    var queryChars = Array.from(query);
    var tokens = [];
    var token = '';
    var endOfPrevWord = '';
    var quoteType = '';
    var quoteEnclosed = false;
    queryChars.forEach(function (char, idx) {
        var nextChar = queryChars.length - 1 > idx ? queryChars[idx + 1] : null;
        token += char;
        if (nextChar !== null && !isSpace(char) && isSpace(nextChar)) {
            endOfPrevWord = char;
        }
        if (isSpace(char) && !quoteEnclosed && endOfPrevWord !== ':' && !isSpace(token)) {
            tokens.push(token.trim());
            token = '';
        }
        if (["'", '"'].includes(char) && (!quoteEnclosed || quoteType === char)) {
            quoteEnclosed = !quoteEnclosed;
            if (quoteEnclosed) {
                quoteType = char;
            }
        }
    });
    var trimmedToken = token.trim();
    if (trimmedToken !== '') {
        tokens.push(trimmedToken);
    }
    return tokens;
}
/**
 * Checks if the string is only spaces
 */
function isSpace(s) {
    return s.trim() === '';
}
/**
 * Splits tags on ':' and removes enclosing quotes if present, and returns both
 * sides of the split as strings.
 */
function formatTag(tag) {
    var idx = tag.indexOf(':');
    var key = tag.slice(0, idx).replace(/^"+|"+$/g, '');
    var value = tag.slice(idx + 1).replace(/^"+|"+$/g, '');
    return [key, value];
}
/**
 * Strips enclosing quotes and parens from a query, if present.
 */
function formatQuery(query) {
    return query.replace(/^["\(]+|["\)]+$/g, '');
}
//# sourceMappingURL=tokenizeSearch.jsx.map