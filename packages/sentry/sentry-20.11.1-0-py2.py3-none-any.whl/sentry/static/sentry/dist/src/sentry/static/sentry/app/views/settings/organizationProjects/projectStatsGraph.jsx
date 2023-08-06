import React from 'react';
import LazyLoad from 'react-lazyload';
import { t } from 'app/locale';
import MiniBarChart from 'app/components/charts/miniBarChart';
var ProjectStatsGraph = function (_a) {
    var project = _a.project, stats = _a.stats;
    stats = stats || project.stats || [];
    var series = [
        {
            seriesName: t('Events'),
            data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        },
    ];
    return (<React.Fragment>
      {series && (<LazyLoad height={25} debounce={50}>
          <MiniBarChart isGroupedByDate showTimeInTooltip series={series} height={25}/>
        </LazyLoad>)}
    </React.Fragment>);
};
export default ProjectStatsGraph;
//# sourceMappingURL=projectStatsGraph.jsx.map