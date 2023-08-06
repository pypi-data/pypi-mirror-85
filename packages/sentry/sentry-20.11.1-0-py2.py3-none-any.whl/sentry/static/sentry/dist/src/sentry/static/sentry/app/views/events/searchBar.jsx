import { __extends, __makeTemplateObject } from "tslib";
import { ClassNames } from '@emotion/core';
import assign from 'lodash/assign';
import flatten from 'lodash/flatten';
import isEqual from 'lodash/isEqual';
import memoize from 'lodash/memoize';
import omit from 'lodash/omit';
import PropTypes from 'prop-types';
import React from 'react';
import { NEGATION_OPERATOR, SEARCH_WILDCARD } from 'app/constants';
import { defined } from 'app/utils';
import { fetchTagValues } from 'app/actionCreators/tags';
import SentryTypes from 'app/sentryTypes';
import { SavedSearchType } from 'app/types';
import SmartSearchBar from 'app/components/smartSearchBar';
import { FIELD_TAGS, TRACING_FIELDS, isAggregateField, isMeasurement, } from 'app/utils/discover/fields';
import withApi from 'app/utils/withApi';
import withTags from 'app/utils/withTags';
import Measurements from 'app/utils/measurements/measurements';
var SEARCH_SPECIAL_CHARS_REGEXP = new RegExp("^" + NEGATION_OPERATOR + "|\\" + SEARCH_WILDCARD, 'g');
var SearchBar = /** @class */ (function (_super) {
    __extends(SearchBar, _super);
    function SearchBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with data when ready
         */
        _this.getEventFieldValues = memoize(function (tag, query, endpointParams) {
            var _a;
            var _b = _this.props, api = _b.api, organization = _b.organization, projectIds = _b.projectIds;
            var projectIdStrings = (_a = projectIds) === null || _a === void 0 ? void 0 : _a.map(String);
            if (isAggregateField(tag.key) || isMeasurement(tag.key)) {
                // We can't really auto suggest values for aggregate fields
                // or measurements, so we simply don't
                return Promise.resolve([]);
            }
            return fetchTagValues(api, organization.slug, tag.key, query, projectIdStrings, endpointParams, 
            // allows searching for tags on transactions as well
            true).then(function (results) {
                return flatten(results.filter(function (_a) {
                    var name = _a.name;
                    return defined(name);
                }).map(function (_a) {
                    var name = _a.name;
                    return name;
                }));
            }, function () {
                throw new Error('Unable to fetch event field values');
            });
        }, function (_a, query) {
            var key = _a.key;
            return key + "-" + query;
        });
        /**
         * Prepare query string (e.g. strip special characters like negation operator)
         */
        _this.prepareQuery = function (query) { return query.replace(SEARCH_SPECIAL_CHARS_REGEXP, ''); };
        return _this;
    }
    SearchBar.prototype.componentDidMount = function () {
        var _a, _b;
        // Clear memoized data on mount to make tests more consistent.
        (_b = (_a = this.getEventFieldValues.cache).clear) === null || _b === void 0 ? void 0 : _b.call(_a);
    };
    SearchBar.prototype.componentDidUpdate = function (prevProps) {
        var _a, _b;
        if (!isEqual(this.props.projectIds, prevProps.projectIds)) {
            // Clear memoized data when projects change.
            (_b = (_a = this.getEventFieldValues.cache).clear) === null || _b === void 0 ? void 0 : _b.call(_a);
        }
    };
    SearchBar.prototype.getTagList = function (measurements) {
        var _a = this.props, fields = _a.fields, organization = _a.organization, tags = _a.tags, omitTags = _a.omitTags;
        var functionTags = fields
            ? Object.fromEntries(fields
                .filter(function (item) { return !Object.keys(FIELD_TAGS).includes(item.field); })
                .map(function (item) { return [item.field, { key: item.field, name: item.field }]; }))
            : {};
        var fieldTags = organization.features.includes('performance-view')
            ? Object.assign({}, measurements, FIELD_TAGS, functionTags)
            : omit(FIELD_TAGS, TRACING_FIELDS);
        var combined = assign({}, tags, fieldTags);
        combined.has = {
            key: 'has',
            name: 'Has property',
            values: Object.keys(combined),
            predefined: true,
        };
        return omit(combined, omitTags !== null && omitTags !== void 0 ? omitTags : []);
    };
    SearchBar.prototype.render = function () {
        var _this = this;
        return (<Measurements>
        {function (_a) {
            var measurements = _a.measurements;
            var tags = _this.getTagList(measurements);
            return (<ClassNames>
              {function (_a) {
                var css = _a.css;
                return (<SmartSearchBar {..._this.props} hasRecentSearches savedSearchType={SavedSearchType.EVENT} onGetTagValues={_this.getEventFieldValues} supportedTags={tags} prepareQuery={_this.prepareQuery} excludeEnvironment dropdownClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                    max-height: 300px;\n                    overflow-y: auto;\n                  "], ["\n                    max-height: 300px;\n                    overflow-y: auto;\n                  "])))}/>);
            }}
            </ClassNames>);
        }}
      </Measurements>);
    };
    SearchBar.propTypes = {
        api: PropTypes.object,
        organization: SentryTypes.Organization,
        tags: PropTypes.objectOf(SentryTypes.Tag),
        omitTags: PropTypes.arrayOf(PropTypes.string.isRequired),
        projectIds: PropTypes.arrayOf(PropTypes.number.isRequired),
        fields: PropTypes.arrayOf(PropTypes.object.isRequired),
    };
    return SearchBar;
}(React.PureComponent));
export default withApi(withTags(SearchBar));
var templateObject_1;
//# sourceMappingURL=searchBar.jsx.map