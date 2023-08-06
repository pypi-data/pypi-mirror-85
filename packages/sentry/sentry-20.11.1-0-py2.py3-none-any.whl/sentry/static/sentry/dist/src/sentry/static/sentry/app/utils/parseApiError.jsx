export default function parseApiError(resp) {
    var detail = ((resp && resp.responseJSON) || {}).detail;
    // return immediately if string
    if (typeof detail === 'string') {
        return detail;
    }
    if (detail && detail.message) {
        return detail.message;
    }
    return 'Unknown API Error';
}
//# sourceMappingURL=parseApiError.jsx.map