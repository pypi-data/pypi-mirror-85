import React from 'react';
import Tooltip from 'app/components/tooltip';
import { getTooltipText } from './utils';
import Redaction from './redaction';
var Chunk = function (_a) {
    var chunk = _a.chunk;
    if (chunk.type === 'redaction') {
        var title = getTooltipText({ rule_id: chunk.rule_id, remark: chunk.remark });
        return (<Tooltip title={title}>
        <Redaction>{chunk.text}</Redaction>
      </Tooltip>);
    }
    return <span>{chunk.text}</span>;
};
export default Chunk;
//# sourceMappingURL=chunk.jsx.map