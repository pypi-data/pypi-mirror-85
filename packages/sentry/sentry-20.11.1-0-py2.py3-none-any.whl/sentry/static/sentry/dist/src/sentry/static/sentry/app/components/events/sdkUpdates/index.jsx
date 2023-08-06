import React from 'react';
import Alert from 'app/components/alert';
import { IconUpgrade } from 'app/icons';
import { tct } from 'app/locale';
import EventDataSection from 'app/components/events/eventDataSection';
import getSuggestion from './getSuggestion';
var SdkUpdates = function (_a) {
    var event = _a.event;
    var sdkUpdates = event.sdkUpdates;
    var eventDataSectinContent = sdkUpdates
        .map(function (sdkUpdate, index) {
        var suggestion = getSuggestion({ suggestion: sdkUpdate, event: event });
        if (!suggestion) {
            return null;
        }
        return (<Alert key={index} type="info" icon={<IconUpgrade />}>
          {tct('We recommend you [suggestion]', { suggestion: suggestion })}
        </Alert>);
    })
        .filter(function (alert) { return !!alert; });
    if (!eventDataSectinContent.length) {
        return null;
    }
    return (<EventDataSection title={null} type="sdk-updates">
      {eventDataSectinContent}
    </EventDataSection>);
};
export default SdkUpdates;
//# sourceMappingURL=index.jsx.map