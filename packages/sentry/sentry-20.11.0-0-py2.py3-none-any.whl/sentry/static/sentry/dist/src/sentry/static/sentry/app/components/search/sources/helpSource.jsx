import { __assign, __awaiter, __extends, __generator, __read, __spread } from "tslib";
import React from 'react';
import debounce from 'lodash/debounce';
import dompurify from 'dompurify';
import { withRouter } from 'react-router';
import { SentryGlobalSearch, standardSDKSlug, } from '@sentry-internal/global-search';
import withLatestContext from 'app/utils/withLatestContext';
import parseHtmlMarks from 'app/utils/parseHtmlMarks';
var MARK_TAGS = {
    highlightPreTag: '<mark>',
    highlightPostTag: '</mark>',
};
var HelpSource = /** @class */ (function (_super) {
    __extends(HelpSource, _super);
    function HelpSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            results: [],
        };
        _this.search = new SentryGlobalSearch(['docs', 'help-center', 'develop', 'blog']);
        _this.doSearch = debounce(_this.unbouncedSearch, 300);
        return _this;
    }
    HelpSource.prototype.componentDidMount = function () {
        if (this.props.query !== undefined) {
            this.doSearch(this.props.query);
        }
    };
    HelpSource.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.query !== this.props.query) {
            this.doSearch(nextProps.query);
        }
    };
    HelpSource.prototype.unbouncedSearch = function (query) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, platforms, searchResults, results;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({ loading: true });
                        _a = this.props.platforms, platforms = _a === void 0 ? [] : _a;
                        return [4 /*yield*/, this.search.query(query, {
                                platforms: platforms.map(function (platform) { var _a; return (_a = standardSDKSlug(platform)) === null || _a === void 0 ? void 0 : _a.slug; }),
                            })];
                    case 1:
                        searchResults = _b.sent();
                        results = mapSearchResults(searchResults);
                        this.setState({ loading: false, results: results });
                        return [2 /*return*/];
                }
            });
        });
    };
    HelpSource.prototype.render = function () {
        return this.props.children({
            isLoading: this.state.loading,
            allResults: this.state.results,
            results: this.state.results,
        });
    };
    return HelpSource;
}(React.Component));
function mapSearchResults(results) {
    var items = [];
    results.forEach(function (section) {
        var sectionItems = section.hits.map(function (hit) {
            var _a, _b, _c;
            var title = parseHtmlMarks({
                key: 'title',
                htmlString: (_a = hit.title) !== null && _a !== void 0 ? _a : '',
                markTags: MARK_TAGS,
            });
            var description = parseHtmlMarks({
                key: 'description',
                htmlString: (_b = hit.text) !== null && _b !== void 0 ? _b : '',
                markTags: MARK_TAGS,
            });
            var item = __assign(__assign({}, hit), { sourceType: 'help', resultType: "help-" + hit.site, title: dompurify.sanitize((_c = hit.title) !== null && _c !== void 0 ? _c : ''), extra: hit.context.context1, description: hit.text ? dompurify.sanitize(hit.text) : undefined, to: hit.url });
            return { item: item, matches: [title, description] };
        });
        // The first element should indicate the section.
        if (sectionItems.length > 0) {
            sectionItems[0].item.sectionHeading = section.name;
            sectionItems[0].item.sectionCount = sectionItems.length;
            items.push.apply(items, __spread(sectionItems));
            return;
        }
        // If we didn't have any results for this section mark it as empty
        var emptyHeaderItem = {
            sourceType: 'help',
            resultType: "help-" + section.site,
            title: "No results in " + section.name,
            sectionHeading: section.name,
            empty: true,
        };
        items.push({ item: emptyHeaderItem });
    });
    return items;
}
export { HelpSource };
export default withLatestContext(withRouter(HelpSource));
//# sourceMappingURL=helpSource.jsx.map