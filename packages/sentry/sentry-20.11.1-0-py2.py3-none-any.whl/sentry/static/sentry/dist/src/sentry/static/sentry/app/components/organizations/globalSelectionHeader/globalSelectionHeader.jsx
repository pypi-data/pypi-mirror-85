import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import debounce from 'lodash/debounce';
import styled from '@emotion/styled';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { PageContent } from 'app/styles/organization';
import { callIfFunction } from 'app/utils/callIfFunction';
import { t } from 'app/locale';
import { updateDateTime, updateEnvironments, updateProjects, } from 'app/actionCreators/globalSelection';
import BackToIssues from 'app/components/organizations/backToIssues';
import HeaderItemPosition from 'app/components/organizations/headerItemPosition';
import HeaderSeparator from 'app/components/organizations/headerSeparator';
import { IconArrow } from 'app/icons';
import MultipleEnvironmentSelector from 'app/components/organizations/multipleEnvironmentSelector';
import MultipleProjectSelector from 'app/components/organizations/multipleProjectSelector';
import Projects from 'app/utils/projects';
import SentryTypes from 'app/sentryTypes';
import TimeRangeSelector from 'app/components/organizations/timeRangeSelector';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import Header from './header';
var PROJECTS_PER_PAGE = 50;
var defaultProps = {
    /**
     * Disable automatic routing
     */
    hasCustomRouting: false,
    /**
     * Display Environment selector?
     */
    showEnvironmentSelector: true,
    /**
     * Display date selector?
     */
    showDateSelector: true,
    /**
     * Reset these URL params when we fire actions
     * (custom routing only)
     */
    resetParamsOnChange: [],
    /**
     * Remove ability to select multiple projects even if organization has feature 'global-views'
     */
    disableMultipleProjectSelection: false,
};
var GlobalSelectionHeader = /** @class */ (function (_super) {
    __extends(GlobalSelectionHeader, _super);
    function GlobalSelectionHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            projects: null,
            environments: null,
            searchQuery: '',
        };
        _this.hasMultipleProjectSelection = function () {
            return new Set(_this.props.organization.features).has('global-views');
        };
        // Returns `router` from props if `hasCustomRouting` property is false
        _this.getRouter = function () { return (!_this.props.hasCustomRouting ? _this.props.router : null); };
        // Returns an options object for `update*` actions
        _this.getUpdateOptions = function () {
            return !_this.props.hasCustomRouting
                ? {
                    save: true,
                    resetParams: _this.props.resetParamsOnChange,
                }
                : {};
        };
        _this.handleChangeProjects = function (projects) {
            _this.setState({
                projects: projects,
            });
            callIfFunction(_this.props.onChangeProjects, projects);
        };
        _this.handleChangeEnvironments = function (environments) {
            _this.setState({
                environments: environments,
            });
            callIfFunction(_this.props.onChangeEnvironments, environments);
        };
        _this.handleChangeTime = function (_a) {
            var start = _a.start, end = _a.end, period = _a.relative, utc = _a.utc;
            callIfFunction(_this.props.onChangeTime, { start: start, end: end, period: period, utc: utc });
        };
        _this.handleUpdateTime = function (_a) {
            var _b = _a === void 0 ? {} : _a, period = _b.relative, start = _b.start, end = _b.end, utc = _b.utc;
            var newValueObj = {
                period: period,
                start: start,
                end: end,
                utc: utc,
            };
            updateDateTime(newValueObj, _this.getRouter(), _this.getUpdateOptions());
            callIfFunction(_this.props.onUpdateTime, newValueObj);
        };
        _this.handleUpdateEnvironmments = function () {
            var environments = _this.state.environments;
            updateEnvironments(environments, _this.getRouter(), _this.getUpdateOptions());
            _this.setState({ environments: null });
            callIfFunction(_this.props.onUpdateEnvironments, environments);
        };
        _this.handleUpdateProjects = function () {
            var projects = _this.state.projects;
            // Clear environments when switching projects
            updateProjects(projects || [], _this.getRouter(), __assign(__assign({}, _this.getUpdateOptions()), { environments: [] }));
            _this.setState({ projects: null, environments: null });
            callIfFunction(_this.props.onUpdateProjects, projects);
        };
        _this.getBackButton = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location;
            return (<BackButtonWrapper>
        <Tooltip title={t('Back to Issues Stream')} position="bottom">
          <BackToIssues data-test-id="back-to-issues" to={"/organizations/" + organization.slug + "/issues/" + location.search}>
            <IconArrow direction="left" size="sm"/>
          </BackToIssues>
        </Tooltip>
      </BackButtonWrapper>);
        };
        _this.scrollFetchDispatcher = debounce(function (onSearch, options) {
            onSearch(_this.state.searchQuery, options);
        }, 200, { leading: true, trailing: false });
        _this.searchDispatcher = debounce(function (onSearch, searchQuery, options) {
            // in the case that a user repeats a search query (because search is
            // debounced this is possible if the user types and then deletes what they
            // typed) we should switch to an append strategy to not override all results
            // with a new page.
            if (_this.state.searchQuery === searchQuery) {
                options.append = true;
            }
            onSearch(searchQuery, options);
            _this.setState({
                searchQuery: searchQuery,
            });
        }, 200);
        return _this;
    }
    GlobalSelectionHeader.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, className = _b.className, children = _b.children, shouldForceProject = _b.shouldForceProject, forceProject = _b.forceProject, isGlobalSelectionReady = _b.isGlobalSelectionReady, loadingProjects = _b.loadingProjects, organization = _b.organization, showAbsolute = _b.showAbsolute, showRelative = _b.showRelative, showDateSelector = _b.showDateSelector, showEnvironmentSelector = _b.showEnvironmentSelector, memberProjects = _b.memberProjects, nonMemberProjects = _b.nonMemberProjects, showIssueStreamLink = _b.showIssueStreamLink, showProjectSettingsLink = _b.showProjectSettingsLink, lockedMessageSubject = _b.lockedMessageSubject, timeRangeHint = _b.timeRangeHint, specificProjectSlugs = _b.specificProjectSlugs, disableMultipleProjectSelection = _b.disableMultipleProjectSelection, projectsFooterMessage = _b.projectsFooterMessage, defaultSelection = _b.defaultSelection;
        var _c = this.props.selection.datetime || {}, period = _c.period, start = _c.start, end = _c.end, utc = _c.utc;
        var defaultPeriod = ((_a = defaultSelection === null || defaultSelection === void 0 ? void 0 : defaultSelection.datetime) === null || _a === void 0 ? void 0 : _a.period) || DEFAULT_STATS_PERIOD;
        var selectedProjects = forceProject
            ? [parseInt(forceProject.id, 10)]
            : this.props.selection.projects;
        return (<React.Fragment>
        <Header className={className}>
          <HeaderItemPosition>
            {showIssueStreamLink && this.getBackButton()}
            <Projects orgId={organization.slug} limit={PROJECTS_PER_PAGE} slugs={specificProjectSlugs}>
              {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, hasMore = _a.hasMore, onSearch = _a.onSearch, fetching = _a.fetching;
            var paginatedProjectSelectorCallbacks = {
                onScroll: function (_a) {
                    var clientHeight = _a.clientHeight, scrollHeight = _a.scrollHeight, scrollTop = _a.scrollTop;
                    // check if no new projects are being fetched and the user has
                    // scrolled far enough to fetch a new page of projects
                    if (!fetching &&
                        scrollTop + clientHeight >= scrollHeight - clientHeight &&
                        hasMore) {
                        _this.scrollFetchDispatcher(onSearch, { append: true });
                    }
                },
                onFilterChange: function (event) {
                    _this.searchDispatcher(onSearch, event.target.value, {
                        append: false,
                    });
                },
                searching: fetching,
                paginated: true,
            };
            return (<MultipleProjectSelector organization={organization} shouldForceProject={shouldForceProject} forceProject={forceProject} projects={loadingProjects ? projects : memberProjects} isGlobalSelectionReady={isGlobalSelectionReady} isLoadingProjects={!initiallyLoaded} nonMemberProjects={nonMemberProjects} value={_this.state.projects || _this.props.selection.projects} onChange={_this.handleChangeProjects} onUpdate={_this.handleUpdateProjects} multi={!disableMultipleProjectSelection &&
                _this.hasMultipleProjectSelection()} {...(loadingProjects ? paginatedProjectSelectorCallbacks : {})} showIssueStreamLink={showIssueStreamLink} showProjectSettingsLink={showProjectSettingsLink} lockedMessageSubject={lockedMessageSubject} footerMessage={projectsFooterMessage}/>);
        }}
            </Projects>
          </HeaderItemPosition>

          {showEnvironmentSelector && (<React.Fragment>
              <HeaderSeparator />
              <HeaderItemPosition>
                <MultipleEnvironmentSelector organization={organization} projects={this.props.projects} loadingProjects={loadingProjects} selectedProjects={selectedProjects} value={this.props.selection.environments} onChange={this.handleChangeEnvironments} onUpdate={this.handleUpdateEnvironmments}/>
              </HeaderItemPosition>
            </React.Fragment>)}

          {showDateSelector && (<React.Fragment>
              <HeaderSeparator />
              <HeaderItemPosition>
                <TimeRangeSelector key={"period:" + period + "-start:" + start + "-end:" + end + "-utc:" + utc + "-defaultPeriod:" + defaultPeriod} showAbsolute={showAbsolute} showRelative={showRelative} relative={period} start={start} end={end} utc={utc} onChange={this.handleChangeTime} onUpdate={this.handleUpdateTime} organization={organization} defaultPeriod={defaultPeriod} hint={timeRangeHint}/>
              </HeaderItemPosition>
            </React.Fragment>)}

          {!showEnvironmentSelector && <HeaderItemPosition isSpacer/>}
          {!showDateSelector && <HeaderItemPosition isSpacer/>}
        </Header>

        {isGlobalSelectionReady ? children : <PageContent />}
      </React.Fragment>);
    };
    GlobalSelectionHeader.propTypes = {
        organization: SentryTypes.Organization,
        router: PropTypes.object,
        projects: PropTypes.arrayOf(SentryTypes.Project).isRequired,
        memberProjects: PropTypes.arrayOf(SentryTypes.Project).isRequired,
        nonMemberProjects: PropTypes.arrayOf(SentryTypes.Project).isRequired,
        /**
         * Slugs of projects to display in project selector (this affects the ^^^projects returned from HoC)
         */
        specificProjectSlugs: PropTypes.arrayOf(PropTypes.string),
        disableMultipleProjectSelection: PropTypes.bool,
        isGlobalSelectionReady: PropTypes.bool,
        loadingProjects: PropTypes.bool,
        shouldForceProject: PropTypes.bool,
        forceProject: SentryTypes.Project,
        selection: SentryTypes.GlobalSelection,
        showEnvironmentSelector: PropTypes.bool,
        showDateSelector: PropTypes.bool,
        hasCustomRouting: PropTypes.bool,
        resetParamsOnChange: PropTypes.arrayOf(PropTypes.string),
        showAbsolute: PropTypes.bool,
        showRelative: PropTypes.bool,
        timeRangeHint: PropTypes.string,
        // Callbacks //
        onChangeProjects: PropTypes.func,
        onUpdateProjects: PropTypes.func,
        onChangeEnvironments: PropTypes.func,
        onUpdateEnvironments: PropTypes.func,
        onChangeTime: PropTypes.func,
        onUpdateTime: PropTypes.func,
        showIssueStreamLink: PropTypes.bool,
        showProjectSettingsLink: PropTypes.bool,
        lockedMessageSubject: PropTypes.string,
        projectsFooterMessage: PropTypes.node,
    };
    GlobalSelectionHeader.defaultProps = defaultProps;
    return GlobalSelectionHeader;
}(React.Component));
export default withGlobalSelection(GlobalSelectionHeader);
var BackButtonWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  position: relative;\n  left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  position: relative;\n  left: ", ";\n"])), space(2));
var templateObject_1;
//# sourceMappingURL=globalSelectionHeader.jsx.map