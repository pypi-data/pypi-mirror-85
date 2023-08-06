import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import ErrorLevel from 'app/components/events/errorLevel';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var EventMessage = function (_a) {
    var className = _a.className, level = _a.level, levelIndicatorSize = _a.levelIndicatorSize, message = _a.message, annotations = _a.annotations;
    return (<div className={className}>
    {level && (<StyledErrorLevel size={levelIndicatorSize} level={level}>
        {level}
      </StyledErrorLevel>)}

    {message && <Message>{message}</Message>}

    {annotations}
  </div>);
};
EventMessage.propTypes = {
    level: PropTypes.oneOf(['error', 'fatal', 'info', 'warning', 'sample']),
    levelIndicatorSize: PropTypes.string,
    message: PropTypes.node,
    annotations: PropTypes.node,
    className: PropTypes.string,
};
var StyledEventMessage = styled(EventMessage)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: relative;\n  line-height: 1.2;\n  overflow: hidden;\n"], ["\n  display: flex;\n  align-items: center;\n  position: relative;\n  line-height: 1.2;\n  overflow: hidden;\n"])));
var StyledErrorLevel = styled(ErrorLevel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Message = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n  width: auto;\n  max-height: 38px;\n"], ["\n  ", "\n  width: auto;\n  max-height: 38px;\n"])), overflowEllipsis);
export default StyledEventMessage;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventMessage.jsx.map