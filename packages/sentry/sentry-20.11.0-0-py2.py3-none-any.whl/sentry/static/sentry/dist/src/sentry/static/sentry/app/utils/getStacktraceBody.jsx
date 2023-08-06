import rawStacktraceContent from 'app/components/events/interfaces/rawStacktraceContent';
export default function getStacktraceBody(event) {
    var _a;
    if (!event || !event.entries) {
        return [];
    }
    // TODO(billyvg): This only accounts for the first exception, will need navigation to be able to
    // diff multiple exceptions
    //
    // See: https://github.com/getsentry/sentry/issues/6055
    var exc = event.entries.find(function (_a) {
        var type = _a.type;
        return type === 'exception';
    });
    if (!exc) {
        // Look for a message if not an exception
        var msg = event.entries.find(function (_a) {
            var type = _a.type;
            return type === 'message';
        });
        if (!msg) {
            return [];
        }
        return ((_a = msg === null || msg === void 0 ? void 0 : msg.data) === null || _a === void 0 ? void 0 : _a.formatted) && [msg.data.formatted];
    }
    if (!exc.data) {
        return [];
    }
    // TODO(ts): This should be verified when EntryData has the correct type
    return exc.data.values
        .filter(function (value) { return !!value.stacktrace; })
        .map(function (value) { return rawStacktraceContent(value.stacktrace, event.platform, value); })
        .reduce(function (acc, value) { return acc.concat(value); }, []);
}
//# sourceMappingURL=getStacktraceBody.jsx.map