import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Pagination from 'app/components/pagination';
import Button from 'app/components/button';
import SimilarSpectrum from 'app/components/similarSpectrum';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { Panel, PanelBody } from 'app/components/panels';
import space from 'app/styles/space';
import Item from './item';
import Toolbar from './toolbar';
var List = /** @class */ (function (_super) {
    __extends(List, _super);
    function List() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showAllItems: false,
        };
        _this.renderEmpty = function () { return (<Panel>
      <PanelBody>
        <EmptyStateWarning small withIcon={false}>
          {t('No issues with a similar stack trace have been found.')}
        </EmptyStateWarning>
      </PanelBody>
    </Panel>); };
        _this.handleShowAll = function () {
            _this.setState({ showAllItems: true });
        };
        return _this;
    }
    List.prototype.render = function () {
        var _a = this.props, orgId = _a.orgId, groupId = _a.groupId, project = _a.project, items = _a.items, filteredItems = _a.filteredItems, pageLinks = _a.pageLinks, onMerge = _a.onMerge;
        var showAllItems = this.state.showAllItems;
        var hasHiddenItems = !!filteredItems.length;
        var hasResults = items.length > 0 || hasHiddenItems;
        var itemsWithFiltered = items.concat((showAllItems && filteredItems) || []);
        if (!hasResults) {
            return this.renderEmpty();
        }
        return (<Wrapper className="similar-list-container">
        <Header>
          <SimilarSpectrum />
        </Header>
        <Toolbar onMerge={onMerge}/>
        <div className="similar-list">
          {itemsWithFiltered.map(function (item) { return (<Item key={item.issue.id} orgId={orgId} groupId={groupId} project={project} {...item}/>); })}

          {hasHiddenItems && !showAllItems && (<Footer>
              <Button onClick={this.handleShowAll}>
                {t('Show %s issues below threshold', filteredItems.length)}
              </Button>
            </Footer>)}
        </div>
        <Pagination pageLinks={pageLinks}/>
      </Wrapper>);
    };
    List.defaultProps = {
        filteredItems: [],
    };
    return List;
}(React.Component));
export default List;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"])), space(1));
var Footer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"])), space(1.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=list.jsx.map