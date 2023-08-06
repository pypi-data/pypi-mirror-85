import { __assign, __extends } from "tslib";
import React from 'react';
import ConfigStore from 'app/stores/configStore';
import EventDataSection from 'app/components/events/eventDataSection';
import { t } from 'app/locale';
import CrashTitle from 'app/components/events/interfaces/crashHeader/crashTitle';
import CrashActions from 'app/components/events/interfaces/crashHeader/crashActions';
import CrashContent from 'app/components/events/interfaces/crashContent';
import { STACK_VIEW, STACK_TYPE } from 'app/types/stacktrace';
export function isStacktraceNewestFirst() {
    var user = ConfigStore.get('user');
    // user may not be authenticated
    if (!user) {
        return true;
    }
    switch (user.options.stacktraceOrder) {
        case 2:
            return true;
        case 1:
            return false;
        case -1:
        default:
            return true;
    }
}
var defaultProps = {
    hideGuide: false,
};
var StacktraceInterface = /** @class */ (function (_super) {
    __extends(StacktraceInterface, _super);
    function StacktraceInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            stackView: _this.props.data.hasSystemFrames ? STACK_VIEW.APP : STACK_VIEW.FULL,
            newestFirst: isStacktraceNewestFirst(),
        };
        _this.handleChangeNewestFirst = function (_a) {
            var newestFirst = _a.newestFirst;
            _this.setState(function (prevState) { return (__assign(__assign({}, prevState), { newestFirst: newestFirst })); });
        };
        _this.handleChangeStackView = function (_a) {
            var stackView = _a.stackView;
            if (!stackView) {
                return;
            }
            _this.setState(function (prevState) { return (__assign(__assign({}, prevState), { stackView: stackView })); });
        };
        return _this;
    }
    StacktraceInterface.prototype.render = function () {
        var _a = this.props, projectId = _a.projectId, event = _a.event, data = _a.data, hideGuide = _a.hideGuide, type = _a.type;
        var _b = this.state, stackView = _b.stackView, newestFirst = _b.newestFirst;
        return (<EventDataSection type={type} title={<CrashTitle title={t('Stack Trace')} hideGuide={hideGuide} newestFirst={newestFirst} onChange={this.handleChangeNewestFirst}/>} actions={<CrashActions stackView={stackView} platform={event.platform} stacktrace={data} onChange={this.handleChangeStackView}/>} wrapTitle={false}>
        <CrashContent projectId={projectId} event={event} stackView={stackView} newestFirst={newestFirst} stacktrace={data} stackType={STACK_TYPE.ORIGINAL}/>
      </EventDataSection>);
    };
    StacktraceInterface.defaultProps = defaultProps;
    return StacktraceInterface;
}(React.Component));
export default StacktraceInterface;
//# sourceMappingURL=stacktrace.jsx.map