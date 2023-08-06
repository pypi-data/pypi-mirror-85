import { __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import { DEFAULT_QUERY } from 'app/constants';
import { t } from 'app/locale';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LoadingIndicator from 'app/components/loadingIndicator';
import Placeholder from 'app/components/placeholder';
import NoUnresolvedIssues from './noUnresolvedIssues';
/**
 * Component which is rendered when no groups/issues were found. This could
 * either be caused by having no first events, having resolved all issues, or
 * having no issues be returned from a query. This component will conditionally
 * render one of those states.
 */
var NoGroupsHandler = /** @class */ (function (_super) {
    __extends(NoGroupsHandler, _super);
    function NoGroupsHandler() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fetchingSentFirstEvent: true,
            sentFirstEvent: false,
            firstEventProjects: null,
        };
        /**
         * This is a bit hacky, but this is causing flakiness in frontend tests
         * `issueList/overview` is being unmounted during tests before the requests
         * in `this.fetchSentFirstEvent` are completed and causing this React warning:
         *
         * Warning: Can't perform a React state update on an unmounted component.
         * This is a no-op, but it indicates a memory leak in your application.
         * To fix, cancel all subscriptions and asynchronous tasks in the
         * componentWillUnmount method.
         *
         * This is something to revisit if we refactor API client
         */
        _this._isMounted = false;
        return _this;
    }
    NoGroupsHandler.prototype.componentDidMount = function () {
        this.fetchSentFirstEvent();
        this._isMounted = true;
    };
    NoGroupsHandler.prototype.componentWillUnmount = function () {
        this._isMounted = false;
    };
    NoGroupsHandler.prototype.fetchSentFirstEvent = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, organization, selectedProjectIds, api, sentFirstEvent, projects, firstEventQuery, projectsQuery;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        this.setState({
                            fetchingSentFirstEvent: true,
                        });
                        _a = this.props, organization = _a.organization, selectedProjectIds = _a.selectedProjectIds, api = _a.api;
                        sentFirstEvent = false;
                        projects = [];
                        firstEventQuery = {};
                        projectsQuery = { per_page: 1 };
                        if (!selectedProjectIds || !selectedProjectIds.length) {
                            firstEventQuery = { is_member: true };
                        }
                        else {
                            firstEventQuery = { project: selectedProjectIds };
                            projectsQuery.query = selectedProjectIds.map(function (id) { return "id:" + id; }).join(' ');
                        }
                        return [4 /*yield*/, Promise.all([
                                // checks to see if selection has sent a first event
                                api.requestPromise("/organizations/" + organization.slug + "/sent-first-event/", {
                                    query: firstEventQuery,
                                }),
                                // retrieves a single project to feed to the ErrorRobot from renderStreamBody
                                api.requestPromise("/organizations/" + organization.slug + "/projects/", {
                                    query: projectsQuery,
                                }),
                            ])];
                    case 1:
                        _b = __read.apply(void 0, [_c.sent(), 2]), sentFirstEvent = _b[0].sentFirstEvent, projects = _b[1];
                        // See comment where this property is initialized
                        // FIXME
                        if (!this._isMounted) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            fetchingSentFirstEvent: false,
                            sentFirstEvent: sentFirstEvent,
                            firstEventProjects: projects,
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    NoGroupsHandler.prototype.renderLoading = function () {
        return <LoadingIndicator />;
    };
    NoGroupsHandler.prototype.renderAwaitingEvents = function (projects) {
        var _a = this.props, organization = _a.organization, groupIds = _a.groupIds;
        var project = projects && projects.length > 0 ? projects[0] : undefined;
        var sampleIssueId = groupIds.length > 0 ? groupIds[0] : undefined;
        var ErrorRobot = React.lazy(function () { return import(/* webpackChunkName: "ErrorRobot" */ 'app/components/errorRobot'); });
        return (<React.Suspense fallback={<Placeholder height="260px"/>}>
        <ErrorRobot org={organization} project={project} sampleIssueId={sampleIssueId} gradient/>
      </React.Suspense>);
    };
    NoGroupsHandler.prototype.renderEmpty = function () {
        return (<EmptyStateWarning>
        <p>{t('Sorry, no issues match your filters.')}</p>
      </EmptyStateWarning>);
    };
    NoGroupsHandler.prototype.render = function () {
        var _a = this.state, fetchingSentFirstEvent = _a.fetchingSentFirstEvent, sentFirstEvent = _a.sentFirstEvent, firstEventProjects = _a.firstEventProjects;
        var query = this.props.query;
        if (fetchingSentFirstEvent) {
            return this.renderLoading();
        }
        if (!sentFirstEvent) {
            return this.renderAwaitingEvents(firstEventProjects);
        }
        if (query === DEFAULT_QUERY) {
            return <NoUnresolvedIssues />;
        }
        return this.renderEmpty();
    };
    return NoGroupsHandler;
}(React.Component));
export default NoGroupsHandler;
//# sourceMappingURL=index.jsx.map