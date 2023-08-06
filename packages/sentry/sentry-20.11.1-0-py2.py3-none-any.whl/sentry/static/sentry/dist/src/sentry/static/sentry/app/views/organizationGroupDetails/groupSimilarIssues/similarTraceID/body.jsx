import React from 'react';
import moment from 'moment-timezone';
import LoadingIndicator from 'app/components/loadingIndicator';
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import EventView from 'app/utils/discover/eventView';
import { t } from 'app/locale';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { Panel, PanelBody } from 'app/components/panels';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import List from './list';
var Body = function (_a) {
    var traceID = _a.traceID, organization = _a.organization, event = _a.event, location = _a.location;
    if (!traceID) {
        return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {t('This event has no trace context, therefore it was not possible to fetch similar issues by trace ID.')}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
    }
    var orgSlug = organization.slug;
    var orgFeatures = organization.features;
    var dateCreated = moment(event.dateCreated).valueOf() / 1000;
    var _b = getTraceDateTimeRange({ start: dateCreated, end: dateCreated }), start = _b.start, end = _b.end;
    var eventView = EventView.fromSavedQuery({
        id: undefined,
        name: "Issues with Trace ID " + traceID,
        fields: ['issue.id'],
        orderby: '-timestamp',
        query: "trace:" + traceID + " !event.type:transaction !id:" + event.id + " ",
        projects: orgFeatures.includes('global-views')
            ? [ALL_ACCESS_PROJECTS]
            : [Number(event.projectID)],
        version: 2,
        start: start,
        end: end,
    });
    return (<DiscoverQuery eventView={eventView} location={location} orgSlug={orgSlug} limit={5}>
      {function (data) {
        var _a;
        if (data.isLoading) {
            return <LoadingIndicator />;
        }
        var issues = ((_a = data === null || data === void 0 ? void 0 : data.tableData) === null || _a === void 0 ? void 0 : _a.data) || [];
        return (<List issues={issues} pageLinks={data.pageLinks} traceID={traceID} orgSlug={orgSlug} location={location} period={{ start: start, end: end }}/>);
    }}
    </DiscoverQuery>);
};
export default Body;
//# sourceMappingURL=body.jsx.map