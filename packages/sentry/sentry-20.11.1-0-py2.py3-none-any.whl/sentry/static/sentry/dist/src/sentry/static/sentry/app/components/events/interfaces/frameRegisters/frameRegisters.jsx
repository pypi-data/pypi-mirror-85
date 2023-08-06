import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { defined } from 'app/utils';
import { t } from 'app/locale';
import FrameRegistersValue from 'app/components/events/interfaces/frameRegisters/frameRegistersValue';
import { getMeta } from 'app/components/events/meta/metaProxy';
var FrameRegisters = function (_a) {
    var data = _a.data;
    // make sure that clicking on the registers does not actually do
    // anything on the containing element.
    var handlePreventToggling = function (event) {
        event.stopPropagation();
    };
    return (<RegistersWrapper>
      <RegistersHeading>{t('registers')}</RegistersHeading>
      <Registers>
        {Object.entries(data).map(function (_a) {
        var _b = __read(_a, 2), name = _b[0], value = _b[1];
        if (!defined(value)) {
            return null;
        }
        return (<Register key={name} onClick={handlePreventToggling}>
              <RegisterName>{name}</RegisterName>
              <FrameRegistersValue value={value} meta={getMeta(data, name)}/>
            </Register>);
    })}
      </Registers>
    </RegistersWrapper>);
};
var RegistersWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding-top: 10px;\n"], ["\n  border-top: 1px solid ", ";\n  padding-top: 10px;\n"])), function (p) { return p.theme.innerBorder; });
var Registers = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  margin-left: 125px;\n  padding: 2px 0px;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  margin-left: 125px;\n  padding: 2px 0px;\n"])));
var Register = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 4px 5px;\n"], ["\n  padding: 4px 5px;\n"])));
var RegistersHeading = styled('strong')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: 600;\n  font-size: 13px;\n  width: 125px;\n  max-width: 125px;\n  word-wrap: break-word;\n  padding: 10px 15px 10px 0;\n  line-height: 1.4;\n  float: left;\n"], ["\n  font-weight: 600;\n  font-size: 13px;\n  width: 125px;\n  max-width: 125px;\n  word-wrap: break-word;\n  padding: 10px 15px 10px 0;\n  line-height: 1.4;\n  float: left;\n"])));
var RegisterName = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: inline-block;\n  font-size: 13px;\n  font-weight: 600;\n  text-align: right;\n  width: 4em;\n"], ["\n  display: inline-block;\n  font-size: 13px;\n  font-weight: 600;\n  text-align: right;\n  width: 4em;\n"])));
export default FrameRegisters;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=frameRegisters.jsx.map