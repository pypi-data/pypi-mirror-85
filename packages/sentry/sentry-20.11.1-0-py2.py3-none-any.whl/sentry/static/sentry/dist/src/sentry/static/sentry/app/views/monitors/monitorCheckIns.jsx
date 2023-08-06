import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { PanelBody, PanelItem } from 'app/components/panels';
import AsyncComponent from 'app/components/asyncComponent';
import Duration from 'app/components/duration';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
import CheckInIcon from './checkInIcon';
var MonitorCheckIns = /** @class */ (function (_super) {
    __extends(MonitorCheckIns, _super);
    function MonitorCheckIns() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MonitorCheckIns.prototype.getEndpoints = function () {
        var monitor = this.props.monitor;
        return [
            ['checkInList', "/monitors/" + monitor.id + "/checkins/", { query: { per_page: 10 } }],
        ];
    };
    MonitorCheckIns.prototype.renderError = function () {
        return <ErrorWrapper>{_super.prototype.renderError.call(this)}</ErrorWrapper>;
    };
    MonitorCheckIns.prototype.renderBody = function () {
        return (<PanelBody>
        {this.state.checkInList.map(function (checkIn) { return (<PanelItem key={checkIn.id}>
            <CheckInIconWrapper>
              <CheckInIcon status={checkIn.status} size={16}/>
            </CheckInIconWrapper>
            <TimeSinceWrapper>
              <TimeSince date={checkIn.dateCreated}/>
            </TimeSinceWrapper>
            <div>{checkIn.duration && <Duration seconds={checkIn.duration / 100}/>}</div>
          </PanelItem>); })}
      </PanelBody>);
    };
    MonitorCheckIns.propTypes = {
        monitor: PropTypes.object.isRequired,
    };
    return MonitorCheckIns;
}(AsyncComponent));
export default MonitorCheckIns;
var DivMargin = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(2));
var CheckInIconWrapper = styled(DivMargin)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TimeSinceWrapper = styled(DivMargin)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var ErrorWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: ", " ", " 0;\n"], ["\n  margin: ", " ", " 0;\n"])), space(3), space(3));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=monitorCheckIns.jsx.map