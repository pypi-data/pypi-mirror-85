import { __rest } from "tslib";
import React from 'react';
import { IconGraphLine } from './iconGraphLine';
import { IconGraphCircle } from './iconGraphCircle';
import { IconGraphBar } from './iconGraphBar';
var IconGraph = React.forwardRef(function IconGraph(_a, ref) {
    var _b = _a.type, type = _b === void 0 ? 'line' : _b, props = __rest(_a, ["type"]);
    switch (type) {
        case 'circle':
            return <IconGraphCircle {...props} ref={ref}/>;
        case 'bar':
            return <IconGraphBar {...props} ref={ref}/>;
        default:
            return <IconGraphLine {...props} ref={ref}/>;
    }
});
IconGraph.displayName = 'IconGraph';
export { IconGraph };
//# sourceMappingURL=iconGraph.jsx.map