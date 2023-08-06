function filterContexts(event, context) {
    var _a, _b, _c;
    // if the operating system is macOS, we want to hide devices called "Mac" which don't have any additional info
    if (context.keys.includes('device')) {
        var _d = ((_a = event.contexts) === null || _a === void 0 ? void 0 : _a.device) || {}, model = _d.model, arch = _d.arch, data_id = _d.data_id;
        var os = (((_b = event.contexts) === null || _b === void 0 ? void 0 : _b.os) || ((_c = event.contexts) === null || _c === void 0 ? void 0 : _c.client_os) || {}).name;
        if (model === 'Mac' && !arch && !data_id && (os === null || os === void 0 ? void 0 : os.toLowerCase().includes('mac'))) {
            return false;
        }
    }
    return true;
}
export default filterContexts;
//# sourceMappingURL=filterContexts.jsx.map