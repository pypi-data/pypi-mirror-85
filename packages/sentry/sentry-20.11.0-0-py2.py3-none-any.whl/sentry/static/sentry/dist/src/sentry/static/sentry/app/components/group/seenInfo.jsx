import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import DateTime from 'app/components/dateTime';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import VersionHoverCard from 'app/components/versionHoverCard';
import space from 'app/styles/space';
import { IconInfo } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import { defined, toTitleCase } from 'app/utils';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var SeenInfo = /** @class */ (function (_super) {
    __extends(SeenInfo, _super);
    function SeenInfo() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SeenInfo.prototype.shouldComponentUpdate = function (nextProps) {
        var _a;
        var _b = this.props, date = _b.date, release = _b.release;
        return (release === null || release === void 0 ? void 0 : release.version) !== ((_a = nextProps.release) === null || _a === void 0 ? void 0 : _a.version) || date !== nextProps.date;
    };
    SeenInfo.prototype.getReleaseTrackingUrl = function () {
        var _a = this.props, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
        return "/settings/" + orgSlug + "/projects/" + projectSlug + "/release-tracking/";
    };
    SeenInfo.prototype.getTooltipTitle = function () {
        var _a = this.props, date = _a.date, dateGlobal = _a.dateGlobal, title = _a.title, environment = _a.environment;
        return (<div style={{ width: '170px' }}>
        <div className="time-label" style={{ marginBottom: '10px' }}>
          {title}
        </div>
        {environment && (<React.Fragment>
            {toTitleCase(environment)}
            {': '}
            <TimeSince date={date} disabledAbsoluteTooltip/>
            <br />
          </React.Fragment>)}
        {t('Globally: ')}
        <TimeSince date={dateGlobal} disabledAbsoluteTooltip/>
      </div>);
    };
    SeenInfo.prototype.render = function () {
        var _a = this.props, date = _a.date, dateGlobal = _a.dateGlobal, environment = _a.environment, release = _a.release, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, projectId = _a.projectId;
        return (<DateWrapper>
        {date ? (<TooltipWrapper>
            <Tooltip title={this.getTooltipTitle()} disableForVisualTest>
              <IconInfo size="xs" color="gray300"/>
              <TimeSince date={date} disabledAbsoluteTooltip/>
            </Tooltip>
          </TooltipWrapper>) : dateGlobal && environment === '' ? (<React.Fragment>
            <Tooltip title={this.getTooltipTitle()} disableForVisualTest>
              <TimeSince date={dateGlobal} disabledAbsoluteTooltip/>
            </Tooltip>
          </React.Fragment>) : (<React.Fragment>{t('n/a')} </React.Fragment>)}
        {defined(release) ? (<React.Fragment>
            {t('in release ')}
            <VersionHoverCard orgSlug={orgSlug} projectSlug={projectSlug} releaseVersion={release.version}>
              <span>
                <Version version={release.version} projectId={projectId}/>
              </span>
            </VersionHoverCard>
          </React.Fragment>) : !this.props.hasRelease ? (<React.Fragment>
            <NotConfigured>
              <a href={this.getReleaseTrackingUrl()}>{t('Releases not configured')}</a>
            </NotConfigured>
          </React.Fragment>) : (<React.Fragment>{t('Release n/a')}</React.Fragment>)}
        <StyledDateTime date={date} seconds/>
      </DateWrapper>);
    };
    SeenInfo.propTypes = {
        orgSlug: PropTypes.string.isRequired,
        projectSlug: PropTypes.string.isRequired,
        projectId: PropTypes.string.isRequired,
        date: PropTypes.any,
        dateGlobal: PropTypes.any,
        release: PropTypes.shape({
            version: PropTypes.string.isRequired,
        }),
        environment: PropTypes.string,
        hasRelease: PropTypes.bool.isRequired,
        title: PropTypes.string.isRequired,
    };
    SeenInfo.contextTypes = {
        organization: PropTypes.object,
    };
    return SeenInfo;
}(React.Component));
var NotConfigured = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.25));
var StyledDateTime = styled(DateTime)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: block;\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var DateWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  margin-bottom: ", ";\n  ", ";\n"])), space(2), overflowEllipsis);
var TooltipWrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n  svg {\n    margin-right: ", ";\n    position: relative;\n    top: 1px;\n  }\n\n  a {\n    display: inline;\n  }\n"], ["\n  margin-right: ", ";\n  svg {\n    margin-right: ", ";\n    position: relative;\n    top: 1px;\n  }\n\n  a {\n    display: inline;\n  }\n"])), space(0.25), space(0.5));
export default SeenInfo;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=seenInfo.jsx.map