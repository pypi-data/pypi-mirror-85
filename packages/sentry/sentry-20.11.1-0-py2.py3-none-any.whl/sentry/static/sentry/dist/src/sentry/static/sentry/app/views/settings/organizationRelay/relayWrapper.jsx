import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import { updateOrganization } from 'app/actionCreators/organizations';
import { openModal } from 'app/actionCreators/modal';
import { t, tct } from 'app/locale';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import ExternalLink from 'app/components/links/externalLink';
import Button from 'app/components/button';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import TextBlock from 'app/views/settings/components/text/textBlock';
import { IconAdd } from 'app/icons';
import AsyncView from 'app/views/asyncView';
import Add from './modals/add';
import Edit from './modals/edit';
import EmptyState from './emptyState';
import List from './list';
var RELAY_DOCS_LINK = 'https://getsentry.github.io/relay/';
var RelayWrapper = /** @class */ (function (_super) {
    __extends(RelayWrapper, _super);
    function RelayWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (publicKey) { return function () { return __awaiter(_this, void 0, void 0, function () {
            var relays, trustedRelays, response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        relays = this.state.relays;
                        trustedRelays = relays
                            .filter(function (relay) { return relay.publicKey !== publicKey; })
                            .map(function (relay) { return omit(relay, ['created', 'lastModified']); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.organization.slug + "/", {
                                method: 'PUT',
                                data: { trustedRelays: trustedRelays },
                            })];
                    case 2:
                        response = _b.sent();
                        addSuccessMessage(t('Successfully deleted Relay public key'));
                        this.setRelays(response.trustedRelays);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('An unknown error occurred while deleting Relay public key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        _this.handleOpenEditDialog = function (publicKey) { return function () {
            var editRelay = _this.state.relays.find(function (relay) { return relay.publicKey === publicKey; });
            if (!editRelay) {
                return;
            }
            openModal(function (modalProps) { return (<Edit {...modalProps} savedRelays={_this.state.relays} api={_this.api} orgSlug={_this.props.organization.slug} relay={editRelay} onSubmitSuccess={function (response) {
                _this.successfullySaved(response, t('Successfully updated Relay public key'));
            }}/>); });
        }; };
        _this.handleOpenAddDialog = function () {
            openModal(function (modalProps) { return (<Add {...modalProps} savedRelays={_this.state.relays} api={_this.api} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                _this.successfullySaved(response, t('Successfully added Relay public key'));
            }}/>); });
        };
        _this.handleRefresh = function () {
            // Fetch fresh activities
            _this.fetchData();
        };
        return _this;
    }
    RelayWrapper.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!isEqual(prevState.relays, this.state.relays)) {
            // Fetch fresh activities
            this.fetchData();
            updateOrganization(__assign(__assign({}, prevProps.organization), { trustedRelays: this.state.relays }));
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    RelayWrapper.prototype.getTitle = function () {
        return t('Relay');
    };
    RelayWrapper.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { relays: this.props.organization.trustedRelays });
    };
    RelayWrapper.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [['relayActivities', "/organizations/" + organization.slug + "/relay_usage/"]];
    };
    RelayWrapper.prototype.setRelays = function (trustedRelays) {
        this.setState({ relays: trustedRelays });
    };
    RelayWrapper.prototype.successfullySaved = function (response, successMessage) {
        addSuccessMessage(successMessage);
        this.setRelays(response.trustedRelays);
    };
    RelayWrapper.prototype.renderContent = function () {
        var _a = this.state, relays = _a.relays, relayActivities = _a.relayActivities, loading = _a.loading;
        if (loading) {
            return this.renderLoading();
        }
        if (!relays.length) {
            return <EmptyState />;
        }
        return (<List relays={relays} relayActivities={relayActivities} onEdit={this.handleOpenEditDialog} onRefresh={this.handleRefresh} onDelete={this.handleDelete}/>);
    };
    RelayWrapper.prototype.renderBody = function () {
        return (<React.Fragment>
        <SettingsPageHeader title={t('Relay')} action={<Button priority="primary" size="small" icon={<IconAdd size="xs" isCircled/>} onClick={this.handleOpenAddDialog}>
              {t('Register Key')}
            </Button>}/>
        <StyledTextBlock>
          {t('Sentry Relay offers enterprise-grade data security by providing a standalone service that acts as a middle layer between your application and sentry.io.')}
        </StyledTextBlock>
        <TextBlock>
          {tct("Go to [link:Relay Documentation] for setup and details.", {
            link: <ExternalLink href={RELAY_DOCS_LINK}/>,
        })}
        </TextBlock>
        {this.renderContent()}
      </React.Fragment>);
    };
    return RelayWrapper;
}(AsyncView));
export default RelayWrapper;
var StyledTextBlock = styled(TextBlock)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-width: 600px;\n"], ["\n  max-width: 600px;\n"])));
var templateObject_1;
//# sourceMappingURL=relayWrapper.jsx.map