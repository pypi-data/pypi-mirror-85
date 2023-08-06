import { __assign, __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import EventDataSection from 'app/components/events/eventDataSection';
import { isStacktraceNewestFirst } from 'app/components/events/interfaces/stacktrace';
import CrashTitle from 'app/components/events/interfaces/crashHeader/crashTitle';
import CrashActions from 'app/components/events/interfaces/crashHeader/crashActions';
import { STACK_TYPE, STACK_VIEW } from 'app/types/stacktrace';
import CrashContent from 'app/components/events/interfaces/crashContent';
var defaultProps = {
    hideGuide: false,
};
var Exception = /** @class */ (function (_super) {
    __extends(Exception, _super);
    function Exception() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            stackView: _this.props.data.hasSystemFrames ? STACK_VIEW.APP : STACK_VIEW.FULL,
            newestFirst: isStacktraceNewestFirst(),
            stackType: STACK_TYPE.ORIGINAL,
        };
        _this.handleChange = function (newState) {
            _this.setState(function (prevState) { return (__assign(__assign({}, prevState), newState)); });
        };
        return _this;
    }
    Exception.prototype.render = function () {
        var eventHasThreads = !!this.props.event.entries.find(function (entry) { return entry.type === 'threads'; });
        // in case there are threads in the event data, we don't render the
        // exception block.  Instead the exception is contained within the
        // thread interface.
        if (eventHasThreads) {
            return null;
        }
        var _a = this.props, projectId = _a.projectId, event = _a.event, data = _a.data, hideGuide = _a.hideGuide, type = _a.type;
        var _b = this.state, stackView = _b.stackView, stackType = _b.stackType, newestFirst = _b.newestFirst;
        var commonCrashHeaderProps = {
            newestFirst: newestFirst,
            hideGuide: hideGuide,
            onChange: this.handleChange,
        };
        return (<EventDataSection type={type} title={<CrashTitle title={t('Exception')} {...commonCrashHeaderProps}/>} actions={<CrashActions stackType={stackType} stackView={stackView} platform={event.platform} exception={data} {...commonCrashHeaderProps}/>} wrapTitle={false}>
        <CrashContent projectId={projectId} event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} exception={data}/>
      </EventDataSection>);
    };
    Exception.defaultProps = {
        hideGuide: false,
    };
    return Exception;
}(React.Component));
export default Exception;
//# sourceMappingURL=exception.jsx.map