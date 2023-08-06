import { __assign, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import { IconInfo, IconClose, IconSiren } from 'app/icons';
import Button from 'app/components/button';
import Alert from 'app/components/alert';
import Access from 'app/components/acl/access';
import { explodeFieldString, AGGREGATIONS } from 'app/utils/discover/fields';
import { errorFieldConfig, transactionFieldConfig, } from 'app/views/settings/incidentRules/constants';
import Link from 'app/components/links/link';
/**
 * Displays messages to the user on what needs to change in their query
 */
function IncompatibleQueryAlert(_a) {
    var incompatibleQuery = _a.incompatibleQuery, eventView = _a.eventView, orgId = _a.orgId, onClose = _a.onClose;
    var hasProjectError = incompatibleQuery.hasProjectError, hasEnvironmentError = incompatibleQuery.hasEnvironmentError, hasEventTypeError = incompatibleQuery.hasEventTypeError, hasYAxisError = incompatibleQuery.hasYAxisError;
    var totalErrors = Object.values(incompatibleQuery).filter(function (val) { return val === true; }).length;
    var eventTypeError = eventView.clone();
    eventTypeError.query += ' event.type:error';
    var eventTypeTransaction = eventView.clone();
    eventTypeTransaction.query += ' event.type:transaction';
    var pathname = "/organizations/" + orgId + "/discover/results/";
    return (<StyledAlert type="warning" icon={<IconInfo color="yellow300" size="sm"/>}>
      {totalErrors === 1 && (<React.Fragment>
          {hasProjectError &&
        t('An alert can use data from only one Project. Select one and try again.')}
          {hasEnvironmentError &&
        t('An alert supports data from a single Environment or All Environments. Pick one try again.')}
          {hasEventTypeError &&
        tct('An alert needs a filter of [error:event.type:error] or [transaction:event.type:transaction]. Use one of these and try again.', {
            error: (<Link to={{
                pathname: pathname,
                query: eventTypeError.generateQueryStringObject(),
            }}/>),
            transaction: (<Link to={{
                pathname: pathname,
                query: eventTypeTransaction.generateQueryStringObject(),
            }}/>),
        })}
          {hasYAxisError &&
        tct('An alert can’t use the metric [yAxis] just yet. Select another metric and try again.', {
            yAxis: <StyledCode>{eventView.getYAxis()}</StyledCode>,
        })}
        </React.Fragment>)}
      {totalErrors > 1 && (<React.Fragment>
          {t('Yikes! That button didn’t work. Please fix the following problems:')}
          <StyledUnorderedList>
            {hasProjectError && <li>{t('Select one Project.')}</li>}
            {hasEnvironmentError && (<li>{t('Select a single Environment or All Environments.')}</li>)}
            {hasEventTypeError && (<li>
                {tct('Use the filter [error:event.type:error] or [transaction:event.type:transaction].', {
        error: (<Link to={{
            pathname: pathname,
            query: eventTypeError.generateQueryStringObject(),
        }}/>),
        transaction: (<Link to={{
            pathname: pathname,
            query: eventTypeTransaction.generateQueryStringObject(),
        }}/>),
    })}
              </li>)}
            {hasYAxisError && (<li>
                {tct('An alert can’t use the metric [yAxis] just yet. Select another metric and try again.', {
        yAxis: <StyledCode>{eventView.getYAxis()}</StyledCode>,
    })}
              </li>)}
          </StyledUnorderedList>
        </React.Fragment>)}
      <StyledCloseButton icon={<IconClose color="yellow300" size="sm" isCircled/>} aria-label={t('Close')} size="zero" onClick={onClose} borderless/>
    </StyledAlert>);
}
function incompatibleYAxis(eventView) {
    var _a;
    var column = explodeFieldString(eventView.getYAxis());
    if (column.kind === 'field') {
        return true;
    }
    var eventTypeMatch = eventView.query.match(/event\.type:(transaction|error)/);
    if (!eventTypeMatch) {
        return false;
    }
    var dataset = eventTypeMatch[1];
    var yAxisConfig = dataset === 'error' ? errorFieldConfig : transactionFieldConfig;
    var invalidFunction = !yAxisConfig.aggregations.includes(column.function[0]);
    // Allow empty parameters, allow all numeric parameters - eg. apdex(300)
    var aggregation = AGGREGATIONS[column.function[0]];
    if (!aggregation) {
        return false;
    }
    var isNumericParameter = aggregation.parameters.some(function (param) { return param.kind === 'value' && param.dataType === 'number'; });
    // There are other measurements possible, but for the time being, only allow alerting
    // on the predefined set of measurements for alerts.
    var allowedParameters = __spread([
        ''
    ], yAxisConfig.fields, ((_a = yAxisConfig.measurementKeys) !== null && _a !== void 0 ? _a : []));
    var invalidParameter = !isNumericParameter && !allowedParameters.includes(column.function[1]);
    return invalidFunction || invalidParameter;
}
/**
 * Provide a button that can create an alert from an event view.
 * Emits incompatible query issues on click
 */
function CreateAlertButton(_a) {
    var projects = _a.projects, eventView = _a.eventView, organization = _a.organization, referrer = _a.referrer, onIncompatibleQuery = _a.onIncompatibleQuery, onSuccess = _a.onSuccess, buttonProps = __rest(_a, ["projects", "eventView", "organization", "referrer", "onIncompatibleQuery", "onSuccess"]);
    // Must have exactly one project selected and not -1 (all projects)
    var hasProjectError = eventView.project.length !== 1 || eventView.project[0] === -1;
    // Must have one or zero environments
    var hasEnvironmentError = eventView.environment.length > 1;
    // Must have event.type of error or transaction
    var hasEventTypeError = !eventView.query.includes('event.type:error') &&
        !eventView.query.includes('event.type:transaction');
    // yAxis must be a function and enabled on alerts
    var hasYAxisError = incompatibleYAxis(eventView);
    var errors = {
        hasProjectError: hasProjectError,
        hasEnvironmentError: hasEnvironmentError,
        hasEventTypeError: hasEventTypeError,
        hasYAxisError: hasYAxisError,
    };
    var project = projects.find(function (p) { return p.id === "" + eventView.project[0]; });
    var hasErrors = Object.values(errors).some(function (x) { return x; });
    var to = hasErrors
        ? undefined
        : {
            pathname: "/organizations/" + organization.slug + "/alerts/" + (project === null || project === void 0 ? void 0 : project.slug) + "/new/",
            query: __assign(__assign({}, eventView.generateQueryStringObject()), { createFromDiscover: true, referrer: referrer }),
        };
    var handleClick = function (event) {
        if (hasErrors) {
            event.preventDefault();
            onIncompatibleQuery(function (onAlertClose) { return (<IncompatibleQueryAlert incompatibleQuery={errors} eventView={eventView} orgId={organization.slug} onClose={onAlertClose}/>); }, errors);
            return;
        }
        onSuccess();
    };
    return (<Access organization={organization} access={['project:write']}>
      {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Button type="button" disabled={!hasAccess} title={!hasAccess
            ? t('Users with admin permission or higher can create alert rules.')
            : undefined} icon={<IconSiren />} to={to} onClick={handleClick} {...buttonProps}>
          {t('Create alert')}
        </Button>);
    }}
    </Access>);
}
export default CreateAlertButton;
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: 0;\n"], ["\n  color: ", ";\n  margin-bottom: 0;\n"])), function (p) { return p.theme.textColor; });
var StyledUnorderedList = styled('ul')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var StyledCode = styled('code')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: transparent;\n  padding: 0;\n"], ["\n  background-color: transparent;\n  padding: 0;\n"])));
var StyledCloseButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 3px;\n  right: 0;\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"], ["\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 3px;\n  right: 0;\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=createAlertButton.jsx.map