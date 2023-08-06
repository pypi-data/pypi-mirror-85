import React from 'react';
var SpanEntryContext = React.createContext({
    getViewChildTransactionTarget: function () { return undefined; },
});
export var Provider = SpanEntryContext.Provider;
export var Consumer = SpanEntryContext.Consumer;
//# sourceMappingURL=context.jsx.map