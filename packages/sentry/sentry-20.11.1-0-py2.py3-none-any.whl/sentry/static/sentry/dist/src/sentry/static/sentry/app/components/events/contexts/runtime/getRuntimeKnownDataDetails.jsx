import { t } from 'app/locale';
import { RuntimeKnownDataType } from './types';
function getRuntimeKnownDataDetails(data, type) {
    switch (type) {
        case RuntimeKnownDataType.NAME:
            return {
                subject: t('Name'),
                value: data.name,
            };
        case RuntimeKnownDataType.VERSION:
            return {
                subject: t('Version'),
                value: "" + data.version + (data.build ? "(" + data.build + ")" : ''),
            };
        default:
            return {
                subject: type,
                value: data[type],
            };
    }
}
export default getRuntimeKnownDataDetails;
//# sourceMappingURL=getRuntimeKnownDataDetails.jsx.map