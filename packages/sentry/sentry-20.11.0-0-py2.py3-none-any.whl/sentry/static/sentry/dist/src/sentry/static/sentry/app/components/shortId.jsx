import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
import AutoSelectText from 'app/components/autoSelectText';
var ShortId = /** @class */ (function (_super) {
    __extends(ShortId, _super);
    function ShortId() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ShortId.prototype.render = function () {
        var _a = this.props, shortId = _a.shortId, avatar = _a.avatar;
        if (!shortId) {
            return null;
        }
        return (<StyledShortId {...this.props}>
        {avatar}
        <StyledAutoSelectText avatar={!!avatar}>{shortId}</StyledAutoSelectText>
      </StyledShortId>);
    };
    ShortId.propTypes = {
        shortId: PropTypes.string.isRequired,
        avatar: PropTypes.node,
    };
    return ShortId;
}(React.Component));
export default ShortId;
var StyledShortId = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-family: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  font-family: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])), function (p) { return p.theme.text.familyMono; });
var StyledAutoSelectText = styled(AutoSelectText, { shouldForwardProp: isPropValid })(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n  min-width: 0;\n"], ["\n  margin-left: ", ";\n  min-width: 0;\n"])), function (p) { return p.avatar && '0.5em'; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=shortId.jsx.map