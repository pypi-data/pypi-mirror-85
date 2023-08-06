import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import { t } from 'app/locale';
import space from 'app/styles/space';
var RootSpanStatus = /** @class */ (function (_super) {
    __extends(RootSpanStatus, _super);
    function RootSpanStatus() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RootSpanStatus.prototype.getTransactionEvent = function () {
        var event = this.props.event;
        if (event.type === 'transaction') {
            return event;
        }
        return undefined;
    };
    RootSpanStatus.prototype.getRootSpanStatus = function () {
        var _a, _b;
        var event = this.getTransactionEvent();
        var DEFAULT = '\u2014';
        if (!event) {
            return DEFAULT;
        }
        var traceContext = (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
        return (_b = traceContext === null || traceContext === void 0 ? void 0 : traceContext.status) !== null && _b !== void 0 ? _b : DEFAULT;
    };
    RootSpanStatus.prototype.getHttpStatusCode = function () {
        var event = this.props.event;
        var tags = event.tags;
        if (!Array.isArray(tags)) {
            return '';
        }
        var tag = tags.find(function (tagObject) { return tagObject.key === 'http.status_code'; });
        if (!tag) {
            return '';
        }
        return tag.value;
    };
    RootSpanStatus.prototype.render = function () {
        var event = this.getTransactionEvent();
        if (!event) {
            return null;
        }
        var label = (this.getHttpStatusCode() + " " + this.getRootSpanStatus()).trim();
        return (<Container>
        <Header>
          <SectionHeading>{t('Status')}</SectionHeading>
        </Header>
        <div>{label}</div>
      </Container>);
    };
    return RootSpanStatus;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(4));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
export default RootSpanStatus;
var templateObject_1, templateObject_2;
//# sourceMappingURL=rootSpanStatus.jsx.map