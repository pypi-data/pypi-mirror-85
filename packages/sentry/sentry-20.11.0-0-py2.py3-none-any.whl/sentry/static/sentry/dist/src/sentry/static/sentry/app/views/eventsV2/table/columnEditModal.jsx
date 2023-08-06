import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import ExternalLink from 'app/components/links/externalLink';
import { DISCOVER2_DOCS_URL } from 'app/constants';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import ColumnEditCollection from './columnEditCollection';
var ColumnEditModal = /** @class */ (function (_super) {
    __extends(ColumnEditModal, _super);
    function ColumnEditModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            columns: _this.props.columns,
        };
        _this.handleChange = function (columns) {
            _this.setState({ columns: columns });
        };
        _this.handleApply = function () {
            _this.props.onApply(_this.state.columns);
            _this.props.closeModal();
        };
        return _this;
    }
    ColumnEditModal.prototype.componentDidMount = function () {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'discover_v2.column_editor.open',
            eventName: 'Discoverv2: Open column editor',
            organization_id: parseInt(organization.id, 10),
        });
    };
    ColumnEditModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, tagKeys = _a.tagKeys, measurementKeys = _a.measurementKeys, organization = _a.organization;
        return (<React.Fragment>
        <Header>
          <h4>{t('Edit Columns')}</h4>
        </Header>
        <Body>
          <Instruction>
            {tct('To stack events, add [functionLink: functions] f(x) that may take in additional parameters. [tagFieldLink: Tag and field] columns will help you view more details about the events (i.e. title).', {
            functionLink: (<ExternalLink href="https://docs.sentry.io/product/discover-queries/query-builder/#filter-by-table-columns"/>),
            tagFieldLink: (<ExternalLink href="https://docs.sentry.io/product/sentry-basics/search/#event-properties"/>),
        })}
          </Instruction>
          <ColumnEditCollection organization={organization} columns={this.state.columns} tagKeys={tagKeys} measurementKeys={measurementKeys} onChange={this.handleChange}/>
        </Body>
        <Footer>
          <ButtonBar gap={1}>
            <Button priority="default" href={DISCOVER2_DOCS_URL} external>
              {t('Read the Docs')}
            </Button>
            <Button label={t('Apply')} priority="primary" onClick={this.handleApply}>
              {t('Apply')}
            </Button>
          </ButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return ColumnEditModal;
}(React.Component));
var Instruction = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var modalCss = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: auto;\n      max-width: 750px;\n      margin-left: -375px;\n    }\n  }\n"], ["\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: auto;\n      max-width: 750px;\n      margin-left: -375px;\n    }\n  }\n"])), theme.breakpoints[0]);
export default ColumnEditModal;
export { modalCss };
var templateObject_1, templateObject_2;
//# sourceMappingURL=columnEditModal.jsx.map