import { t } from 'app/locale';
import { defined } from 'app/utils';
import { OperatingSystemKnownDataType } from './types';
function getOperatingSystemKnownDataDetails(data, type) {
    switch (type) {
        case OperatingSystemKnownDataType.NAME:
            return {
                subject: t('Name'),
                value: data.name,
            };
        case OperatingSystemKnownDataType.VERSION:
            return {
                subject: t('Version'),
                value: "" + data.version + (data.build ? "(" + data.build + ")" : ''),
            };
        case OperatingSystemKnownDataType.KERNEL_VERSION:
            return {
                subject: t('Kernel Version'),
                value: data.kernel_version,
            };
        case OperatingSystemKnownDataType.ROOTED:
            return {
                subject: t('Rooted'),
                value: defined(data.rooted) ? (data.rooted ? 'yes' : 'no') : null,
            };
        default:
            return {
                subject: type,
                value: data[type] || null,
            };
    }
}
export default getOperatingSystemKnownDataDetails;
//# sourceMappingURL=getOperatingSystemKnownDataDetails.jsx.map