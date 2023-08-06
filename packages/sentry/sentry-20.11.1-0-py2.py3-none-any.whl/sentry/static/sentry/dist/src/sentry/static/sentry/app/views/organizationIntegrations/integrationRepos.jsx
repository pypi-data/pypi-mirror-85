import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import debounce from 'lodash/debounce';
import React from 'react';
import styled from '@emotion/styled';
import { migrateRepository, addRepository } from 'app/actionCreators/integrations';
import RepositoryActions from 'app/actions/repositoryActions';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import { IconCommit, IconFlag } from 'app/icons';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import Pagination from 'app/components/pagination';
import RepositoryRow from 'app/components/repositoryRow';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import space from 'app/styles/space';
import { t } from 'app/locale';
var IntegrationRepos = /** @class */ (function (_super) {
    __extends(IntegrationRepos, _super);
    function IntegrationRepos() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Called by row to signal repository change.
        _this.onRepositoryChange = function (data) {
            var itemList = _this.state.itemList;
            itemList.forEach(function (item) {
                if (item.id === data.id) {
                    item.status = data.status;
                }
            });
            _this.setState({ itemList: itemList });
            RepositoryActions.resetRepositories();
        };
        _this.debouncedSearchRepositoriesRequest = debounce(function (query) { return _this.searchRepositoriesRequest(query); }, 200);
        _this.searchRepositoriesRequest = function (searchQuery) {
            var orgId = _this.context.organization.slug;
            var query = { search: searchQuery };
            var endpoint = "/organizations/" + orgId + "/integrations/" + _this.props.integration.id + "/repos/";
            return _this.api.request(endpoint, {
                method: 'GET',
                query: query,
                success: function (data) {
                    _this.setState({ integrationRepos: data, dropdownBusy: false });
                },
                error: function () {
                    _this.setState({ dropdownBusy: false });
                },
            });
        };
        _this.handleSearchRepositories = function (e) {
            _this.setState({ dropdownBusy: true });
            _this.debouncedSearchRepositoriesRequest(e.target.value);
        };
        return _this;
    }
    IntegrationRepos.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { adding: false, itemList: [], integrationRepos: { repos: [], searchable: false }, dropdownBusy: false });
    };
    IntegrationRepos.prototype.getEndpoints = function () {
        var orgId = this.context.organization.slug;
        return [
            ['itemList', "/organizations/" + orgId + "/repos/", { query: { status: '' } }],
            [
                'integrationRepos',
                "/organizations/" + orgId + "/integrations/" + this.props.integration.id + "/repos/",
            ],
        ];
    };
    IntegrationRepos.prototype.getIntegrationRepos = function () {
        var integrationId = this.props.integration.id;
        return this.state.itemList.filter(function (repo) { return repo.integrationId === integrationId; });
    };
    IntegrationRepos.prototype.addRepo = function (selection) {
        var _this = this;
        var integration = this.props.integration;
        var itemList = this.state.itemList;
        var orgId = this.context.organization.slug;
        this.setState({ adding: true });
        var migratableRepo = itemList.filter(function (item) {
            if (!(selection.value && item.externalSlug)) {
                return false;
            }
            return selection.value === item.externalSlug;
        })[0];
        var promise;
        if (migratableRepo) {
            promise = migrateRepository(this.api, orgId, migratableRepo.id, integration);
        }
        else {
            promise = addRepository(this.api, orgId, selection.value, integration);
        }
        promise.then(function (repo) {
            _this.setState({ adding: false, itemList: itemList.concat(repo) });
            RepositoryActions.resetRepositories();
        }, function () { return _this.setState({ adding: false }); });
    };
    IntegrationRepos.prototype.renderDropdown = function () {
        var _this = this;
        var access = new Set(this.context.organization.access);
        if (!access.has('org:integrations')) {
            return (<DropdownButton disabled title={t('You must be an organization owner, manager or admin to add repositories')} isOpen={false} size="xsmall">
          {t('Add Repository')}
        </DropdownButton>);
        }
        var repositories = new Set(this.state.itemList.filter(function (item) { return item.integrationId; }).map(function (i) { return i.externalSlug; }));
        var repositoryOptions = (this.state.integrationRepos.repos || []).filter(function (repo) { return !repositories.has(repo.identifier); });
        var items = repositoryOptions.map(function (repo) { return ({
            searchKey: repo.name,
            value: repo.identifier,
            label: (<StyledListElement>
          <StyledName>{repo.name}</StyledName>
        </StyledListElement>),
        }); });
        var menuHeader = <StyledReposLabel>{t('Repositories')}</StyledReposLabel>;
        var onChange = this.state.integrationRepos.searchable
            ? this.handleSearchRepositories
            : undefined;
        return (<DropdownAutoComplete items={items} onSelect={this.addRepo.bind(this)} onChange={onChange} menuHeader={menuHeader} emptyMessage={t('No repositories available')} noResultsMessage={t('No repositories found')} busy={this.state.dropdownBusy} alignMenu="right">
        {function (_a) {
            var isOpen = _a.isOpen;
            return (<DropdownButton isOpen={isOpen} size="xsmall" busy={_this.state.adding}>
            {t('Add Repository')}
          </DropdownButton>);
        }}
      </DropdownAutoComplete>);
    };
    IntegrationRepos.prototype.renderError = function (error) {
        var badRequest = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 400; });
        if (badRequest) {
            return (<Alert type="error" icon={<IconFlag size="md"/>}>
          {t('We were unable to fetch repositories for this integration. Try again later, or reconnect this integration.')}
        </Alert>);
        }
        return _super.prototype.renderError.call(this, error);
    };
    IntegrationRepos.prototype.renderBody = function () {
        var _this = this;
        var itemListPageLinks = this.state.itemListPageLinks;
        var orgId = this.context.organization.slug;
        var itemList = this.getIntegrationRepos() || [];
        var header = (<PanelHeader disablePadding hasButtons>
        <HeaderText>{t('Repositories')}</HeaderText>
        <DropdownWrapper>{this.renderDropdown()}</DropdownWrapper>
      </PanelHeader>);
        return (<React.Fragment>
        <Panel>
          {header}
          <PanelBody>
            {itemList.length === 0 && (<EmptyMessage icon={<IconCommit />} title={t('Sentry is better with commit data')} description={t('Add a repository to begin tracking its commit data. Then, set up release tracking to unlock features like suspect commits, suggested issue owners, and deploy emails.')} action={<Button href="https://docs.sentry.io/learn/releases/">
                    {t('Learn More')}
                  </Button>}/>)}
            {itemList.map(function (repo) { return (<RepositoryRow key={repo.id} repository={repo} orgId={orgId} api={_this.api} onRepositoryChange={_this.onRepositoryChange}/>); })}
          </PanelBody>
        </Panel>
        {itemListPageLinks && (<Pagination pageLinks={itemListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    IntegrationRepos.propTypes = {
        integration: PropTypes.object.isRequired,
    };
    IntegrationRepos.contextTypes = {
        organization: PropTypes.object.isRequired,
        router: PropTypes.object,
    };
    return IntegrationRepos;
}(AsyncComponent));
export default IntegrationRepos;
var HeaderText = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-left: ", ";\n  flex: 1;\n"], ["\n  padding-left: ", ";\n  flex: 1;\n"])), space(2));
var DropdownWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: ", ";\n  text-transform: none;\n"], ["\n  padding-right: ", ";\n  text-transform: none;\n"])), space(1));
var StyledReposLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 250px;\n  font-size: 0.875em;\n  padding: ", " 0;\n  text-transform: uppercase;\n"], ["\n  width: 250px;\n  font-size: 0.875em;\n  padding: ", " 0;\n  text-transform: uppercase;\n"])), space(1));
var StyledListElement = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space(0.5));
var StyledName = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0;\n  ", ";\n"], ["\n  flex-shrink: 1;\n  min-width: 0;\n  ", ";\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=integrationRepos.jsx.map