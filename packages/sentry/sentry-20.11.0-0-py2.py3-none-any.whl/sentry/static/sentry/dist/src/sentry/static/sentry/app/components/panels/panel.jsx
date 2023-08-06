import { __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import PanelBody from 'app/components/panels/panelBody';
import PanelHeader from 'app/components/panels/panelHeader';
import space from 'app/styles/space';
var Panel = styled(function (_a) {
    var title = _a.title, body = _a.body, _dashedBorder = _a.dashedBorder, props = __rest(_a, ["title", "body", "dashedBorder"]);
    var hasHeaderAndBody = !!title && !!body;
    return !hasHeaderAndBody ? (<div {...props}/>) : (<div {...props}>
        <PanelHeader>{title}</PanelHeader>
        <PanelBody>{body}</PanelBody>
      </div>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: ", ";\n  border-radius: ", ";\n  border: 1px\n    ", ";\n  box-shadow: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"], ["\n  background: ", ";\n  border-radius: ", ";\n  border: 1px\n    ", ";\n  box-shadow: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"])), function (p) { return (p.dashedBorder ? p.theme.backgroundSecondary : p.theme.background); }, function (p) { return p.theme.borderRadius; }, function (p) { return (p.dashedBorder ? 'dashed' + p.theme.gray300 : 'solid ' + p.theme.border); }, function (p) { return (p.dashedBorder ? 'none' : p.theme.dropShadowLight); }, space(3));
Panel.propTypes = {
    /**
     * When `title` and `body` are defined, use as children to `<PanelHeader>`
     * and `<PanelBody>` respectively.
     */
    title: PropTypes.node,
    body: PropTypes.node,
    dashedBorder: PropTypes.bool,
};
export default Panel;
var templateObject_1;
//# sourceMappingURL=panel.jsx.map