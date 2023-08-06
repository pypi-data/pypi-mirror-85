import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
var Qrcode = function (_a) {
    var code = _a.code;
    return (<Table>
    <tbody>
      {code.map(function (row, i) { return (<tr key={i}>
          {row.map(function (cell, j) { return (cell ? <BlackCell key={j}/> : <WhiteCell key={j}/>); })}
        </tr>); })}
    </tbody>
  </Table>);
};
var Cell = styled('td')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 6px;\n  width: 6px;\n  padding: 0;\n"], ["\n  height: 6px;\n  width: 6px;\n  padding: 0;\n"])));
var BlackCell = styled(Cell)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background-color: black;\n"], ["\n  background-color: black;\n"])));
var WhiteCell = styled(Cell)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: white;\n"], ["\n  background-color: white;\n"])));
var Table = styled('table')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
export default Qrcode;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=qrcode.jsx.map