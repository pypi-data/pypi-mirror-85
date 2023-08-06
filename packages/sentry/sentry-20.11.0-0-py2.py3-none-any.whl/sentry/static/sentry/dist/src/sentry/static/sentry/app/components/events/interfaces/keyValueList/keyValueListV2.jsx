import { __makeTemplateObject } from "tslib";
import React from 'react';
import sortBy from 'lodash/sortBy';
import styled from '@emotion/styled';
import { defined } from 'app/utils';
import ContextData from 'app/components/contextData';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import theme from 'app/utils/theme';
var KeyValueList = function (_a) {
    var data = _a.data, _b = _a.isContextData, isContextData = _b === void 0 ? false : _b, _c = _a.isSorted, isSorted = _c === void 0 ? true : _c, _d = _a.raw, raw = _d === void 0 ? false : _d, _e = _a.longKeys, longKeys = _e === void 0 ? false : _e, onClick = _a.onClick;
    if (!defined(data) || data.length === 0) {
        return null;
    }
    var getData = function () {
        if (isSorted) {
            return sortBy(data, [function (_a) {
                    var key = _a.key;
                    return key.toLowerCase();
                }]);
        }
        return data;
    };
    return (<table className="table key-value" onClick={onClick}>
      <tbody>
        {getData().map(function (_a) {
        var key = _a.key, subject = _a.subject, _b = _a.value, value = _b === void 0 ? null : _b, meta = _a.meta, subjectIcon = _a.subjectIcon, subjectDataTestId = _a.subjectDataTestId;
        var dataValue = typeof value === 'object' && !React.isValidElement(value)
            ? JSON.stringify(value, null, 2)
            : value;
        var valueIsReactRenderable = typeof dataValue !== 'string' && React.isValidElement(dataValue);
        var contentComponent = (<pre className="val-string">
                <AnnotatedText value={dataValue} meta={meta}/>
                {subjectIcon}
              </pre>);
        if (isContextData) {
            contentComponent = (<ContextData data={!raw ? value : JSON.stringify(value)} meta={meta} withAnnotatedText>
                  {subjectIcon}
                </ContextData>);
        }
        else if (valueIsReactRenderable) {
            contentComponent = dataValue;
        }
        return (<tr key={key}>
                <TableSubject className="key" wide={longKeys}>
                  {subject}
                </TableSubject>
                <td className="val" data-test-id={subjectDataTestId}>
                  {contentComponent}
                </td>
              </tr>);
    })}
      </tbody>
    </table>);
};
var TableSubject = styled('td')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: ", ";\n  }\n"])), theme.breakpoints[2], function (p) { return (p.wide ? '620px !important' : 'none'); });
KeyValueList.displayName = 'KeyValueList';
export default KeyValueList;
var templateObject_1;
//# sourceMappingURL=keyValueListV2.jsx.map