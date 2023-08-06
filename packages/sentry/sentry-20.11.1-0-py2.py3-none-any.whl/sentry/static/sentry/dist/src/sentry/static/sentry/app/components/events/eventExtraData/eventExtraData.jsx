import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import EventDataSection from 'app/components/events/eventDataSection';
import SentryTypes from 'app/sentryTypes';
import EventDataContent from './eventDataContent';
var EventExtraData = /** @class */ (function (_super) {
    __extends(EventExtraData, _super);
    function EventExtraData() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            raw: false,
        };
        _this.toggleRaw = function (shouldBeRaw) {
            _this.setState({
                raw: shouldBeRaw,
            });
        };
        return _this;
    }
    EventExtraData.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return this.props.event.id !== nextProps.event.id || this.state.raw !== nextState.raw;
    };
    EventExtraData.prototype.render = function () {
        return (<div className="extra-data">
        <EventDataSection type="extra" title={t('Additional Data')} toggleRaw={this.toggleRaw} raw={this.state.raw}>
          <EventDataContent raw={this.state.raw} data={this.props.event.context}/>
        </EventDataSection>
      </div>);
    };
    EventExtraData.propTypes = {
        event: SentryTypes.Event.isRequired,
    };
    return EventExtraData;
}(React.Component));
export default EventExtraData;
//# sourceMappingURL=eventExtraData.jsx.map