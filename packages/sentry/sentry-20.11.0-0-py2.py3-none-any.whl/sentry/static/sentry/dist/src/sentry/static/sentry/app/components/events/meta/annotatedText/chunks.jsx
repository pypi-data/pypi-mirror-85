import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Chunk from './chunk';
var Chunks = function (_a) {
    var chunks = _a.chunks;
    return (<ChunksSpan>
    {chunks.map(function (chunk, key) { return React.cloneElement(<Chunk chunk={chunk}/>, { key: key }); })}
  </ChunksSpan>);
};
export default Chunks;
var ChunksSpan = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  span {\n    display: inline;\n  }\n"], ["\n  span {\n    display: inline;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=chunks.jsx.map