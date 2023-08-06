import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Card from 'app/components/card';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import Radio from 'app/components/radio';
import textStyles from 'app/styles/text';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import Tooltip from 'app/components/tooltip';
import Feature from 'app/components/acl/feature';
import { trackAnalyticsEvent } from 'app/utils/analytics';
var MetricsTooltip = function (_a) {
    var children = _a.children;
    return (<Tooltip title={t("A metric is the value of an aggregate function like count() or avg()\n       applied to your events over time")}>
    <abbr>{children}</abbr>
  </Tooltip>);
};
var IssuesTooltip = function (_a) {
    var children = _a.children;
    return (<Tooltip title={t("Sentry groups similar events into an Issue based on their stack trace\n       and other factors.")}>
    <abbr>{children}</abbr>
  </Tooltip>);
};
var TypeChooser = function (_a) {
    var onChange = _a.onChange, organization = _a.organization, selected = _a.selected;
    var trackedOnChange = function (type) {
        trackAnalyticsEvent({
            eventKey: 'alert_chooser_cards.select',
            eventName: 'Alert Chooser Cards: Select',
            organization_id: organization.id,
            type: type,
        });
        onChange(type);
    };
    return (<Container>
      <TypeCard interactive onClick={function () { return trackedOnChange('metric'); }}>
        <RadioLabel>
          <Radio aria-label="metric" checked={selected === 'metric'} onChange={function () { return trackedOnChange('metric'); }}/>
          {t('Metric Alert')}
        </RadioLabel>
        <Feature requireAll features={['organizations:performance-view']}>
          {function (_a) {
        var hasFeature = _a.hasFeature;
        return hasFeature ? (<React.Fragment>
                <p>
                  {tct("Notifies you when a [tooltip:metric] exceeds a threshold.", {
            tooltip: <MetricsTooltip />,
        })}
                </p>
                {!selected && (<React.Fragment>
                    <ExampleHeading>{t('For Example:')}</ExampleHeading>
                    <List symbol="bullet">
                      <ListItem>
                        {t('Performance metrics like latency and apdex')}
                      </ListItem>
                      <ListItem>
                        {t('Frequency of error events or users affected in the project')}
                      </ListItem>
                    </List>
                  </React.Fragment>)}
              </React.Fragment>) : (<React.Fragment>
                <p>
                  {tct("Notifies you when a [tooltip:metric] like frequency of events or users affected in\n                   the project exceeds a threshold.", { tooltip: <MetricsTooltip /> })}
                </p>
                {!selected && (<React.Fragment>
                    <ExampleHeading>{t('For Example:')}</ExampleHeading>
                    <List symbol="bullet">
                      <ListItem>
                        {t('Total events in the project exceed 1000/minute')}
                      </ListItem>
                      <ListItem>
                        {tct('Events with tag [code:database] and "API" in the title exceed 100/minute', { code: <code /> })}
                      </ListItem>
                    </List>
                  </React.Fragment>)}
              </React.Fragment>);
    }}
        </Feature>
      </TypeCard>
      <TypeCard interactive onClick={function () { return trackedOnChange('issue'); }}>
        <RadioLabel>
          <Radio aria-label="issue" checked={selected === 'issue'} onChange={function () { return trackedOnChange('issue'); }}/>
          {t('Issue Alert')}
        </RadioLabel>
        <p>
          {tct("Notifies you when individual [tooltip:Sentry Issues] trigger your\n           alerting criteria.", { tooltip: <IssuesTooltip /> })}
        </p>
        {!selected && (<React.Fragment>
            <ExampleHeading>{t('For Example:')}</ExampleHeading>
            <List symbol="bullet">
              <ListItem>{t('New Issues or regressions')}</ListItem>
              <ListItem>
                {t('Frequency of individual Issues exceeds 100/minute')}
              </ListItem>
            </List>
          </React.Fragment>)}
      </TypeCard>
    </Container>);
};
var RadioLabel = styled('label')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  cursor: pointer;\n  margin-bottom: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  cursor: pointer;\n  margin-bottom: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(3), space(2));
var ExampleHeading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-transform: uppercase;\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  text-transform: uppercase;\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; }, space(2));
var Container = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"])), space(3));
var TypeCard = styled(Card)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  cursor: pointer;\n  padding: ", ";\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  cursor: pointer;\n  padding: ", ";\n  margin-bottom: ", ";\n  ", ";\n"])), space(4), space(3), textStyles);
export default TypeChooser;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=alertTypeChooser.jsx.map