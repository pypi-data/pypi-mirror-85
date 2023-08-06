import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import DocumentTitle from 'react-document-title';
import { getUserTimezone, getUtcToLocalDateObject } from 'app/utils/dates';
import { t } from 'app/locale';
import { updateProjects, updateDateTime } from 'app/actionCreators/globalSelection';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import { getDiscoverLandingUrl } from 'app/utils/discover/urls';
import Redirect from 'app/utils/redirect';
import Discover from './discover';
import createQueryBuilder from './queryBuilder';
import { getQueryFromQueryString, fetchSavedQuery, parseSavedQuery, getView, } from './utils';
import { DiscoverWrapper } from './styles';
var DiscoverContainer = /** @class */ (function (_super) {
    __extends(DiscoverContainer, _super);
    function DiscoverContainer(props) {
        var _this = _super.call(this, props) || this;
        _this.loadTags = function () { return _this.queryBuilder.load(); };
        _this.setLoadedState = function () {
            _this.setState({ isLoading: false });
        };
        _this.fetchSavedQuery = function (savedQueryId) {
            var organization = _this.props.organization;
            return fetchSavedQuery(organization, savedQueryId)
                .then(function (resp) {
                if (_this.queryBuilder) {
                    _this.queryBuilder.reset(parseSavedQuery(resp));
                }
                else {
                    _this.queryBuilder = createQueryBuilder(parseSavedQuery(resp), organization);
                }
                _this.setState({ isLoading: false, savedQuery: resp, view: 'saved' });
            })
                .catch(function () {
                browserHistory.push({
                    pathname: "/organizations/" + organization.slug + "/discover/",
                    query: { view: 'saved' },
                });
                window.location.reload();
            });
        };
        _this.updateSavedQuery = function (savedQuery) {
            _this.setState({ savedQuery: savedQuery });
        };
        _this.toggleEditMode = function () {
            var organization = _this.props.organization;
            var savedQuery = _this.state.savedQuery;
            var isEditingSavedQuery = _this.props.location.query.editing === 'true';
            var newQuery = __assign({}, _this.props.location.query);
            if (!isEditingSavedQuery) {
                newQuery.editing = 'true';
            }
            else {
                delete newQuery.editing;
            }
            browserHistory.push({
                pathname: "/organizations/" + organization.slug + "/discover/saved/" + savedQuery.id + "/",
                query: newQuery,
            });
        };
        _this.renderNoAccess = function () {
            var _a = _this.props, router = _a.router, organization = _a.organization;
            if (organization.features.includes('discover-query') ||
                organization.features.includes('discover-basic')) {
                return <Redirect router={router} to={getDiscoverLandingUrl(organization)}/>;
            }
            else {
                return <Alert type="warning">{t("You don't have access to this feature")}</Alert>;
            }
        };
        _this.state = {
            isLoading: true,
            savedQuery: null,
            view: getView(props.params, props.location.query.view),
        };
        var search = props.location.search;
        var organization = props.organization;
        var query = getQueryFromQueryString(search);
        if (query.hasOwnProperty('projects')) {
            // Update global store with projects from querystring
            updateProjects(query.projects);
        }
        else {
            // Update query with global projects
            query.projects = props.selection.projects;
        }
        if (['range', 'start', 'end'].some(function (key) { return query.hasOwnProperty(key); })) {
            _this.setGlobalSelectionDate(query);
        }
        else {
            // Update query with global datetime values
            query.start = props.selection.datetime.start;
            query.end = props.selection.datetime.end;
            query.range = props.selection.datetime.period;
            query.utc = props.selection.datetime.utc;
        }
        _this.queryBuilder = createQueryBuilder(query, organization);
        return _this;
    }
    DiscoverContainer.getDerivedStateFromProps = function (nextProps, currState) {
        var nextState = __assign({}, currState);
        nextState.view = getView(nextProps.params, nextProps.location.query.view);
        if (!nextProps.params.savedQueryId) {
            nextState.savedQuery = null;
            return nextState;
        }
        return nextState;
    };
    DiscoverContainer.prototype.componentDidMount = function () {
        var _this = this;
        document.body.classList.add('body-discover');
        var savedQueryId = this.props.params.savedQueryId;
        if (savedQueryId) {
            this.loadTags()
                .then(function () { return _this.fetchSavedQuery(savedQueryId); })
                .then(this.setLoadedState);
        }
        else {
            this.loadTags().then(this.setLoadedState);
        }
    };
    DiscoverContainer.prototype.componentDidUpdate = function (prevProps, prevState) {
        var currProps = this.props;
        var currState = this.state;
        // Switching from Saved to New
        if (!currProps.params.savedQueryId && prevProps.params.savedQueryId) {
            var _a = prevProps.selection, datetime = _a.datetime, projects = _a.projects;
            var start = datetime.start, end = datetime.end, range = datetime.period;
            this.queryBuilder.reset({ projects: projects, range: range, start: start, end: end });
            // Reset to default 14d
            this.setGlobalSelectionDate(null);
            return;
        }
        // Switching from a Saved to another Saved
        if (currProps.params.savedQueryId !== prevProps.params.savedQueryId) {
            this.fetchSavedQuery(currProps.params.savedQueryId);
            return;
        }
        // If there are updates within the same SavedQuery
        if (currState.savedQuery !== prevState.savedQuery) {
            this.setGlobalSelectionDate(currState.savedQuery);
        }
    };
    DiscoverContainer.prototype.componentWillUnmount = function () {
        this.queryBuilder.cancelRequests();
        document.body.classList.remove('body-discover');
    };
    DiscoverContainer.prototype.setGlobalSelectionDate = function (query) {
        if (query) {
            var timezone = getUserTimezone();
            // start/end will always be in UTC, however we need to coerce into
            // system time for date picker to be able to synced.
            updateDateTime({
                start: (query.start && getUtcToLocalDateObject(query.start)) || null,
                end: (query.end && getUtcToLocalDateObject(query.end)) || null,
                period: query.range || null,
                utc: query.utc || timezone === 'UTC',
            });
        }
        else {
            updateDateTime({
                start: null,
                end: null,
                period: null,
                utc: true,
            });
        }
    };
    DiscoverContainer.prototype.render = function () {
        var _a = this.state, isLoading = _a.isLoading, savedQuery = _a.savedQuery, view = _a.view;
        var _b = this.props, location = _b.location, organization = _b.organization, params = _b.params, selection = _b.selection;
        return (<DocumentTitle title={"Discover - " + organization.slug + " - Sentry"}>
        <Feature features={['organizations:discover']} hookName="feature-disabled:discover-page" organization={organization} renderDisabled={this.renderNoAccess}>
          <DiscoverWrapper>
            <Discover utc={selection.datetime.utc} isLoading={isLoading} organization={organization} queryBuilder={this.queryBuilder} location={location} params={params} savedQuery={savedQuery} isEditingSavedQuery={this.props.location.query.editing === 'true'} updateSavedQueryData={this.updateSavedQuery} view={view} toggleEditMode={this.toggleEditMode}/>
          </DiscoverWrapper>
        </Feature>
      </DocumentTitle>);
    };
    return DiscoverContainer;
}(React.Component));
export default withGlobalSelection(withOrganization(DiscoverContainer));
export { DiscoverContainer };
//# sourceMappingURL=index.jsx.map