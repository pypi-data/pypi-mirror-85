import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import withApi from 'app/utils/withApi';
import Hovercard, { Body } from 'app/components/hovercard';
import { isStacktraceNewestFirst } from 'app/components/events/interfaces/stacktrace';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
var StacktracePreview = /** @class */ (function (_super) {
    __extends(StacktracePreview, _super);
    function StacktracePreview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            event: null,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, issueId, event_1, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (this.state.event) {
                            return [2 /*return*/];
                        }
                        _a = this.props, api = _a.api, issueId = _a.issueId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + issueId + "/events/latest/")];
                    case 2:
                        event_1 = _c.sent();
                        this.setState({ event: event_1 });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleStacktracePreviewClick = function (event) {
            event.stopPropagation();
            event.preventDefault();
        };
        return _this;
    }
    StacktracePreview.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, organization = _d.organization, children = _d.children;
        var event = this.state.event;
        var exception = (_a = event === null || event === void 0 ? void 0 : event.entries.find(function (e) { return e.type === 'exception'; })) === null || _a === void 0 ? void 0 : _a.data;
        var stacktrace = (_b = exception === null || exception === void 0 ? void 0 : exception.values[0]) === null || _b === void 0 ? void 0 : _b.stacktrace;
        if (!organization.features.includes('stacktrace-hover-preview')) {
            return children;
        }
        return (<span onMouseEnter={this.fetchData}>
        <StyledHovercard body={event && exception && stacktrace ? (<div onClick={this.handleStacktracePreviewClick}>
                <StacktraceContent data={stacktrace} expandFirstFrame 
        // includeSystemFrames={!exception.hasSystemFrames} // (chainedException && stacktrace.frames.every(frame => !frame.inApp))
        includeSystemFrames={stacktrace.frames.every(function (frame) { return !frame.inApp; })} platform={((_c = event.platform) !== null && _c !== void 0 ? _c : 'other')} newestFirst={isStacktraceNewestFirst()} event={event}/>
              </div>) : null} position="left">
          {children}
        </StyledHovercard>
      </span>);
    };
    return StacktracePreview;
}(React.Component));
var StyledHovercard = styled(Hovercard)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 700px;\n  border: none;\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow: scroll;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  width: 700px;\n  border: none;\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow: scroll;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), Body, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[2]; });
export default withApi(StacktracePreview);
var templateObject_1;
//# sourceMappingURL=stacktracePreview.jsx.map