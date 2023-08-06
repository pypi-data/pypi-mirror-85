import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import TextOverflow from 'app/components/textOverflow';
import { IconFire } from 'app/icons';
import { Grid, GridCell } from './styles';
var Option = function (_a) {
    var id = _a.id, details = _a.details, name = _a.name, crashed = _a.crashed, crashedInfo = _a.crashedInfo;
    var _b = details.label, label = _b === void 0 ? "<" + t('unknown') + ">" : _b, _c = details.filename, filename = _c === void 0 ? "<" + t('unknown') + ">" : _c;
    var optionName = name || "<" + t('unknown') + ">";
    return (<Grid>
      <GridCell>
        <InnerCell>
          <Tooltip title={"#" + id} position="top">
            <TextOverflow>{"#" + id}</TextOverflow>
          </Tooltip>
        </InnerCell>
      </GridCell>
      <GridCell>
        <InnerCell isBold>
          <Tooltip title={optionName} position="top">
            <TextOverflow>{optionName}</TextOverflow>
          </Tooltip>
        </InnerCell>
      </GridCell>
      <GridCell>
        <InnerCell color="blue300">
          <Tooltip title={label} position="top">
            <TextOverflow>{label}</TextOverflow>
          </Tooltip>
        </InnerCell>
      </GridCell>
      <GridCell>
        <InnerCell color="purple300">
          <Tooltip title={filename} position="top">
            <TextOverflow>{filename}</TextOverflow>
          </Tooltip>
        </InnerCell>
      </GridCell>
      <GridCell>
        {crashed && (<InnerCell isCentered>
            {crashedInfo ? (<Tooltip skipWrapper title={tct('Errored with [crashedInfo]', {
        crashedInfo: crashedInfo.values[0].type,
    })} position="top">
                <IconFire color="red300"/>
              </Tooltip>) : (<IconFire color="red300"/>)}
          </InnerCell>)}
      </GridCell>
    </Grid>);
};
export default Option;
var InnerCell = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: ", ";\n  font-weight: ", ";\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: ", ";\n  font-weight: ", ";\n  ", "\n"])), function (p) { return (p.isCentered ? 'center' : 'flex-start'); }, function (p) { return (p.isBold ? 600 : 400); }, function (p) { return p.color && "color: " + p.theme[p.color]; });
var templateObject_1;
//# sourceMappingURL=option.jsx.map