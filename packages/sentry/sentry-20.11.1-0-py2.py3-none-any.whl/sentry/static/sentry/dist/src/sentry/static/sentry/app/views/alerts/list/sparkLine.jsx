import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Placeholder from 'app/components/placeholder';
import theme from 'app/utils/theme';
// Height of sparkline
var SPARKLINE_HEIGHT = 38;
var Sparklines = React.lazy(function () { return import(/* webpackChunkName: "Sparklines" */ 'app/components/sparklines'); });
var SparklinesLine = React.lazy(function () { return import(/* webpackChunkName: "SparklinesLine" */ 'app/components/sparklines/line'); });
var SparkLine = /** @class */ (function (_super) {
    __extends(SparkLine, _super);
    function SparkLine() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SparkLine.prototype.render = function () {
        var _a = this.props, className = _a.className, error = _a.error, eventStats = _a.eventStats;
        if (error) {
            return <SparklineError error={error}/>;
        }
        if (!eventStats) {
            return <SparkLinePlaceholder />;
        }
        var data = eventStats.data.map(function (_a) {
            var _b = __read(_a, 2), value = _b[1];
            return value && Array.isArray(value) && value.length ? value[0].count || 0 : 0;
        });
        return (<React.Suspense fallback={<SparkLinePlaceholder />}>
        <div data-test-id="incident-sparkline" className={className}>
          <Sparklines data={data} width={100} height={32}>
            <SparklinesLine style={{ stroke: theme.gray300, fill: 'none', strokeWidth: 2 }}/>
          </Sparklines>
        </div>
      </React.Suspense>);
    };
    return SparkLine;
}(React.Component));
var StyledSparkLine = styled(SparkLine)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-shrink: 0;\n  width: 100%;\n  height: ", "px;\n"], ["\n  flex-shrink: 0;\n  width: 100%;\n  height: ", "px;\n"])), SPARKLINE_HEIGHT);
var SparkLinePlaceholder = styled(Placeholder)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: ", "px;\n"], ["\n  height: ", "px;\n"])), SPARKLINE_HEIGHT);
var SparklineError = styled(SparkLinePlaceholder)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: center;\n  line-height: 1;\n"], ["\n  align-items: center;\n  line-height: 1;\n"])));
export default StyledSparkLine;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sparkLine.jsx.map