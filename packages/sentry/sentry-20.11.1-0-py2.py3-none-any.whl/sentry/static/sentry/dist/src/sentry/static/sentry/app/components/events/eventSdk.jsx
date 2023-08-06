import React from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import Annotated from 'app/components/events/meta/annotated';
import { t } from 'app/locale';
var EventSdk = function (_a) {
    var sdk = _a.sdk;
    return (<EventDataSection type="sdk" title={t('SDK')}>
    <table className="table key-value">
      <tbody>
        <tr key="name">
          <td className="key">{t('Name')}</td>
          <td className="value">
            <Annotated object={sdk} objectKey="name">
              {function (value) { return <pre className="val-string">{value}</pre>; }}
            </Annotated>
          </td>
        </tr>
        <tr key="version">
          <td className="key">{t('Version')}</td>
          <td className="value">
            <Annotated object={sdk} objectKey="version">
              {function (value) { return <pre className="val-string">{value}</pre>; }}
            </Annotated>
          </td>
        </tr>
      </tbody>
    </table>
  </EventDataSection>);
};
export default EventSdk;
//# sourceMappingURL=eventSdk.jsx.map