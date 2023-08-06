import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Form from 'app/views/settings/components/forms/form';
import FormField from 'app/views/settings/components/forms/formField';
import { IconFlag } from 'app/icons';
import InputControl from 'app/views/settings/components/forms/controls/input';
import RangeSlider from 'app/views/settings/components/forms/controls/rangeSlider';
import space from 'app/styles/space';
var RATE_LIMIT_FORMAT_MAP = new Map([
    [0, 'None'],
    [60, '1 minute'],
    [300, '5 minutes'],
    [900, '15 minutes'],
    [3600, '1 hour'],
    [7200, '2 hours'],
    [14400, '4 hours'],
    [21600, '6 hours'],
    [43200, '12 hours'],
    [86400, '24 hours'],
]);
var formatRateLimitWindow = function (val) { return RATE_LIMIT_FORMAT_MAP.get(val); };
var KeyRateLimitsForm = /** @class */ (function (_super) {
    __extends(KeyRateLimitsForm, _super);
    function KeyRateLimitsForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeWindow = function (onChange, onBlur, currentValueObj, value, e) {
            var valueObj = __assign(__assign({}, currentValueObj), { window: value });
            onChange(valueObj, e);
            onBlur(valueObj, e);
        };
        _this.handleChangeCount = function (cb, value, e) {
            var valueObj = __assign(__assign({}, value), { count: e.target.value });
            cb(valueObj, e);
        };
        return _this;
    }
    KeyRateLimitsForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, data = _a.data, disabled = _a.disabled;
        var _b = this.props.params, keyId = _b.keyId, orgId = _b.orgId, projectId = _b.projectId;
        var apiEndpoint = "/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/";
        var disabledAlert = function (_a) {
            var features = _a.features;
            return (<FeatureDisabled alert={PanelAlert} features={features} featureName={t('Key Rate Limits')}/>);
        };
        return (<Form saveOnBlur apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
        <Feature features={['projects:rate-limits']} hookName="feature-disabled:rate-limits" renderDisabled={function (_a) {
            var children = _a.children, props = __rest(_a, ["children"]);
            return typeof children === 'function' &&
                children(__assign(__assign({}, props), { renderDisabled: disabledAlert }));
        }}>
          {function (_a) {
            var hasFeature = _a.hasFeature, features = _a.features, organization = _a.organization, project = _a.project, renderDisabled = _a.renderDisabled;
            return (<Panel>
              <PanelHeader>{t('Rate Limits')}</PanelHeader>

              <PanelBody>
                <PanelAlert type="info" icon={<IconFlag size="md"/>}>
                  {t("Rate limits provide a flexible way to manage your event\n                      volume. If you have a noisy project or environment you\n                      can configure a rate limit for this key to reduce the\n                      number of events processed.")}
                </PanelAlert>
                {!hasFeature &&
                typeof renderDisabled === 'function' &&
                renderDisabled({
                    organization: organization,
                    project: project,
                    features: features,
                    hasFeature: hasFeature,
                    children: null,
                })}
                <FormField className="rate-limit-group" name="rateLimit" label={t('Rate Limit')} disabled={disabled || !hasFeature} validate={function (_a) {
                var form = _a.form;
                //TODO(TS): is validate actually doing anything because it's an unexpected prop
                var isValid = form &&
                    form.rateLimit &&
                    typeof form.rateLimit.count !== 'undefined' &&
                    typeof form.rateLimit.window !== 'undefined';
                if (isValid) {
                    return [];
                }
                return [['rateLimit', t('Fill in both fields first')]];
            }} help={t('Apply a rate limit to this credential to cap the amount of events accepted during a time window.')} inline={false}>
                  {function (_a) {
                var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value;
                return (<RateLimitRow>
                      <InputControl type="number" name="rateLimit.count" min={0} value={value && value.count} placeholder={t('Count')} disabled={disabled || !hasFeature} onChange={_this.handleChangeCount.bind(_this, onChange, value)} onBlur={_this.handleChangeCount.bind(_this, onBlur, value)}/>
                      <EventsIn>{t('event(s) in')}</EventsIn>
                      <RangeSlider name="rateLimit.window" allowedValues={Array.from(RATE_LIMIT_FORMAT_MAP.keys())} value={value && value.window} placeholder={t('Window')} formatLabel={formatRateLimitWindow} disabled={disabled || !hasFeature} onChange={_this.handleChangeWindow.bind(_this, onChange, onBlur, value)}/>
                    </RateLimitRow>);
            }}
                </FormField>
              </PanelBody>
            </Panel>);
        }}
        </Feature>
      </Form>);
    };
    return KeyRateLimitsForm;
}(React.Component));
export default KeyRateLimitsForm;
var RateLimitRow = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 2fr 1fr 2fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 2fr 1fr 2fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(1));
var EventsIn = styled('small')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  text-align: center;\n  white-space: nowrap;\n"], ["\n  font-size: ", ";\n  text-align: center;\n  white-space: nowrap;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=keyRateLimitsForm.jsx.map