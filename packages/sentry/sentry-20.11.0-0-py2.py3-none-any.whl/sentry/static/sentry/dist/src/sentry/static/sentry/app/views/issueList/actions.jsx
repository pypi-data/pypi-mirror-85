import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import capitalize from 'lodash/capitalize';
import uniq from 'lodash/uniq';
import React from 'react';
import styled from '@emotion/styled';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import { t, tct, tn } from 'app/locale';
import { IconEllipsis, IconPause, IconPlay, IconIssues } from 'app/icons';
import { ResolutionStatus } from 'app/types';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import ActionLink from 'app/components/actions/actionLink';
import Checkbox from 'app/components/checkbox';
import DropdownLink from 'app/components/dropdownLink';
import ExternalLink from 'app/components/links/externalLink';
import GroupStore from 'app/stores/groupStore';
import IgnoreActions from 'app/components/actions/ignore';
import MenuItem from 'app/components/menuItem';
import Projects from 'app/utils/projects';
import ResolveActions from 'app/components/actions/resolve';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
import ToolbarHeader from 'app/components/toolbarHeader';
import Tooltip from 'app/components/tooltip';
import Feature from 'app/components/acl/feature';
import { callIfFunction } from 'app/utils/callIfFunction';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var BULK_LIMIT = 1000;
var BULK_LIMIT_STR = BULK_LIMIT.toLocaleString();
var getBulkConfirmMessage = function (action, queryCount) {
    if (queryCount > BULK_LIMIT) {
        return tct('Are you sure you want to [action] the first [bulkNumber] issues that match the search?', {
            action: action,
            bulkNumber: BULK_LIMIT_STR,
        });
    }
    return tct('Are you sure you want to [action] all [bulkNumber] issues that match the search?', {
        action: action,
        bulkNumber: queryCount,
    });
};
var getConfirm = function (numIssues, allInQuerySelected, query, queryCount) {
    return function (action, canBeUndone, append) {
        if (append === void 0) { append = ''; }
        var question = allInQuerySelected
            ? getBulkConfirmMessage("" + action + append, queryCount)
            : tn("Are you sure you want to " + action + " this %s issue" + append + "?", "Are you sure you want to " + action + " these %s issues" + append + "?", numIssues);
        var message = action === 'delete'
            ? tct('Bulk deletion is only recommended for junk data. To clear your stream, consider resolving or ignoring. [link:When should I delete events?]', {
                link: (<ExternalLink href="https://help.sentry.io/hc/en-us/articles/360003443113-When-should-I-delete-events"/>),
            })
            : t('This action cannot be undone.');
        return (<div>
        <p style={{ marginBottom: '20px' }}>
          <strong>{question}</strong>
        </p>
        <ExtraDescription all={allInQuerySelected} query={query} queryCount={queryCount}/>
        {!canBeUndone && <p>{message}</p>}
      </div>);
    };
};
var getLabel = function (numIssues, allInQuerySelected) {
    return function (action, append) {
        if (append === void 0) { append = ''; }
        var capitalized = capitalize(action);
        var text = allInQuerySelected
            ? t("Bulk " + action + " issues")
            : tn(capitalized + " %s selected issue", capitalized + " %s selected issues", numIssues);
        return text + append;
    };
};
var ExtraDescription = function (_a) {
    var all = _a.all, query = _a.query, queryCount = _a.queryCount;
    if (!all) {
        return null;
    }
    if (query) {
        return (<div>
        <p>{t('This will apply to the current search query') + ':'}</p>
        <pre>{query}</pre>
      </div>);
    }
    return (<p className="error">
      <strong>
        {queryCount > BULK_LIMIT
        ? tct('This will apply to the first [bulkNumber] issues matched in this project!', {
            bulkNumber: BULK_LIMIT_STR,
        })
        : tct('This will apply to all [bulkNumber] issues matched in this project!', {
            bulkNumber: queryCount,
        })}
      </strong>
    </p>);
};
var IssueListActions = /** @class */ (function (_super) {
    __extends(IssueListActions, _super);
    function IssueListActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            datePickerActive: false,
            anySelected: false,
            multiSelected: false,
            pageSelected: false,
            allInQuerySelected: false,
            selectedIds: new Set(),
        };
        _this.listener = SelectedGroupStore.listen(function () { return _this.handleSelectedGroupChange(); }, undefined);
        _this.handleApplyToAll = function () {
            _this.setState({
                allInQuerySelected: true,
            });
        };
        _this.handleUpdate = function (data) {
            var selection = _this.props.selection;
            _this.actionSelectedGroups(function (itemIds) {
                addLoadingMessage(t('Saving changes\u2026'));
                // If `itemIds` is undefined then it means we expect to bulk update all items
                // that match the query.
                //
                // We need to always respect the projects selected in the global selection header:
                // * users with no global views requires a project to be specified
                // * users with global views need to be explicit about what projects the query will run against
                var projectConstraints = { project: selection.projects };
                _this.props.api.bulkUpdate(__assign(__assign({ orgId: _this.props.orgId, itemIds: itemIds,
                    data: data, query: _this.props.query, environment: selection.environments }, projectConstraints), selection.datetime), {
                    complete: function () {
                        clearIndicators();
                    },
                });
            });
        };
        _this.handleDelete = function () {
            var selection = _this.props.selection;
            addLoadingMessage(t('Removing events\u2026'));
            _this.actionSelectedGroups(function (itemIds) {
                _this.props.api.bulkDelete(__assign({ orgId: _this.props.orgId, itemIds: itemIds, query: _this.props.query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: function () {
                        clearIndicators();
                    },
                });
            });
        };
        _this.handleMerge = function () {
            var selection = _this.props.selection;
            addLoadingMessage(t('Merging events\u2026'));
            _this.actionSelectedGroups(function (itemIds) {
                _this.props.api.merge(__assign({ orgId: _this.props.orgId, itemIds: itemIds, query: _this.props.query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: function () {
                        clearIndicators();
                    },
                });
            });
        };
        _this.handleRealtimeChange = function () {
            _this.props.onRealtimeChange(!_this.props.realtimeActive);
        };
        _this.shouldConfirm = function (action) {
            var selectedItems = SelectedGroupStore.getSelectedIds();
            switch (action) {
                case 'resolve':
                case 'unresolve':
                case 'ignore':
                case 'unbookmark':
                    return _this.state.pageSelected && selectedItems.size > 1;
                case 'backlog':
                case 'bookmark':
                    return selectedItems.size > 1;
                case 'merge':
                case 'delete':
                default:
                    return true; // By default, should confirm ...
            }
        };
        return _this;
    }
    IssueListActions.prototype.componentDidMount = function () {
        this.handleSelectedGroupChange();
    };
    IssueListActions.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    IssueListActions.prototype.actionSelectedGroups = function (callback) {
        var selectedIds;
        if (this.state.allInQuerySelected) {
            selectedIds = undefined; // undefined means "all"
        }
        else {
            var itemIdSet_1 = SelectedGroupStore.getSelectedIds();
            selectedIds = this.props.groupIds.filter(function (itemId) { return itemIdSet_1.has(itemId); });
        }
        callback(selectedIds);
        this.deselectAll();
    };
    IssueListActions.prototype.deselectAll = function () {
        SelectedGroupStore.deselectAll();
        this.setState({ allInQuerySelected: false });
    };
    // Handler for when `SelectedGroupStore` changes
    IssueListActions.prototype.handleSelectedGroupChange = function () {
        var selected = SelectedGroupStore.getSelectedIds();
        var projects = __spread(selected).map(function (id) { return GroupStore.get(id); })
            .filter(function (group) { return !!(group && group.project); })
            .map(function (group) { return group.project.slug; });
        var uniqProjects = uniq(projects);
        // we only want selectedProjectSlug set if there is 1 project
        // more or fewer should result in a null so that the action toolbar
        // can behave correctly.
        var selectedProjectSlug = uniqProjects.length === 1 ? uniqProjects[0] : undefined;
        this.setState({
            pageSelected: SelectedGroupStore.allSelected(),
            multiSelected: SelectedGroupStore.multiSelected(),
            anySelected: SelectedGroupStore.anySelected(),
            allInQuerySelected: false,
            selectedIds: SelectedGroupStore.getSelectedIds(),
            selectedProjectSlug: selectedProjectSlug,
        });
    };
    IssueListActions.prototype.handleSelectStatsPeriod = function (period) {
        return this.props.onSelectStatsPeriod(period);
    };
    IssueListActions.prototype.handleSelectAll = function () {
        SelectedGroupStore.toggleSelectAll();
    };
    IssueListActions.prototype.renderResolveActions = function (params) {
        var hasReleases = params.hasReleases, latestRelease = params.latestRelease, projectId = params.projectId, confirm = params.confirm, label = params.label, loadingProjects = params.loadingProjects, projectFetchError = params.projectFetchError;
        var orgId = this.props.orgId;
        var anySelected = this.state.anySelected;
        // resolve requires a single project to be active in an org context
        // projectId is null when 0 or >1 projects are selected.
        var resolveDisabled = Boolean(!anySelected || projectFetchError);
        var resolveDropdownDisabled = Boolean(!anySelected || !projectId || loadingProjects || projectFetchError);
        return (<ResolveActions hasRelease={hasReleases} latestRelease={latestRelease} orgId={orgId} projectId={projectId} onUpdate={this.handleUpdate} shouldConfirm={this.shouldConfirm('resolve')} confirmMessage={confirm('resolve', true)} confirmLabel={label('resolve')} disabled={resolveDisabled} disableDropdown={resolveDropdownDisabled} projectFetchError={projectFetchError}/>);
    };
    IssueListActions.prototype.render = function () {
        var _this = this;
        var _a = this.props, allResultsVisible = _a.allResultsVisible, orgId = _a.orgId, queryCount = _a.queryCount, query = _a.query, realtimeActive = _a.realtimeActive, selection = _a.selection, statsPeriod = _a.statsPeriod, organization = _a.organization, groupIds = _a.groupIds, issuesLoading = _a.issuesLoading;
        var issues = this.state.selectedIds;
        var numIssues = issues.size;
        var _b = this.state, allInQuerySelected = _b.allInQuerySelected, anySelected = _b.anySelected, multiSelected = _b.multiSelected, pageSelected = _b.pageSelected, selectedProjectSlug = _b.selectedProjectSlug;
        var confirm = getConfirm(numIssues, allInQuerySelected, query, queryCount);
        var label = getLabel(numIssues, allInQuerySelected);
        // merges require a single project to be active in an org context
        // selectedProjectSlug is null when 0 or >1 projects are selected.
        var mergeDisabled = !(multiSelected && selectedProjectSlug);
        var hasInboxReason = issuesLoading || groupIds.some(function (id) { var _a; return !!((_a = GroupStore.get(id)) === null || _a === void 0 ? void 0 : _a.inbox); });
        return (<Sticky>
        <StyledFlex>
          <ActionsCheckbox>
            <Checkbox onChange={this.handleSelectAll} checked={pageSelected}/>
          </ActionsCheckbox>
          <ActionSet>
            <Feature organization={organization} features={['organizations:inbox']}>
              <div className="btn-group hidden-sm hidden-xs">
                <StyledActionLink className="btn btn-default btn-sm action-merge" data-test-id="button-backlog" disabled={!anySelected} onAction={function () { return _this.handleUpdate({ inbox: false }); }} shouldConfirm={this.shouldConfirm('backlog')} message={confirm('move', false, ' to the backlog')} confirmLabel={label('backlog')} title={t('Move to backlog')}>
                  <StyledIconIssues size="xs"/>
                  {t('Backlog')}
                </StyledActionLink>
              </div>
            </Feature>
            {selectedProjectSlug ? (<Projects orgId={orgId} slugs={[selectedProjectSlug]}>
                {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
            var selectedProject = projects[0];
            return _this.renderResolveActions({
                hasReleases: selectedProject.hasOwnProperty('features')
                    ? selectedProject.features.includes('releases')
                    : false,
                latestRelease: selectedProject.hasOwnProperty('latestRelease')
                    ? selectedProject.latestRelease
                    : undefined,
                projectId: selectedProject.slug,
                confirm: confirm,
                label: label,
                loadingProjects: !initiallyLoaded,
                projectFetchError: !!fetchError,
            });
        }}
              </Projects>) : (this.renderResolveActions({
            hasReleases: false,
            latestRelease: null,
            projectId: null,
            confirm: confirm,
            label: label,
        }))}
            <IgnoreActions onUpdate={this.handleUpdate} shouldConfirm={this.shouldConfirm('ignore')} confirmMessage={confirm('ignore', true)} confirmLabel={label('ignore')} disabled={!anySelected}/>
            <div className="btn-group hidden-md hidden-sm hidden-xs">
              <ActionLink className="btn btn-default btn-sm action-merge" disabled={mergeDisabled} onAction={this.handleMerge} shouldConfirm={this.shouldConfirm('merge')} message={confirm('merge', false)} confirmLabel={label('merge')} title={t('Merge Selected Issues')}>
                {t('Merge')}
              </ActionLink>
            </div>
            <div className="btn-group">
              <DropdownLink key="actions" caret={false} className="btn btn-sm btn-default action-more" title={<IconPad>
                    <IconEllipsis size="xs"/>
                  </IconPad>}>
                <MenuItem noAnchor>
                  <ActionLink className="action-merge hidden-lg hidden-xl" disabled={mergeDisabled} onAction={this.handleMerge} shouldConfirm={this.shouldConfirm('merge')} message={confirm('merge', false)} confirmLabel={label('merge')} title={t('Merge Selected Issues')}>
                    {t('Merge')}
                  </ActionLink>
                </MenuItem>
                <Feature organization={organization} features={['organizations:inbox']}>
                  <MenuItem divider className="hidden-md hidden-lg hidden-xl"/>
                  <MenuItem noAnchor>
                    <ActionLink className="action-backlog hidden-md hidden-lg hidden-xl" disabled={!anySelected} onAction={function () { return _this.handleUpdate({ inbox: false }); }} shouldConfirm={this.shouldConfirm('backlog')} message={confirm('move', false, ' to the backlog')} confirmLabel={label('backlog')} title={t('Move to backlog')}>
                      {t('Move to backlog')}
                    </ActionLink>
                  </MenuItem>
                </Feature>
                <MenuItem divider className="hidden-lg hidden-xl"/>
                <MenuItem noAnchor>
                  <ActionLink className="action-bookmark" disabled={!anySelected} onAction={function () { return _this.handleUpdate({ isBookmarked: true }); }} shouldConfirm={this.shouldConfirm('bookmark')} message={confirm('bookmark', false)} confirmLabel={label('bookmark')} title={t('Add to Bookmarks')}>
                    {t('Add to Bookmarks')}
                  </ActionLink>
                </MenuItem>
                <MenuItem divider/>
                <MenuItem noAnchor>
                  <ActionLink className="action-remove-bookmark" disabled={!anySelected} onAction={function () { return _this.handleUpdate({ isBookmarked: false }); }} shouldConfirm={this.shouldConfirm('unbookmark')} message={confirm('remove', false, ' from your bookmarks')} confirmLabel={label('remove', ' from your bookmarks')} title={t('Remove from Bookmarks')}>
                    {t('Remove from Bookmarks')}
                  </ActionLink>
                </MenuItem>
                <MenuItem divider/>
                <MenuItem noAnchor>
                  <ActionLink className="action-unresolve" disabled={!anySelected} onAction={function () {
            return _this.handleUpdate({ status: ResolutionStatus.UNRESOLVED });
        }} shouldConfirm={this.shouldConfirm('unresolve')} message={confirm('unresolve', true)} confirmLabel={label('unresolve')} title={t('Set status to: Unresolved')}>
                    {t('Set status to: Unresolved')}
                  </ActionLink>
                </MenuItem>
                <MenuItem divider/>
                <MenuItem noAnchor>
                  <ActionLink className="action-delete" disabled={!anySelected} onAction={this.handleDelete} shouldConfirm={this.shouldConfirm('delete')} message={confirm('delete', false)} confirmLabel={label('delete')} title={t('Delete Issues')}>
                    {t('Delete Issues')}
                  </ActionLink>
                </MenuItem>
              </DropdownLink>
            </div>
            <div className="btn-group">
              <Tooltip title={t('%s real-time updates', realtimeActive ? t('Pause') : t('Enable'))}>
                <a data-test-id="realtime-control" className="btn btn-default btn-sm hidden-xs" onClick={this.handleRealtimeChange}>
                  <IconPad>
                    {realtimeActive ? <IconPause size="xs"/> : <IconPlay size="xs"/>}
                  </IconPad>
                </a>
              </Tooltip>
            </div>
          </ActionSet>
          <GraphHeaderWrapper className="hidden-xs hidden-sm">
            <GraphHeader>
              <StyledToolbarHeader>{t('Graph:')}</StyledToolbarHeader>
              <GraphToggle active={statsPeriod === '24h'} onClick={this.handleSelectStatsPeriod.bind(this, '24h')}>
                {t('24h')}
              </GraphToggle>
              <GraphToggle active={statsPeriod === 'auto'} onClick={this.handleSelectStatsPeriod.bind(this, 'auto')}>
                {selection.datetime.period || t('Custom')}
              </GraphToggle>
            </GraphHeader>
          </GraphHeaderWrapper>
          <React.Fragment>
            <EventsOrUsersLabel className="align-right">{t('Events')}</EventsOrUsersLabel>
            <EventsOrUsersLabel className="align-right">{t('Users')}</EventsOrUsersLabel>
          </React.Fragment>
          <AssigneesLabel className="align-right hidden-xs hidden-sm">
            <ToolbarHeader>{t('Assignee')}</ToolbarHeader>
          </AssigneesLabel>
          <Feature organization={organization} features={['organizations:inbox']}>
            {hasInboxReason && <ReasonSpacerLabel className="hidden-xs hidden-sm"/>}
            <TimesSpacerLabel className="hidden-xs hidden-sm"/>
          </Feature>
        </StyledFlex>

        {!allResultsVisible && pageSelected && (<SelectAllNotice>
            {allInQuerySelected ? (queryCount >= BULK_LIMIT ? (tct('Selected up to the first [count] issues that match this search query.', {
            count: BULK_LIMIT_STR,
        })) : (tct('Selected all [count] issues that match this search query.', {
            count: queryCount,
        }))) : (<React.Fragment>
                {tn('%s issue on this page selected.', '%s issues on this page selected.', numIssues)}
                <SelectAllLink onClick={this.handleApplyToAll}>
                  {queryCount >= BULK_LIMIT
            ? tct('Select the first [count] issues that match this search query.', {
                count: BULK_LIMIT_STR,
            })
            : tct('Select all [count] issues that match this search query.', {
                count: queryCount,
            })}
                </SelectAllLink>
              </React.Fragment>)}
          </SelectAllNotice>)}
      </Sticky>);
    };
    return IssueListActions;
}(React.Component));
var Sticky = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: sticky;\n  z-index: ", ";\n  top: -1px;\n"], ["\n  position: sticky;\n  z-index: ", ";\n  top: -1px;\n"])), function (p) { return p.theme.zIndex.header; });
var StyledFlex = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  align-items: center;\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  margin-bottom: -1px;\n"], ["\n  display: flex;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  align-items: center;\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  margin-bottom: -1px;\n"])), space(1), space(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var ActionsCheckbox = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-left: ", ";\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"], ["\n  padding-left: ", ";\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"])), space(2));
var ActionSet = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n\n  display: flex;\n\n  .btn-group {\n    display: flex;\n    margin-right: 6px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n\n  display: flex;\n\n  .btn-group {\n    display: flex;\n    margin-right: 6px;\n  }\n"])), theme.breakpoints[0], theme.breakpoints[2], space(1), space(1));
var GraphHeaderWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n"], ["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n"])), space(2), space(2));
var GraphHeader = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledToolbarHeader = styled(ToolbarHeader)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var StyledActionLink = styled(ActionLink)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
var StyledIconIssues = styled(IconIssues)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var GraphToggle = styled('a')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: 13px;\n  padding-left: 8px;\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  font-size: 13px;\n  padding-left: 8px;\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return (p.active ? p.theme.textColor : p.theme.disabled); });
var EventsOrUsersLabel = styled(ToolbarHeader)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n\n  margin-left: ", ";\n  margin-right: ", ";\n  @media (min-width: ", ") {\n    width: 60px;\n  }\n  @media (min-width: ", ") {\n    width: 60px;\n  }\n  @media (min-width: ", ") {\n    width: 80px;\n    margin-left: ", ";\n    margin-right: ", ";\n  }\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n\n  margin-left: ", ";\n  margin-right: ", ";\n  @media (min-width: ", ") {\n    width: 60px;\n  }\n  @media (min-width: ", ") {\n    width: 60px;\n  }\n  @media (min-width: ", ") {\n    width: 80px;\n    margin-left: ", ";\n    margin-right: ", ";\n  }\n"])), space(0.5), space(1.5), space(1.5), theme.breakpoints[0], theme.breakpoints[1], theme.breakpoints[2], space(2), space(2));
var AssigneesLabel = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"], ["\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"])), space(2), space(2));
var ReasonSpacerLabel = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  width: 95px;\n  margin: 0 ", " 0 ", ";\n"], ["\n  width: 95px;\n  margin: 0 ", " 0 ", ";\n"])), space(0.25), space(1));
var TimesSpacerLabel = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  width: 170px;\n  margin: 0 ", " 0 ", ";\n"], ["\n  width: 170px;\n  margin: 0 ", " 0 ", ";\n"])), space(1.5), space(0.5));
// New icons are misaligned inside bootstrap buttons.
// This is a shim that can be removed when buttons are upgraded
// to styled components.
var IconPad = styled('span')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  position: relative;\n  top: ", ";\n"], ["\n  position: relative;\n  top: ", ";\n"])), space(0.25));
var SelectAllNotice = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n  text-align: center;\n  padding: ", " ", ";\n"], ["\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n  text-align: center;\n  padding: ", " ", ";\n"])), function (p) { return p.theme.yellow100; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.fontSizeMedium; }, space(0.5), space(1.5));
var SelectAllLink = styled('a')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
export { IssueListActions };
export default withApi(withOrganization(IssueListActions));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=actions.jsx.map