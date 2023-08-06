import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import space from 'app/styles/space';
import { STACK_TYPE, STACK_VIEW } from 'app/types/stacktrace';
var CrashActions = function (_a) {
    var _b;
    var stackView = _a.stackView, stackType = _a.stackType, stacktrace = _a.stacktrace, thread = _a.thread, exception = _a.exception, platform = _a.platform, onChange = _a.onChange;
    var hasSystemFrames = (stacktrace === null || stacktrace === void 0 ? void 0 : stacktrace.hasSystemFrames) || ((_b = thread === null || thread === void 0 ? void 0 : thread.stacktrace) === null || _b === void 0 ? void 0 : _b.hasSystemFrames) || (exception === null || exception === void 0 ? void 0 : exception.values.find(function (x) { var _a; return !!((_a = x === null || x === void 0 ? void 0 : x.stacktrace) === null || _a === void 0 ? void 0 : _a.hasSystemFrames); }));
    var hasMinified = !stackType
        ? false
        : !!(exception === null || exception === void 0 ? void 0 : exception.values.find(function (x) { return x.rawStacktrace; })) || !!(thread === null || thread === void 0 ? void 0 : thread.rawStacktrace);
    var notify = function (options) {
        if (onChange) {
            onChange(options);
        }
    };
    var setStackType = function (type) { return function () {
        notify({ stackType: type });
    }; };
    var setStackView = function (view) { return function () {
        notify({ stackView: view });
    }; };
    var getOriginalButtonLabel = function () {
        if (platform === 'javascript' || platform === 'node') {
            return t('Original');
        }
        return t('Symbolicated');
    };
    var getMinifiedButtonLabel = function () {
        if (platform === 'javascript' || platform === 'node') {
            return t('Minified');
        }
        return t('Unsymbolicated');
    };
    return (<ButtonGroupWrapper>
      <ButtonBar active={stackView} merged>
        {hasSystemFrames && (<Button barId={STACK_VIEW.APP} size="xsmall" onClick={setStackView(STACK_VIEW.APP)}>
            {t('App Only')}
          </Button>)}
        <Button barId={STACK_VIEW.FULL} size="xsmall" onClick={setStackView(STACK_VIEW.FULL)}>
          {t('Full')}
        </Button>
        <Button barId={STACK_VIEW.RAW} onClick={setStackView(STACK_VIEW.RAW)} size="xsmall">
          {t('Raw')}
        </Button>
      </ButtonBar>
      {hasMinified && (<ButtonBar active={stackType} merged>
          <Button barId={STACK_TYPE.ORIGINAL} size="xsmall" onClick={setStackType(STACK_TYPE.ORIGINAL)}>
            {getOriginalButtonLabel()}
          </Button>
          <Button barId={STACK_TYPE.MINIFIED} size="xsmall" onClick={setStackType(STACK_TYPE.MINIFIED)}>
            {getMinifiedButtonLabel()}
          </Button>
        </ButtonBar>)}
    </ButtonGroupWrapper>);
};
export default CrashActions;
var ButtonGroupWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  > * {\n    padding: ", " 0;\n  }\n  > * :not(:last-child) {\n    margin-right: ", ";\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  > * {\n    padding: ", " 0;\n  }\n  > * :not(:last-child) {\n    margin-right: ", ";\n  }\n"])), space(0.5), space(1));
var templateObject_1;
//# sourceMappingURL=crashActions.jsx.map