import { __rest } from "tslib";
import React from 'react';
import classNames from 'classnames';
import omit from 'lodash/omit';
export default function Input(_a) {
    var className = _a.className, otherProps = __rest(_a, ["className"]);
    return (<input className={classNames('form-control', className)} {...omit(otherProps, 'children')}/>);
}
//# sourceMappingURL=input.jsx.map