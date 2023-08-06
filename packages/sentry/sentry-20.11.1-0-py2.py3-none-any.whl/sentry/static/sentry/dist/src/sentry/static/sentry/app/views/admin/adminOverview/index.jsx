import React from 'react';
import DocumentTitle from 'react-document-title';
import { Panel, PanelHeader, PanelBody } from 'app/components/panels';
import { t } from 'app/locale';
import ApiChart from './apiChart';
import EventChart from './eventChart';
var AdminOverview = function () {
    var resolution = '1h';
    var since = new Date().getTime() / 1000 - 3600 * 24 * 7;
    return (<DocumentTitle title="Admin Overview - Sentry">
      <React.Fragment>
        <h3>{t('System Overview')}</h3>

        <Panel key="events">
          <PanelHeader>{t('Event Throughput')}</PanelHeader>
          <PanelBody withPadding>
            <EventChart since={since} resolution={resolution}/>
          </PanelBody>
        </Panel>

        <Panel key="api">
          <PanelHeader>{t('API Responses')}</PanelHeader>
          <PanelBody withPadding>
            <ApiChart since={since} resolution={resolution}/>
          </PanelBody>
        </Panel>
      </React.Fragment>
    </DocumentTitle>);
};
export default AdminOverview;
//# sourceMappingURL=index.jsx.map