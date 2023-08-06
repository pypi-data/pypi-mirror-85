import { getDuration } from 'app/utils/formatters';
export function formattedValue(record, value) {
    if (record && record.type === 'duration') {
        return getDuration(value / 1000, 3);
    }
    return value.toFixed(3);
}
//# sourceMappingURL=index.jsx.map