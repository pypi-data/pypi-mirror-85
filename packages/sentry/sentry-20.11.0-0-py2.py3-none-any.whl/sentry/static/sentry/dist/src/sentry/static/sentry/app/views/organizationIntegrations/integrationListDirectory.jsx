import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import flatten from 'lodash/flatten';
import groupBy from 'lodash/groupBy';
import startCase from 'lodash/startCase';
import uniq from 'lodash/uniq';
import * as queryString from 'query-string';
import React from 'react';
import { browserHistory } from 'react-router';
import Feature from 'app/components/acl/feature';
import AsyncComponent from 'app/components/asyncComponent';
import SelectControl from 'app/components/forms/selectControl';
import { Panel, PanelBody } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import { getCategoriesForIntegration, getReauthAlertText, getSentryAppInstallStatus, isDocumentIntegration, isPlugin, isSentryApp, isSlackWorkspaceApp, trackIntegrationEvent, } from 'app/utils/integrationUtil';
import withOrganization from 'app/utils/withOrganization';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/organization/permissionAlert';
import { documentIntegrations, POPULARITY_WEIGHT } from './constants';
import IntegrationRow from './integrationRow';
var TEXT_SEARCH_ANALYTICS_DEBOUNCE_IN_MS = 1000;
var IntegrationListDirectory = /** @class */ (function (_super) {
    __extends(IntegrationListDirectory, _super);
    function IntegrationListDirectory() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Some integrations require visiting a different website to add them. When
        // we come back to the tab we want to show our integrations as soon as we can.
        _this.shouldReload = true;
        _this.reloadOnVisible = true;
        _this.shouldReloadOnVisible = true;
        _this.getAppInstall = function (app) {
            return _this.state.appInstalls.find(function (i) { return i.app.slug === app.slug; });
        };
        _this.getPopularityWeight = function (integration) { var _a; return (_a = POPULARITY_WEIGHT[integration.slug]) !== null && _a !== void 0 ? _a : 1; };
        _this.sortByName = function (a, b) {
            return a.slug.localeCompare(b.slug);
        };
        _this.sortByPopularity = function (a, b) {
            var weightA = _this.getPopularityWeight(a);
            var weightB = _this.getPopularityWeight(b);
            return weightB - weightA;
        };
        _this.sortByInstalled = function (a, b) {
            return _this.getInstallValue(b) - _this.getInstallValue(a);
        };
        _this.debouncedTrackIntegrationSearch = debounce(function (search, numResults) {
            trackIntegrationEvent({
                eventKey: 'integrations.directory_item_searched',
                eventName: 'Integrations: Directory Item Searched',
                view: 'integrations_directory',
                search_term: search,
                num_results: numResults,
            }, _this.props.organization);
        }, TEXT_SEARCH_ANALYTICS_DEBOUNCE_IN_MS);
        /**
         * Get filter parameters and guard against `queryString.parse` returning arrays.
         */
        _this.getFilterParameters = function () {
            var _a = queryString.parse(_this.props.location.search), category = _a.category, search = _a.search;
            var selectedCategory = Array.isArray(category) ? category[0] : category || '';
            var searchInput = Array.isArray(search) ? search[0] : search || '';
            return { searchInput: searchInput, selectedCategory: selectedCategory };
        };
        /**
         * Update the query string with the current filter parameter values.
         */
        _this.updateQueryString = function () {
            var _a = _this.state, searchInput = _a.searchInput, selectedCategory = _a.selectedCategory;
            var searchString = queryString.stringify(__assign(__assign({}, queryString.parse(_this.props.location.search)), { search: searchInput ? searchInput : undefined, category: selectedCategory ? selectedCategory : undefined }));
            browserHistory.replace({
                pathname: _this.props.location.pathname,
                search: searchString ? "?" + searchString : undefined,
            });
        };
        /**
         * Filter the integrations list by ANDing together the search query and the category select.
         */
        _this.updateDisplayedList = function () {
            var _a = _this.state, fuzzy = _a.fuzzy, list = _a.list, searchInput = _a.searchInput, selectedCategory = _a.selectedCategory;
            var displayedList = list;
            if (searchInput && fuzzy) {
                var searchResults = fuzzy.search(searchInput);
                displayedList = _this.sortIntegrations(searchResults.map(function (i) { return i.item; }));
            }
            if (selectedCategory) {
                displayedList = displayedList.filter(function (integration) {
                    return getCategoriesForIntegration(integration).includes(selectedCategory);
                });
            }
            _this.setState({ displayedList: displayedList });
            return displayedList;
        };
        _this.handleSearchChange = function (value) { return __awaiter(_this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                this.setState({ searchInput: value }, function () {
                    _this.updateQueryString();
                    var result = _this.updateDisplayedList();
                    if (value) {
                        _this.debouncedTrackIntegrationSearch(value, result.length);
                    }
                });
                return [2 /*return*/];
            });
        }); };
        _this.onCategorySelect = function (_a) {
            var category = _a.value;
            _this.setState({ selectedCategory: category }, function () {
                _this.updateQueryString();
                _this.updateDisplayedList();
                if (category) {
                    trackIntegrationEvent({
                        eventKey: 'integrations.directory_category_selected',
                        eventName: 'Integrations: Directory Category Selected',
                        view: 'integrations_directory',
                        category: category,
                    }, _this.props.organization);
                }
            });
        };
        // Rendering
        _this.renderProvider = function (provider) {
            var organization = _this.props.organization;
            //find the integration installations for that provider
            var integrations = _this.state.integrations.filter(function (i) { return i.provider.key === provider.key; });
            var hasWorkspaceApp = integrations.some(isSlackWorkspaceApp);
            return (<Feature key={"row-" + provider.key} organization={organization} features={['slack-migration']}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<IntegrationRow key={"row-" + provider.key} data-test-id="integration-row" organization={organization} type="firstParty" slug={provider.slug} displayName={provider.name} status={integrations.length ? 'Installed' : 'Not Installed'} publishStatus="published" configurations={integrations.length} categories={getCategoriesForIntegration(provider)} alertText={hasFeature && hasWorkspaceApp ? getReauthAlertText(provider) : undefined}/>);
            }}
      </Feature>);
        };
        _this.renderPlugin = function (plugin) {
            var organization = _this.props.organization;
            var isLegacy = plugin.isHidden;
            var displayName = plugin.name + " " + (isLegacy ? '(Legacy)' : '');
            //hide legacy integrations if we don't have any projects with them
            if (isLegacy && !plugin.projectList.length) {
                return null;
            }
            return (<IntegrationRow key={"row-plugin-" + plugin.id} data-test-id="integration-row" organization={organization} type="plugin" slug={plugin.slug} displayName={displayName} status={plugin.projectList.length ? 'Installed' : 'Not Installed'} publishStatus="published" configurations={plugin.projectList.length} categories={getCategoriesForIntegration(plugin)}/>);
        };
        //render either an internal or non-internal app
        _this.renderSentryApp = function (app) {
            var organization = _this.props.organization;
            var status = getSentryAppInstallStatus(_this.getAppInstall(app));
            var categories = getCategoriesForIntegration(app);
            return (<IntegrationRow key={"sentry-app-row-" + app.slug} data-test-id="integration-row" organization={organization} type="sentryApp" slug={app.slug} displayName={app.name} status={status} publishStatus={app.status} configurations={0} categories={categories}/>);
        };
        _this.renderDocumentIntegration = function (integration) {
            var organization = _this.props.organization;
            return (<IntegrationRow key={"doc-int-" + integration.slug} organization={organization} type="documentIntegration" slug={integration.slug} displayName={integration.name} publishStatus="published" configurations={0} categories={getCategoriesForIntegration(integration)}/>);
        };
        _this.renderIntegration = function (integration) {
            if (isSentryApp(integration)) {
                return _this.renderSentryApp(integration);
            }
            if (isPlugin(integration)) {
                return _this.renderPlugin(integration);
            }
            if (isDocumentIntegration(integration)) {
                return _this.renderDocumentIntegration(integration);
            }
            return _this.renderProvider(integration);
        };
        return _this;
    }
    IntegrationListDirectory.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { list: [], displayedList: [], selectedCategory: '' });
    };
    IntegrationListDirectory.prototype.onLoadAllEndpointsSuccess = function () {
        var _this = this;
        var _a = this.state, publishedApps = _a.publishedApps, orgOwnedApps = _a.orgOwnedApps, extraApp = _a.extraApp, plugins = _a.plugins;
        var published = publishedApps || [];
        // If we have an extra app in state from query parameter, add it as org owned app
        if (extraApp) {
            orgOwnedApps.push(extraApp);
        }
        // we dont want the app to render twice if its the org that created
        // the published app.
        var orgOwned = orgOwnedApps.filter(function (app) { return !published.find(function (p) { return p.slug === app.slug; }); });
        /**
         * We should have three sections:
         * 1. Public apps and integrations available to everyone
         * 2. Unpublished apps available to that org
         * 3. Internal apps available to that org
         */
        var combined = []
            .concat(published)
            .concat(orgOwned)
            .concat(this.providers)
            .concat(plugins)
            .concat(Object.values(documentIntegrations));
        var list = this.sortIntegrations(combined);
        var _b = this.getFilterParameters(), searchInput = _b.searchInput, selectedCategory = _b.selectedCategory;
        this.setState({ list: list, searchInput: searchInput, selectedCategory: selectedCategory }, function () {
            _this.updateDisplayedList();
            _this.trackPageViewed();
        });
    };
    IntegrationListDirectory.prototype.trackPageViewed = function () {
        //count the number of installed apps
        var _a = this.state, integrations = _a.integrations, publishedApps = _a.publishedApps, plugins = _a.plugins;
        var integrationsInstalled = new Set();
        //add installed integrations
        integrations.forEach(function (integration) {
            integrationsInstalled.add(integration.provider.key);
        });
        //add sentry apps
        publishedApps.filter(this.getAppInstall).forEach(function (sentryApp) {
            integrationsInstalled.add(sentryApp.slug);
        });
        //add plugins
        plugins.forEach(function (plugin) {
            if (plugin.projectList.length) {
                integrationsInstalled.add(plugin.slug);
            }
        });
        trackIntegrationEvent({
            eventKey: 'integrations.index_viewed',
            eventName: 'Integrations: Index Page Viewed',
            integrations_installed: integrationsInstalled.size,
            view: 'integrations_directory',
        }, this.props.organization, { startSession: true });
    };
    IntegrationListDirectory.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        var baseEndpoints = [
            ['config', "/organizations/" + orgId + "/config/integrations/"],
            [
                'integrations',
                "/organizations/" + orgId + "/integrations/",
                { query: { includeConfig: 0 } },
            ],
            ['orgOwnedApps', "/organizations/" + orgId + "/sentry-apps/"],
            ['publishedApps', '/sentry-apps/', { query: { status: 'published' } }],
            ['appInstalls', "/organizations/" + orgId + "/sentry-app-installations/"],
            ['plugins', "/organizations/" + orgId + "/plugins/configs/"],
        ];
        /**
         * optional app to load for super users
         * should only be done for unpublished integrations from another org
         * but no checks are in place to ensure the above condition
         */
        var extraAppSlug = new URLSearchParams(this.props.location.search).get('extra_app');
        if (extraAppSlug) {
            baseEndpoints.push(['extraApp', "/sentry-apps/" + extraAppSlug + "/"]);
        }
        return baseEndpoints;
    };
    Object.defineProperty(IntegrationListDirectory.prototype, "unmigratableReposByOrg", {
        // State
        get: function () {
            // Group by [GitHub|BitBucket|VSTS] Org name
            return groupBy(this.state.unmigratableRepos, function (repo) { return repo.name.split('/')[0]; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationListDirectory.prototype, "providers", {
        get: function () {
            return this.state.config.providers;
        },
        enumerable: false,
        configurable: true
    });
    //Returns 0 if uninstalled, 1 if pending, and 2 if installed
    IntegrationListDirectory.prototype.getInstallValue = function (integration) {
        var integrations = this.state.integrations;
        if (isPlugin(integration)) {
            return integration.projectList.length > 0 ? 2 : 0;
        }
        if (isSentryApp(integration)) {
            var install = this.getAppInstall(integration);
            if (install) {
                return install.status === 'pending' ? 1 : 2;
            }
            return 0;
        }
        if (isDocumentIntegration(integration)) {
            return 0;
        }
        return integrations.find(function (i) { return i.provider.key === integration.key; }) ? 2 : 0;
    };
    IntegrationListDirectory.prototype.sortIntegrations = function (integrations) {
        var _this = this;
        return integrations.sort(function (a, b) {
            //sort by whether installed first
            var diffWeight = _this.sortByInstalled(a, b);
            if (diffWeight !== 0) {
                return diffWeight;
            }
            //then sort by popularity
            var diffPop = _this.sortByPopularity(a, b);
            if (diffPop !== 0) {
                return diffPop;
            }
            //then sort by name
            return _this.sortByName(a, b);
        });
    };
    IntegrationListDirectory.prototype.componentDidUpdate = function (_, prevState) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!(this.state.list.length !== prevState.list.length)) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.createSearch()];
                    case 1:
                        _a.sent();
                        _a.label = 2;
                    case 2: return [2 /*return*/];
                }
            });
        });
    };
    IntegrationListDirectory.prototype.createSearch = function () {
        return __awaiter(this, void 0, void 0, function () {
            var list, _a;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        list = this.state.list;
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, createFuzzySearch(list || [], {
                                threshold: 0.3,
                                location: 0,
                                distance: 100,
                                keys: ['slug', 'key', 'name', 'id'],
                            })];
                    case 1:
                        _a.apply(this, [(_b.fuzzy = _c.sent(),
                                _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    IntegrationListDirectory.prototype.renderBody = function () {
        var orgId = this.props.params.orgId;
        var _a = this.state, displayedList = _a.displayedList, list = _a.list, searchInput = _a.searchInput, selectedCategory = _a.selectedCategory;
        var title = t('Integrations');
        var categoryList = uniq(flatten(list.map(getCategoriesForIntegration))).sort();
        return (<React.Fragment>
        <SentryDocumentTitle title={title} objSlug={orgId}/>

        {!this.props.hideHeader && (<SettingsPageHeader title={title} action={<ActionContainer>
                <SelectControl name="select-categories" onChange={this.onCategorySelect} value={selectedCategory} choices={__spread([
            ['', t('All Categories')]
        ], categoryList.map(function (category) { return [category, startCase(category)]; }))}/>
                <SearchBar query={searchInput || ''} onChange={this.handleSearchChange} placeholder={t('Filter Integrations...')} width="25em"/>
              </ActionContainer>}/>)}

        <PermissionAlert access={['org:integrations']}/>
        <Panel>
          <PanelBody>
            {displayedList.length ? (displayedList.map(this.renderIntegration)) : (<EmptyResultsContainer>
                <EmptyResultsBody>
                  {tct('No Integrations found for "[searchTerm]".', {
            searchTerm: searchInput,
        })}
                </EmptyResultsBody>
                <EmptyResultsBodyBold>
                  {t("Not seeing what you're looking for?")}
                </EmptyResultsBodyBold>
                <EmptyResultsBody>
                  {tct('[link:Build it on the Sentry Integration Platform.]', {
            link: (<a href="https://docs.sentry.io/workflow/integrations/integration-platform/"/>),
        })}
                </EmptyResultsBody>
              </EmptyResultsContainer>)}
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    return IntegrationListDirectory;
}(AsyncComponent));
export { IntegrationListDirectory };
var ActionContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 240px max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 240px max-content;\n  grid-gap: ", ";\n"])), space(2));
var EmptyResultsContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 200px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n"], ["\n  height: 200px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n"])));
var EmptyResultsBody = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 16px;\n  line-height: 28px;\n  color: ", ";\n  padding-bottom: ", ";\n"], ["\n  font-size: 16px;\n  line-height: 28px;\n  color: ", ";\n  padding-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, space(2));
var EmptyResultsBodyBold = styled(EmptyResultsBody)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
export default withOrganization(IntegrationListDirectory);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=integrationListDirectory.jsx.map