import React from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import Line from 'app/components/events/interfaces/frame/line';
import { t } from 'app/locale';
var TemplateInterface = function (_a) {
    var type = _a.type, data = _a.data, event = _a.event;
    return (<EventDataSection type={type} title={t('Template')}>
    <div className="traceback no-exception">
      <ul>
        <Line data={data} event={event} registers={{}} components={[]} isExpanded/>
      </ul>
    </div>
  </EventDataSection>);
};
export default TemplateInterface;
//# sourceMappingURL=template.jsx.map