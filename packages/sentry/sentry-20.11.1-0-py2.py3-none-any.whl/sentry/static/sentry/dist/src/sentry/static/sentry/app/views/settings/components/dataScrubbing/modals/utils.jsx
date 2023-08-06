import { fetchFromStorage, saveToStorage } from './localStorage';
import { EventIdStatus } from '../types';
import { valueSuggestions } from '../utils';
function fetchSourceGroupData() {
    var fetchedSourceGroupData = fetchFromStorage();
    if (!fetchedSourceGroupData) {
        var sourceGroupData = {
            eventId: '',
            sourceSuggestions: valueSuggestions,
        };
        saveToStorage(sourceGroupData);
        return sourceGroupData;
    }
    return fetchedSourceGroupData;
}
function saveToSourceGroupData(eventId, sourceSuggestions) {
    if (sourceSuggestions === void 0) { sourceSuggestions = valueSuggestions; }
    switch (eventId.status) {
        case EventIdStatus.LOADING:
            break;
        case EventIdStatus.LOADED:
            saveToStorage({ eventId: eventId.value, sourceSuggestions: sourceSuggestions });
            break;
        default:
            saveToStorage({ eventId: '', sourceSuggestions: sourceSuggestions });
    }
}
export { fetchSourceGroupData, saveToSourceGroupData };
//# sourceMappingURL=utils.jsx.map