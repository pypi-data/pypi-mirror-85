import { __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { imageStyle } from 'app/components/avatar/styles';
var COLORS = [
    '#4674ca',
    '#315cac',
    '#57be8c',
    '#3fa372',
    '#f9a66d',
    '#ec5e44',
    '#e63717',
    '#f868bc',
    '#6c5fc7',
    '#4e3fb4',
    '#57b1be',
    '#847a8c',
];
function hashIdentifier(identifier) {
    identifier += '';
    var hash = 0;
    for (var i = 0; i < identifier.length; i++) {
        hash += identifier.charCodeAt(i);
    }
    return hash;
}
function getColor(identifier) {
    // Gray if the identifier is not set
    if (identifier === undefined) {
        return '#847a8c';
    }
    var id = hashIdentifier(identifier);
    return COLORS[id % COLORS.length];
}
function getInitials(displayName) {
    var names = ((displayName && displayName.trim()) || '?').split(' ');
    // Use Array.from as slicing and substring() work on ucs2 segments which
    // results in only getting half of any 4+ byte character.
    var initials = Array.from(names[0])[0];
    if (names.length > 1) {
        initials += Array.from(names[names.length - 1])[0];
    }
    return initials.toUpperCase();
}
/**
 * Also see avatar.py. Anything changed in this file (how colors are selected,
 * the svg, etc) will also need to be changed there.
 */
var LetterAvatar = styled(function (_a) {
    var identifier = _a.identifier, displayName = _a.displayName, _round = _a.round, forwardedRef = _a.forwardedRef, props = __rest(_a, ["identifier", "displayName", "round", "forwardedRef"]);
    return (<svg ref={forwardedRef} viewBox="0 0 120 120" {...props}>
      <rect x="0" y="0" width="120" height="120" rx="15" ry="15" fill={getColor(identifier)}/>
      <text x="50%" y="50%" fontSize="65" style={{ dominantBaseline: 'central' }} textAnchor="middle" fill="#FFFFFF">
        {getInitials(displayName)}
      </text>
    </svg>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), imageStyle);
LetterAvatar.propTypes = {
    identifier: PropTypes.string,
    displayName: PropTypes.string,
    round: PropTypes.bool,
};
LetterAvatar.defaultProps = {
    round: false,
};
export default React.forwardRef(function (props, ref) { return (<LetterAvatar forwardedRef={ref} {...props}/>); });
var templateObject_1;
//# sourceMappingURL=letterAvatar.jsx.map