import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { ListGroup, ListGroupItem } from 'app/components/listGroup';
import FileChange from 'app/components/fileChange';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
function Collapsed(props) {
    return (<ListGroupItem centered>
      <a onClick={props.onClick}>
        {tn('Show %s collapsed file', 'Show %s collapsed files', props.count)}
      </a>
    </ListGroupItem>);
}
var RepositoryFileSummary = /** @class */ (function (_super) {
    __extends(RepositoryFileSummary, _super);
    function RepositoryFileSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            collapsed: true,
        };
        _this.onCollapseToggle = function () {
            _this.setState({
                collapsed: !_this.state.collapsed,
            });
        };
        return _this;
    }
    RepositoryFileSummary.prototype.render = function () {
        var _a = this.props, repository = _a.repository, fileChangeSummary = _a.fileChangeSummary, collapsable = _a.collapsable, maxWhenCollapsed = _a.maxWhenCollapsed;
        var files = Object.keys(fileChangeSummary);
        var fileCount = files.length;
        files.sort();
        if (this.state.collapsed && collapsable && fileCount > maxWhenCollapsed) {
            files = files.slice(0, maxWhenCollapsed);
        }
        var numCollapsed = fileCount - files.length;
        var canCollapse = collapsable && fileCount > maxWhenCollapsed;
        return (<Container>
        <h5>
          {tn('%s file changed in ' + repository, '%s files changed in ' + repository, fileCount)}
        </h5>
        <ListGroup striped>
          {files.map(function (filename) {
            var authors = fileChangeSummary[filename].authors;
            return (<FileChange key={filename} filename={filename} authors={authors ? Object.values(authors) : []}/>);
        })}
          {numCollapsed > 0 && (<Collapsed onClick={this.onCollapseToggle} count={numCollapsed}/>)}
          {numCollapsed === 0 && canCollapse && (<ListGroupItem centered>
              <a onClick={this.onCollapseToggle}>{t('Collapse')}</a>
            </ListGroupItem>)}
        </ListGroup>
      </Container>);
    };
    RepositoryFileSummary.defaultProps = {
        collapsable: true,
        maxWhenCollapsed: 5,
    };
    return RepositoryFileSummary;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export default RepositoryFileSummary;
var templateObject_1;
//# sourceMappingURL=repositoryFileSummary.jsx.map