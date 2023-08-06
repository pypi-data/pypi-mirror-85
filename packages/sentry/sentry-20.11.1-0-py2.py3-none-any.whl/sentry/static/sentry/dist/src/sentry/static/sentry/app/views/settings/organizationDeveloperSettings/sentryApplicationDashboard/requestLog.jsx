import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import AsyncComponent from 'app/components/asyncComponent';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import DateTime from 'app/components/dateTime';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import DropdownButton from 'app/components/dropdownButton';
import Tag from 'app/components/tagDeprecated';
import ExternalLink from 'app/components/links/externalLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import Checkbox from 'app/components/checkbox';
import Button from 'app/components/button';
import space from 'app/styles/space';
import { IconChevron, IconFlag, IconOpen } from 'app/icons';
import { t } from 'app/locale';
var ALL_EVENTS = t('All Events');
var MAX_PER_PAGE = 10;
var componentHasSelectUri = function (issueLinkComponent) {
    var hasSelectUri = function (fields) {
        return fields.some(function (field) { return field.type === 'select' && 'uri' in field; });
    };
    var createHasSelectUri = hasSelectUri(issueLinkComponent.create.required_fields) ||
        hasSelectUri(issueLinkComponent.create.optional_fields || []);
    var linkHasSelectUri = hasSelectUri(issueLinkComponent.link.required_fields) ||
        hasSelectUri(issueLinkComponent.link.optional_fields || []);
    return createHasSelectUri || linkHasSelectUri;
};
var getEventTypes = memoize(function (app) {
    // TODO(nola): ideally this would be kept in sync with EXTENDED_VALID_EVENTS on the backend
    var issueLinkEvents = [];
    var issueLinkComponent = (app.schema.elements || []).find(function (element) { return element.type === 'issue-link'; });
    if (issueLinkComponent) {
        issueLinkEvents = ['external_issue.created', 'external_issue.linked'];
        if (componentHasSelectUri(issueLinkComponent)) {
            issueLinkEvents.push('select_options.requested');
        }
    }
    var events = __spread([
        ALL_EVENTS
    ], (app.status !== 'internal'
        ? ['installation.created', 'installation.deleted']
        : []), (app.events.includes('error') ? ['error.created'] : []), (app.events.includes('issue')
        ? ['issue.created', 'issue.resolved', 'issue.ignored', 'issue.assigned']
        : []), (app.isAlertable ? ['event_alert.triggered'] : []), issueLinkEvents);
    return events;
});
var ResponseCode = function (_a) {
    var code = _a.code;
    var priority = 'error';
    if (code <= 399 && code >= 300) {
        priority = 'warning';
    }
    else if (code <= 299 && code >= 100) {
        priority = 'success';
    }
    return (<div>
      <Tag priority={priority}>{code === 0 ? 'timeout' : code}</Tag>
    </div>);
};
var TimestampLink = function (_a) {
    var date = _a.date, link = _a.link;
    return link ? (<ExternalLink href={link}>
      <DateTime date={date}/>
      <StyledIconOpen size="12px"/>
    </ExternalLink>) : (<DateTime date={date}/>);
};
var RequestLog = /** @class */ (function (_super) {
    __extends(RequestLog, _super);
    function RequestLog() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.handleChangeEventType = function (eventType) {
            _this.setState({
                eventType: eventType,
                currentPage: 0,
            }, _this.remountComponent);
        };
        _this.handleChangeErrorsOnly = function () {
            _this.setState({
                errorsOnly: !_this.state.errorsOnly,
                currentPage: 0,
            }, _this.remountComponent);
        };
        _this.handleNextPage = function () {
            _this.setState({
                currentPage: _this.state.currentPage + 1,
            });
        };
        _this.handlePrevPage = function () {
            _this.setState({
                currentPage: _this.state.currentPage - 1,
            });
        };
        return _this;
    }
    Object.defineProperty(RequestLog.prototype, "hasNextPage", {
        get: function () {
            return (this.state.currentPage + 1) * MAX_PER_PAGE < this.state.requests.length;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RequestLog.prototype, "hasPrevPage", {
        get: function () {
            return this.state.currentPage > 0;
        },
        enumerable: false,
        configurable: true
    });
    RequestLog.prototype.getEndpoints = function () {
        var slug = this.props.app.slug;
        var query = {};
        if (this.state) {
            if (this.state.eventType !== ALL_EVENTS) {
                query.eventType = this.state.eventType;
            }
            if (this.state.errorsOnly) {
                query.errorsOnly = true;
            }
        }
        return [['requests', "/sentry-apps/" + slug + "/requests/", { query: query }]];
    };
    RequestLog.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { requests: [], eventType: ALL_EVENTS, errorsOnly: false, currentPage: 0 });
    };
    RequestLog.prototype.renderLoading = function () {
        return this.renderBody();
    };
    RequestLog.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, requests = _a.requests, eventType = _a.eventType, errorsOnly = _a.errorsOnly, currentPage = _a.currentPage;
        var app = this.props.app;
        var currentRequests = requests.slice(currentPage * MAX_PER_PAGE, (currentPage + 1) * MAX_PER_PAGE);
        return (<React.Fragment>
        <h5>{t('Request Log')}</h5>

        <div>
          <p>
            {t('This log shows the status of any outgoing webhook requests from Sentry to your integration.')}
          </p>

          <RequestLogFilters>
            <DropdownControl label={eventType} menuWidth="220px" button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
                  {eventType}
                </StyledDropdownButton>);
        }}>
              {getEventTypes(app).map(function (type) { return (<DropdownItem key={type} onSelect={_this.handleChangeEventType} eventKey={type} isActive={eventType === type}>
                  {type}
                </DropdownItem>); })}
            </DropdownControl>

            <StyledErrorsOnlyButton onClick={this.handleChangeErrorsOnly}>
              <ErrorsOnlyCheckbox>
                <Checkbox checked={errorsOnly} onChange={function () { }}/>
                {t('Errors Only')}
              </ErrorsOnlyCheckbox>
            </StyledErrorsOnlyButton>
          </RequestLogFilters>
        </div>

        <Panel>
          <PanelHeader>
            <TableLayout hasOrganization={app.status !== 'internal'}>
              <div>{t('Time')}</div>
              <div>{t('Status Code')}</div>
              {app.status !== 'internal' && <div>{t('Organization')}</div>}
              <div>{t('Event Type')}</div>
              <div>{t('Webhook URL')}</div>
            </TableLayout>
          </PanelHeader>

          {!this.state.loading ? (<PanelBody>
              {currentRequests.length > 0 ? (currentRequests.map(function (request, idx) { return (<PanelItem key={idx}>
                    <TableLayout hasOrganization={app.status !== 'internal'}>
                      <TimestampLink date={request.date} link={request.errorUrl}/>
                      <ResponseCode code={request.responseCode}/>
                      {app.status !== 'internal' && (<div>
                          {request.organization ? request.organization.name : null}
                        </div>)}
                      <div>{request.eventType}</div>
                      <OverflowBox>{request.webhookUrl}</OverflowBox>
                    </TableLayout>
                  </PanelItem>); })) : (<EmptyMessage icon={<IconFlag size="xl"/>}>
                  {t('No requests found in the last 30 days.')}
                </EmptyMessage>)}
            </PanelBody>) : (<LoadingIndicator />)}
        </Panel>

        <PaginationButtons>
          <Button icon={<IconChevron direction="left" size="sm"/>} onClick={this.handlePrevPage} disabled={!this.hasPrevPage} label={t('Previous page')}/>
          <Button icon={<IconChevron direction="right" size="sm"/>} onClick={this.handleNextPage} disabled={!this.hasNextPage} label={t('Next page')}/>
        </PaginationButtons>
      </React.Fragment>);
    };
    return RequestLog;
}(AsyncComponent));
export default RequestLog;
var TableLayout = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr ", " 1fr 1fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr ", " 1fr 1fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n"])), function (p) { return (p.hasOrganization ? '1fr' : ''); }, space(1.5));
var OverflowBox = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  word-break: break-word;\n"], ["\n  word-break: break-word;\n"])));
var PaginationButtons = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n\n  > :first-child {\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n\n  > :nth-child(2) {\n    margin-left: -1px;\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n\n  > :first-child {\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n\n  > :nth-child(2) {\n    margin-left: -1px;\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n"])));
var RequestLogFilters = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding-bottom: ", ";\n"])), space(1));
var ErrorsOnlyCheckbox = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  input {\n    margin: 0 ", " 0 0;\n  }\n\n  display: flex;\n  align-items: center;\n"], ["\n  input {\n    margin: 0 ", " 0 0;\n  }\n\n  display: flex;\n  align-items: center;\n"])), space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  z-index: ", ";\n  white-space: nowrap;\n\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  z-index: ", ";\n  white-space: nowrap;\n\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"])), function (p) { return p.theme.zIndex.header - 1; });
var StyledErrorsOnlyButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-left: -1px;\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"], ["\n  margin-left: -1px;\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"])));
var StyledIconOpen = styled(IconOpen)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-left: 6px;\n  color: ", ";\n"], ["\n  margin-left: 6px;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=requestLog.jsx.map