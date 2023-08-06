import { __extends, __makeTemplateObject } from "tslib";
import { Link } from 'react-router';
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ClippedBox from 'app/components/clippedBox';
import Confirm from 'app/components/confirm';
import { IconDelete } from 'app/icons';
import ProjectKeyCredentials from 'app/views/settings/project/projectKeys/projectKeyCredentials';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
var KeyRow = /** @class */ (function (_super) {
    __extends(KeyRow, _super);
    function KeyRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function () {
            var _a = _this.props, data = _a.data, onRemove = _a.onRemove;
            onRemove(data);
        };
        _this.handleEnable = function () {
            var _a = _this.props, onToggle = _a.onToggle, data = _a.data;
            onToggle(true, data);
        };
        _this.handleDisable = function () {
            var _a = _this.props, onToggle = _a.onToggle, data = _a.data;
            onToggle(false, data);
        };
        return _this;
    }
    KeyRow.prototype.render = function () {
        var _a = this.props, access = _a.access, data = _a.data, routes = _a.routes, location = _a.location, params = _a.params;
        var editUrl = recreateRoute(data.id + "/", { routes: routes, params: params, location: location });
        var controlActive = access.has('project:write');
        var controls = [
            <Button key="edit" to={editUrl} size="small">
        {t('Configure')}
      </Button>,
            <Button key="toggle" size="small" onClick={data.isActive ? this.handleDisable : this.handleEnable} disabled={!controlActive}>
        {data.isActive ? t('Disable') : t('Enable')}
      </Button>,
            <Confirm key="remove" priority="danger" disabled={!controlActive} onConfirm={this.handleRemove} confirmText={t('Remove Key')} message={t('Are you sure you want to remove this key? This action is irreversible.')}>
        <Button size="small" disabled={!controlActive} icon={<IconDelete />}/>
      </Confirm>,
        ];
        return (<Panel>
        <PanelHeader hasButtons>
          <Title disabled={!data.isActive}>
            <PanelHeaderLink to={editUrl}>{data.label}</PanelHeaderLink>
            {!data.isActive && (<small>
                {' \u2014  '}
                {t('Disabled')}
              </small>)}
          </Title>
          <Controls>
            {controls.map(function (c, n) { return (<span key={n}> {c}</span>); })}
          </Controls>
        </PanelHeader>

        <StyledClippedBox clipHeight={300} defaultClipped btnText={t('Expand')}>
          <StyledPanelBody disabled={!data.isActive}>
            <ProjectKeyCredentials projectId={"" + data.projectId} data={data}/>
          </StyledPanelBody>
        </StyledClippedBox>
      </Panel>);
    };
    return KeyRow;
}(React.Component));
export default KeyRow;
var StyledClippedBox = styled(ClippedBox)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  margin: 0;\n  > *:last-child {\n    padding-bottom: ", ";\n  }\n"], ["\n  padding: 0;\n  margin: 0;\n  > *:last-child {\n    padding-bottom: ", ";\n  }\n"])), space(3));
var PanelHeaderLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex: 1;\n  ", ";\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  ", ";\n  margin-right: ", ";\n"])), function (p) { return (p.disabled ? 'opacity: 0.5;' : ''); }, space(1));
var Controls = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n"], ["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n"])), space(1));
var StyledPanelBody = styled(PanelBody)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return (p.disabled ? 'opacity: 0.5;' : ''); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=keyRow.jsx.map