import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import moment from 'moment';
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
import { PageHeader } from 'app/styles/organization';
import { t } from 'app/locale';
import Count from 'app/components/count';
import Duration from 'app/components/duration';
import LoadingError from 'app/components/loadingError';
import MenuItem from 'app/components/menuItem';
import PageHeading from 'app/components/pageHeading';
import Placeholder from 'app/components/placeholder';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import Projects from 'app/utils/projects';
import SubscribeButton from 'app/components/subscribeButton';
import getDynamicText from 'app/utils/getDynamicText';
import space from 'app/styles/space';
import { IconCheckmark } from 'app/icons';
import Breadcrumbs from 'app/components/breadcrumbs';
import { Dataset } from 'app/views/settings/incidentRules/types';
import DropdownControl from 'app/components/dropdownControl';
import { use24Hours } from 'app/utils/dates';
import { isOpen } from '../utils';
import Status from '../status';
var DetailsHeader = /** @class */ (function (_super) {
    __extends(DetailsHeader, _super);
    function DetailsHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsHeader.prototype.renderStatus = function () {
        var _a = this.props, incident = _a.incident, onStatusChange = _a.onStatusChange;
        var isIncidentOpen = incident && isOpen(incident);
        var statusLabel = incident ? <StyledStatus incident={incident}/> : null;
        return (<DropdownControl data-test-id="status-dropdown" label={statusLabel} alignRight blendWithActor={false} buttonProps={{
            size: 'small',
            disabled: !incident || !isIncidentOpen,
            hideBottomBorder: false,
        }}>
        <StatusMenuItem isActive>
          {incident && <Status disableIconColor incident={incident}/>}
        </StatusMenuItem>
        <StatusMenuItem onSelect={onStatusChange}>
          <IconCheckmark color="green300"/>
          {t('Resolved')}
        </StatusMenuItem>
      </DropdownControl>);
    };
    DetailsHeader.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, hasIncidentDetailsError = _d.hasIncidentDetailsError, incident = _d.incident, params = _d.params, stats = _d.stats, onSubscriptionChange = _d.onSubscriptionChange;
        var isIncidentReady = !!incident && !hasIncidentDetailsError;
        // ex - Wed, May 27, 2020 11:09 AM
        var dateFormat = use24Hours() ? 'ddd, MMM D, YYYY HH:mm' : 'llll';
        var dateStarted = incident && moment(new Date(incident.dateStarted)).format(dateFormat);
        var duration = incident &&
            moment(incident.dateClosed ? new Date(incident.dateClosed) : new Date()).diff(moment(new Date(incident.dateStarted)), 'seconds');
        var isErrorDataset = ((_a = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _a === void 0 ? void 0 : _a.dataset) === Dataset.ERRORS;
        var environmentLabel = (_c = (_b = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _b === void 0 ? void 0 : _b.environment) !== null && _c !== void 0 ? _c : t('All Environments');
        var project = incident && incident.projects && incident.projects[0];
        return (<Header>
        <BreadCrumbBar>
          <AlertBreadcrumbs crumbs={[
            { label: t('Alerts'), to: "/organizations/" + params.orgId + "/alerts/" },
            { label: incident && "#" + incident.id },
        ]}/>
          <Controls>
            <SubscribeButton disabled={!isIncidentReady} isSubscribed={incident === null || incident === void 0 ? void 0 : incident.isSubscribed} onClick={onSubscriptionChange} size="small"/>
            {this.renderStatus()}
          </Controls>
        </BreadCrumbBar>
        <Details columns={isErrorDataset ? 5 : 3}>
          <div>
            <IncidentTitle data-test-id="incident-title" loading={!isIncidentReady}>
              {incident && !hasIncidentDetailsError ? incident.title : 'Loading'}
            </IncidentTitle>
            <IncidentSubTitle loading={!isIncidentReady}>
              {t('Triggered: ')}
              {dateStarted}
            </IncidentSubTitle>
          </div>

          {hasIncidentDetailsError ? (<StyledLoadingError />) : (<GroupedHeaderItems columns={isErrorDataset ? 5 : 3}>
              <ItemTitle>{t('Environment')}</ItemTitle>
              <ItemTitle>{t('Project')}</ItemTitle>
              {isErrorDataset && <ItemTitle>{t('Users affected')}</ItemTitle>}
              {isErrorDataset && <ItemTitle>{t('Total events')}</ItemTitle>}
              <ItemTitle>{t('Active For')}</ItemTitle>
              <ItemValue>{environmentLabel}</ItemValue>
              <ItemValue>
                {project ? (<Projects slugs={[project]} orgId={params.orgId}>
                    {function (_a) {
            var projects = _a.projects;
            return (projects === null || projects === void 0 ? void 0 : projects.length) && (<ProjectBadge avatarSize={18} project={projects[0]}/>);
        }}
                  </Projects>) : (<Placeholder height="25px"/>)}
              </ItemValue>
              {isErrorDataset && (<ItemValue>
                  {stats ? (<Count value={stats.uniqueUsers}/>) : (<Placeholder height="25px"/>)}
                </ItemValue>)}
              {isErrorDataset && (<ItemValue>
                  {stats ? (<Count value={stats.totalEvents}/>) : (<Placeholder height="25px"/>)}
                </ItemValue>)}
              <ItemValue>
                {incident ? (<Duration seconds={getDynamicText({ value: duration || 0, fixed: 1200 })}/>) : (<Placeholder height="25px"/>)}
              </ItemValue>
            </GroupedHeaderItems>)}
        </Details>
      </Header>);
    };
    return DetailsHeader;
}(React.Component));
export default DetailsHeader;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
var BreadCrumbBar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"], ["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"])), space(2), space(4), space(1));
var AlertBreadcrumbs = styled(Breadcrumbs)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"], ["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var Controls = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space(1));
var Details = styled(PageHeader, {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'columns'; },
})(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"])), space(1.5), space(4), space(2), space(3), function (p) { return p.theme.breakpoints[p.columns === 3 ? 1 : 2]; });
var StyledLoadingError = styled(LoadingError)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n\n  &.alert.alert-block {\n    margin: 0 20px;\n  }\n"], ["\n  flex: 1;\n\n  &.alert.alert-block {\n    margin: 0 20px;\n  }\n"])));
var GroupedHeaderItems = styled('div', {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'columns'; },
})(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", " ", ";\n  text-align: right;\n  margin-top: ", ";\n\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", " ", ";\n  text-align: right;\n  margin-top: ", ";\n\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"])), function (p) { return p.columns; }, space(1), space(4), space(1), function (p) { return p.theme.breakpoints[p.columns === 3 ? 1 : 2]; });
var ItemTitle = styled('h6')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: 0;\n  text-transform: uppercase;\n  color: ", ";\n  letter-spacing: 0.1px;\n"], ["\n  font-size: ", ";\n  margin-bottom: 0;\n  text-transform: uppercase;\n  color: ", ";\n  letter-spacing: 0.1px;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var ItemValue = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var IncidentTitle = styled(PageHeading, {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'loading'; },
})(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  ", ";\n  line-height: 1.5;\n"], ["\n  ", ";\n  line-height: 1.5;\n"])), function (p) { return p.loading && 'opacity: 0'; });
var IncidentSubTitle = styled('div', {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'loading'; },
})(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  ", ";\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.loading && 'opacity: 0'; }, function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; });
var StyledStatus = styled(Status)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(2));
var StatusMenuItem = styled(MenuItem)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  > span {\n    padding: ", " ", ";\n    font-size: ", ";\n    font-weight: 600;\n    line-height: 1;\n    text-align: left;\n    display: grid;\n    grid-template-columns: max-content 1fr;\n    grid-gap: ", ";\n    align-items: center;\n  }\n"], ["\n  > span {\n    padding: ", " ", ";\n    font-size: ", ";\n    font-weight: 600;\n    line-height: 1;\n    text-align: left;\n    display: grid;\n    grid-template-columns: max-content 1fr;\n    grid-gap: ", ";\n    align-items: center;\n  }\n"])), space(1), space(1.5), function (p) { return p.theme.fontSizeSmall; }, space(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=header.jsx.map