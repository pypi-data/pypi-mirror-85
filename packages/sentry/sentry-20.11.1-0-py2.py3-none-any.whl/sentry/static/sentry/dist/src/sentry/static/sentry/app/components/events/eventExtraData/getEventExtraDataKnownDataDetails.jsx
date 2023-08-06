import { t } from 'app/locale';
import { EventExtraDataType } from './types';
var getEventExtraDataKnownDataDetails = function (data, key) {
    switch (key) {
        case EventExtraDataType.CRASHED_PROCESS:
            return {
                subject: t('Crashed Process'),
                value: data[key],
            };
        default:
            return {
                subject: key,
                value: data[key],
            };
    }
};
export default getEventExtraDataKnownDataDetails;
//# sourceMappingURL=getEventExtraDataKnownDataDetails.jsx.map