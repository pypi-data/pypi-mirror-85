// Consider a query a time series if
export function isTimeSeries(query) {
    var _a;
    return (_a = query === null || query === void 0 ? void 0 : query.groupby) === null || _a === void 0 ? void 0 : _a.includes('time');
}
//# sourceMappingURL=isTimeSeries.jsx.map