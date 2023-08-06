import { __assign, __rest } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
function getMeasurementsHistogramRequestPayload(props) {
    var measurements = props.measurements, numBuckets = props.numBuckets, min = props.min, max = props.max, precision = props.precision, dataFilter = props.dataFilter, eventView = props.eventView, location = props.location;
    var baseApiPayload = {
        measurement: measurements,
        numBuckets: numBuckets,
        min: min,
        max: max,
        precision: precision,
        dataFilter: dataFilter,
    };
    var additionalApiPayload = omit(eventView.getEventsAPIPayload(location), [
        'field',
        'sort',
        'per_page',
    ]);
    var apiPayload = Object.assign(baseApiPayload, additionalApiPayload);
    return apiPayload;
}
function beforeFetch(api) {
    api.clear();
}
function afterFetch(response, props) {
    var data = response.data;
    var measurements = props.measurements;
    var histogramData = measurements.reduce(function (record, measurement) {
        record["measurements." + measurement] = [];
        return record;
    }, {});
    data === null || data === void 0 ? void 0 : data.forEach(function (row) {
        histogramData["measurements." + row.key].push({
            histogram: row.bin,
            count: row.count,
        });
    });
    return histogramData;
}
function MeasurementsHistogramQuery(props) {
    var children = props.children, measurements = props.measurements;
    if (measurements.length === 0) {
        return (<React.Fragment>
        {children({
            isLoading: false,
            error: null,
            pageLinks: null,
            histograms: {},
        })}
      </React.Fragment>);
    }
    return (<GenericDiscoverQuery route="events-measurements-histogram" getRequestPayload={getMeasurementsHistogramRequestPayload} beforeFetch={beforeFetch} afterFetch={afterFetch} {...omit(props, 'children')}>
      {function (_a) {
        var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
        return props.children(__assign({ histograms: tableData }, rest));
    }}
    </GenericDiscoverQuery>);
}
export default withApi(MeasurementsHistogramQuery);
//# sourceMappingURL=measurementsHistogramQuery.jsx.map