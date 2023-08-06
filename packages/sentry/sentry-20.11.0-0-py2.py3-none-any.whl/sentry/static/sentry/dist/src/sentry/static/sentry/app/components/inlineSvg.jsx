import { __makeTemplateObject, __rest } from "tslib";
import pickBy from 'lodash/pickBy';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
var InlineSvg = styled(React.forwardRef(
// eslint-disable-next-line react/prop-types
function (_a, ref) {
    var src = _a.src, size = _a.size, width = _a.width, height = _a.height, props = __rest(_a, ["src", "size", "width", "height"]);
    var _b = require("../icons/" + src + ".svg").default, id = _b.id, viewBox = _b.viewBox;
    return (<svg {...pickBy(props, function (_value, key) { return isPropValid(key); })} ref={ref} viewBox={viewBox} width={width || size || '1em'} height={height || size || '1em'}>
          <use href={"#" + id} xlinkHref={"#" + id}/>
        </svg>);
}))(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
InlineSvg.propTypes = {
    src: PropTypes.string.isRequired,
    size: PropTypes.string,
    width: PropTypes.string,
    height: PropTypes.string,
};
export default InlineSvg;
var templateObject_1;
//# sourceMappingURL=inlineSvg.jsx.map