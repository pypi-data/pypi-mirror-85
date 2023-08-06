import { __assign, __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import classNames from 'classnames';
import moment from 'moment';
import styled from '@emotion/styled';
import { IconEllipsis } from 'app/icons';
import { resetGlobalSelection } from 'app/actionCreators/globalSelection';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import DropdownMenu from 'app/components/dropdownMenu';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import EventView from 'app/utils/discover/eventView';
import MenuItem from 'app/components/menuItem';
import Pagination from 'app/components/pagination';
import TimeSince from 'app/components/timeSince';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import { getPrebuiltQueries } from './utils';
import { handleDeleteQuery, handleCreateQuery } from './savedQuery/utils';
import MiniGraph from './miniGraph';
import QueryCard from './querycard';
var QueryList = /** @class */ (function (_super) {
    __extends(QueryList, _super);
    function QueryList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteQuery = function (eventView) { return function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, onQueryChange = _a.onQueryChange, location = _a.location, savedQueries = _a.savedQueries;
            handleDeleteQuery(api, organization, eventView).then(function () {
                if (savedQueries.length === 1 && location.query.cursor) {
                    browserHistory.push({
                        pathname: location.pathname,
                        query: __assign(__assign({}, location.query), { cursor: undefined }),
                    });
                }
                else {
                    onQueryChange();
                }
            });
        }; };
        _this.handleDuplicateQuery = function (eventView) { return function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, location = _a.location, organization = _a.organization, onQueryChange = _a.onQueryChange;
            eventView = eventView.clone();
            eventView.name = eventView.name + " copy";
            handleCreateQuery(api, organization, eventView).then(function () {
                onQueryChange();
                browserHistory.push({
                    pathname: location.pathname,
                    query: {},
                });
            });
        }; };
        return _this;
    }
    QueryList.prototype.componentDidMount = function () {
        /**
         * We need to reset global selection here because the saved queries can define their own projects
         * in the query. This can lead to mismatched queries for the project
         */
        resetGlobalSelection();
    };
    QueryList.prototype.renderQueries = function () {
        var _a = this.props, pageLinks = _a.pageLinks, renderPrebuilt = _a.renderPrebuilt;
        var links = parseLinkHeader(pageLinks || '');
        var cards = [];
        // If we're on the first page (no-previous page exists)
        // include the pre-built queries.
        if (renderPrebuilt && (!links.previous || links.previous.results === false)) {
            cards = cards.concat(this.renderPrebuiltQueries());
        }
        cards = cards.concat(this.renderSavedQueries());
        if (cards.filter(function (x) { return x; }).length === 0) {
            return (<StyledEmptyStateWarning>
          <p>{t('No saved queries match that filter')}</p>
        </StyledEmptyStateWarning>);
        }
        return cards;
    };
    QueryList.prototype.renderPrebuiltQueries = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, savedQuerySearchQuery = _a.savedQuerySearchQuery;
        var views = getPrebuiltQueries(organization);
        var hasSearchQuery = typeof savedQuerySearchQuery === 'string' && savedQuerySearchQuery.length > 0;
        var needleSearch = hasSearchQuery ? savedQuerySearchQuery.toLowerCase() : '';
        var list = views.map(function (view, index) {
            var eventView = EventView.fromNewQueryWithLocation(view, location);
            // if a search is performed on the list of queries, we filter
            // on the pre-built queries
            if (hasSearchQuery &&
                eventView.name &&
                !eventView.name.toLowerCase().includes(needleSearch)) {
                return null;
            }
            var recentTimeline = t('Last ') + eventView.statsPeriod;
            var customTimeline = moment(eventView.start).format('MMM D, YYYY h:mm A') +
                ' - ' +
                moment(eventView.end).format('MMM D, YYYY h:mm A');
            var to = eventView.getResultsViewUrlTarget(organization.slug);
            return (<QueryCard key={index + "-" + eventView.name} to={to} title={eventView.name} subtitle={eventView.statsPeriod ? recentTimeline : customTimeline} queryDetail={eventView.query} createdBy={eventView.createdBy} renderGraph={function () { return (<MiniGraph location={location} eventView={eventView} organization={organization}/>); }} onEventClick={function () {
                trackAnalyticsEvent({
                    eventKey: 'discover_v2.prebuilt_query_click',
                    eventName: 'Discoverv2: Click a pre-built query',
                    organization_id: parseInt(_this.props.organization.id, 10),
                    query_name: eventView.name,
                });
            }}/>);
        });
        return list;
    };
    QueryList.prototype.renderSavedQueries = function () {
        var _this = this;
        var _a = this.props, savedQueries = _a.savedQueries, location = _a.location, organization = _a.organization;
        if (!savedQueries || !Array.isArray(savedQueries) || savedQueries.length === 0) {
            return [];
        }
        return savedQueries.map(function (savedQuery, index) {
            var eventView = EventView.fromSavedQuery(savedQuery);
            var recentTimeline = t('Last ') + eventView.statsPeriod;
            var customTimeline = moment(eventView.start).format('MMM D, YYYY h:mm A') +
                ' - ' +
                moment(eventView.end).format('MMM D, YYYY h:mm A');
            var to = eventView.getResultsViewUrlTarget(organization.slug);
            var dateStatus = <TimeSince date={savedQuery.dateUpdated}/>;
            return (<QueryCard key={index + "-" + eventView.id} to={to} title={eventView.name} subtitle={eventView.statsPeriod ? recentTimeline : customTimeline} queryDetail={eventView.query} createdBy={eventView.createdBy} dateStatus={dateStatus} onEventClick={function () {
                trackAnalyticsEvent({
                    eventKey: 'discover_v2.saved_query_click',
                    eventName: 'Discoverv2: Click a saved query',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
            }} renderGraph={function () { return (<MiniGraph location={location} eventView={eventView} organization={organization}/>); }} renderContextMenu={function () { return (<ContextMenu>
              <MenuItem data-test-id="delete-query" onClick={_this.handleDeleteQuery(eventView)}>
                {t('Delete Query')}
              </MenuItem>
              <MenuItem data-test-id="duplicate-query" onClick={_this.handleDuplicateQuery(eventView)}>
                {t('Duplicate Query')}
              </MenuItem>
            </ContextMenu>); }}/>);
        });
    };
    QueryList.prototype.render = function () {
        var pageLinks = this.props.pageLinks;
        return (<React.Fragment>
        <QueryGrid>{this.renderQueries()}</QueryGrid>
        <PaginationRow pageLinks={pageLinks} onCursor={function (cursor, path, query, direction) {
            var offset = Number(cursor.split(':')[1]);
            var newQuery = __assign(__assign({}, query), { cursor: cursor });
            var isPrevious = direction === -1;
            if (offset <= 0 && isPrevious) {
                delete newQuery.cursor;
            }
            browserHistory.push({
                pathname: path,
                query: newQuery,
            });
        }}/>
      </React.Fragment>);
    };
    return QueryList;
}(React.Component));
var PaginationRow = styled(Pagination)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var QueryGrid = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var ContextMenu = function (_a) {
    var children = _a.children;
    return (<DropdownMenu>
    {function (_a) {
        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
        var topLevelCx = classNames('dropdown', {
            'anchor-right': true,
            open: isOpen,
        });
        return (<MoreOptions {...getRootProps({
            className: topLevelCx,
        })}>
          <DropdownTarget {...getActorProps({
            onClick: function (event) {
                event.stopPropagation();
                event.preventDefault();
            },
        })}>
            <IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={classNames('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
    }}
  </DropdownMenu>);
};
var MoreOptions = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  color: ", ";\n"], ["\n  display: flex;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var DropdownTarget = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledEmptyStateWarning = styled(EmptyStateWarning)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-column: 1 / 4;\n"], ["\n  grid-column: 1 / 4;\n"])));
export default withApi(QueryList);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=queryList.jsx.map