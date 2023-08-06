import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { SectionHeading } from 'app/components/charts/styles';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
import { IconFire, IconWarning } from 'app/icons';
import { WEB_VITAL_DETAILS, LONG_WEB_VITAL_NAMES, } from 'app/views/performance/transactionVitals/constants';
import { formattedValue } from 'app/utils/measurements/index';
var RealUserMonitoring = /** @class */ (function (_super) {
    __extends(RealUserMonitoring, _super);
    function RealUserMonitoring() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RealUserMonitoring.prototype.hasMeasurements = function () {
        var event = this.props.event;
        if (!event.measurements) {
            return false;
        }
        return Object.keys(event.measurements).length > 0;
    };
    RealUserMonitoring.prototype.renderMeasurements = function () {
        var event = this.props.event;
        if (!event.measurements) {
            return null;
        }
        var measurementNames = Object.keys(event.measurements)
            .filter(function (name) {
            // ignore marker measurements
            return !name.startsWith('mark.');
        })
            .sort();
        return measurementNames.map(function (name) {
            var _a, _b;
            var value = event.measurements[name].value;
            var record = Object.values(WEB_VITAL_DETAILS).find(function (vital) { return vital.slug === name; });
            var failedThreshold = record ? value >= record.failureThreshold : false;
            var currentValue = formattedValue(record, value);
            var thresholdValue = formattedValue(record, (_a = record === null || record === void 0 ? void 0 : record.failureThreshold) !== null && _a !== void 0 ? _a : 0);
            if (!LONG_WEB_VITAL_NAMES.hasOwnProperty(name)) {
                return null;
            }
            return (<div key={name}>
          <StyledPanel failedThreshold={failedThreshold}>
            <Name>{(_b = LONG_WEB_VITAL_NAMES[name]) !== null && _b !== void 0 ? _b : name}</Name>
            <ValueRow>
              {failedThreshold ? (<FireIconContainer size="sm">
                  <Tooltip title={t('Fails threshold at %s.', thresholdValue)} position="top" containerDisplayMode="inline-block">
                    <IconFire size="sm"/>
                  </Tooltip>
                </FireIconContainer>) : null}
              <Value failedThreshold={failedThreshold}>{currentValue}</Value>
            </ValueRow>
          </StyledPanel>
        </div>);
        });
    };
    RealUserMonitoring.prototype.isOutdatedSdk = function () {
        var _a;
        var event = this.props.event;
        if (!((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.version)) {
            return false;
        }
        var sdkVersion = event.sdk.version;
        return (sdkVersion.startsWith('5.26.') ||
            sdkVersion.startsWith('5.27.0') ||
            sdkVersion.startsWith('5.27.1') ||
            sdkVersion.startsWith('5.27.2'));
    };
    RealUserMonitoring.prototype.render = function () {
        if (!this.hasMeasurements()) {
            return null;
        }
        return (<Container>
        <SectionHeading>
          {t('Web Vitals')}
          {this.isOutdatedSdk() && (<WarningIconContainer size="sm">
              <Tooltip title={t('These vitals were collected using an outdated SDK version and may not be accurate. To ensure accurate web vitals in new transaction events, please update your SDK to the latest version.')} position="top" containerDisplayMode="inline-block">
                <IconWarning size="sm"/>
              </Tooltip>
            </WarningIconContainer>)}
        </SectionHeading>
        <Measurements>{this.renderMeasurements()}</Measurements>
      </Container>);
    };
    return RealUserMonitoring;
}(React.Component));
var Measurements = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n"])), space(1));
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(4));
var StyledPanel = styled(Panel)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", " ", ";\n  margin-bottom: ", ";\n  ", "\n"], ["\n  padding: ", " ", ";\n  margin-bottom: ", ";\n  ", "\n"])), space(1), space(1.5), space(1), function (p) { return p.failedThreshold && "border: 1px solid " + p.theme.red300 + ";"; });
var Name = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject([""], [""])));
var ValueRow = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var WarningIconContainer = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-left: ", ";\n  color: ", ";\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, space(0.5), function (p) { return p.theme.red300; });
var FireIconContainer = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-right: ", ";\n  color: ", ";\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-right: ", ";\n  color: ", ";\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, space(0.5), function (p) { return p.theme.red300; });
var Value = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, function (p) { return p.failedThreshold && "color: " + p.theme.red300 + ";"; });
export default RealUserMonitoring;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=realUserMonitoring.jsx.map