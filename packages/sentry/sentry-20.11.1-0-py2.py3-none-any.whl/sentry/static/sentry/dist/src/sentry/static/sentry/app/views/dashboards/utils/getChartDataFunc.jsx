import { getChartDataForWidget, getChartDataByDay } from 'app/views/discover/result/utils';
import { isTimeSeries } from './isTimeSeries';
import { WIDGET_DISPLAY } from '../constants';
/**
 * Get data function based on widget properties
 */
export function getChartDataFunc(_a) {
    var queries = _a.queries, type = _a.type, fieldLabelMap = _a.fieldLabelMap;
    if (queries.discover.some(isTimeSeries)) {
        return [
            getChartDataByDay,
            [
                {
                    allSeries: true,
                    fieldLabelMap: fieldLabelMap,
                },
            ],
        ];
    }
    return [
        getChartDataForWidget,
        [
            {
                includePercentages: type === WIDGET_DISPLAY.TABLE,
            },
        ],
    ];
}
//# sourceMappingURL=getChartDataFunc.jsx.map