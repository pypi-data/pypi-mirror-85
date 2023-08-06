import { __extends } from "tslib";
import React from 'react';
import { IconClose } from 'app/icons/iconClose';
import PageHeading from 'app/components/pageHeading';
import { QueryPanelContainer, QueryPanelTitle, QueryPanelCloseLink } from '../styles';
var QueryPanel = /** @class */ (function (_super) {
    __extends(QueryPanel, _super);
    function QueryPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    QueryPanel.prototype.render = function () {
        var _a = this.props, title = _a.title, onClose = _a.onClose;
        return (<QueryPanelContainer>
        <QueryPanelTitle>
          <PageHeading>{title}</PageHeading>

          <QueryPanelCloseLink to="" onClick={onClose}>
            <IconClose color="gray200"/>
          </QueryPanelCloseLink>
        </QueryPanelTitle>
        {this.props.children}
      </QueryPanelContainer>);
    };
    return QueryPanel;
}(React.Component));
export default QueryPanel;
//# sourceMappingURL=queryPanel.jsx.map