import { __extends } from "tslib";
import React from 'react';
import withApi from 'app/utils/withApi';
import { getInterval } from 'app/components/charts/utils';
import LoadingPanel from 'app/components/charts/loadingPanel';
import QuestionTooltip from 'app/components/questionTooltip';
import getDynamicText from 'app/utils/getDynamicText';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel } from 'app/components/panels';
import EventsRequest from 'app/components/charts/eventsRequest';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { IconWarning } from 'app/icons';
import { getAxisOptions } from '../data';
import { HeaderContainer, HeaderTitle, ErrorPanel } from '../styles';
import Chart from './chart';
import Footer from './footer';
var Container = /** @class */ (function (_super) {
    __extends(Container, _super);
    function Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Container.prototype.getChartParameters = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var options = getAxisOptions(organization);
        var left = options.find(function (opt) { return opt.value === location.query.left; }) || options[0];
        var right = options.find(function (opt) { return opt.value === location.query.right; }) || options[1];
        return [left, right];
    };
    Container.prototype.render = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventView = _a.eventView, router = _a.router;
        // construct request parameters for fetching chart data
        var globalSelection = eventView.getGlobalSelection();
        var start = globalSelection.datetime.start
            ? getUtcToLocalDateObject(globalSelection.datetime.start)
            : undefined;
        var end = globalSelection.datetime.end
            ? getUtcToLocalDateObject(globalSelection.datetime.end)
            : undefined;
        var utc = getParams(location.query).utc;
        var axisOptions = this.getChartParameters();
        return (<Panel>
        <EventsRequest organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} start={start} end={end} interval={getInterval({
            start: start || null,
            end: end || null,
            period: globalSelection.datetime.period,
        }, true)} showLoading={false} query={eventView.getEventsAPIPayload(location).query} includePrevious={false} yAxis={axisOptions.map(function (opt) { return opt.value; })}>
          {function (_a) {
            var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, results = _a.results;
            if (errored) {
                return (<ErrorPanel>
                  <IconWarning color="gray300" size="lg"/>
                </ErrorPanel>);
            }
            return (<React.Fragment>
                <HeaderContainer>
                  {axisOptions.map(function (option, i) { return (<div key={option.label + ":" + i}>
                      <HeaderTitle>
                        {option.label}
                        <QuestionTooltip position="top" size="sm" title={option.tooltip}/>
                      </HeaderTitle>
                    </div>); })}
                </HeaderContainer>
                {results ? (getDynamicText({
                value: (<Chart data={results} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} utc={utc === 'true'} projects={globalSelection.projects} environments={globalSelection.environments}/>),
                fixed: 'apdex and throughput charts',
            })) : (<LoadingPanel data-test-id="events-request-loading"/>)}
              </React.Fragment>);
        }}
        </EventsRequest>
        <Footer api={api} leftAxis={axisOptions[0].value} rightAxis={axisOptions[1].value} organization={organization} eventView={eventView} location={location}/>
      </Panel>);
    };
    return Container;
}(React.Component));
export default withApi(Container);
//# sourceMappingURL=index.jsx.map