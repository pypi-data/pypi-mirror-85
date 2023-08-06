import { __makeTemplateObject, __read } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import { defined } from 'app/utils';
var Context = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline;\n"], ["\n  display: inline;\n"])));
var ContextLine = function (props) {
    var _a;
    var line = props.line, isActive = props.isActive, className = props.className;
    var lineWs = '';
    var lineCode = '';
    if (defined(line[1]) && line[1].match) {
        _a = __read(line[1].match(/^(\s*)(.*?)$/m), 3), lineWs = _a[1], lineCode = _a[2];
    }
    var Component = !props.children ? React.Fragment : Context;
    return (<li className={classNames(className, 'expandable', { active: isActive })} key={line[0]}>
      <Component>
        <span className="ws">{lineWs}</span>
        <span className="contextline">{lineCode}</span>
      </Component>
      {props.children}
    </li>);
};
ContextLine.propTypes = {
    line: PropTypes.array.isRequired,
    isActive: PropTypes.bool,
};
export default ContextLine;
var templateObject_1;
//# sourceMappingURL=contextLine.jsx.map