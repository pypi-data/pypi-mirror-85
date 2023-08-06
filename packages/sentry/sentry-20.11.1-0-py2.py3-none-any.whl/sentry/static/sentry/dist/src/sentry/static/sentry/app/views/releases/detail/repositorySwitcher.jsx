import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var RepositorySwitcher = /** @class */ (function (_super) {
    __extends(RepositorySwitcher, _super);
    function RepositorySwitcher() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.dropdownButton = React.createRef();
        _this.handleRepoFilterChange = function (activeRepo) {
            var _a = _this.props, router = _a.router, location = _a.location;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, activeRepo: activeRepo }) }));
        };
        return _this;
    }
    RepositorySwitcher.prototype.componentDidMount = function () {
        this.setButtonDropDownWidth();
    };
    RepositorySwitcher.prototype.setButtonDropDownWidth = function () {
        var _a, _b;
        var dropdownButtonWidth = (_b = (_a = this.dropdownButton) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (dropdownButtonWidth) {
            this.setState({ dropdownButtonWidth: dropdownButtonWidth });
        }
    };
    RepositorySwitcher.prototype.render = function () {
        var _this = this;
        var _a = this.props, activeRepository = _a.activeRepository, repositories = _a.repositories;
        var dropdownButtonWidth = this.state.dropdownButtonWidth;
        var activeRepo = activeRepository === null || activeRepository === void 0 ? void 0 : activeRepository.name;
        return (<StyledDropdownControl minMenuWidth={dropdownButtonWidth} label={<React.Fragment>
            <FilterText>{t('Filter') + ":"}</FilterText>
            {activeRepo}
          </React.Fragment>} buttonProps={{ forwardRef: this.dropdownButton }}>
        {repositories
            .map(function (repo) { return repo.name; })
            .map(function (repoName) { return (<DropdownItem key={repoName} onSelect={_this.handleRepoFilterChange} eventKey={repoName} isActive={repoName === activeRepo}>
              <RepoLabel>{repoName}</RepoLabel>
            </DropdownItem>); })}
      </StyledDropdownControl>);
    };
    return RepositorySwitcher;
}(React.PureComponent));
export default RepositorySwitcher;
var StyledDropdownControl = styled(DropdownControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  > *:nth-child(2) {\n    right: auto;\n    width: auto;\n    ", "\n    border-radius: ", ";\n    border-top-left-radius: 0px;\n    border: 1px solid ", ";\n    top: calc(100% - 1px);\n  }\n"], ["\n  margin-bottom: ", ";\n  > *:nth-child(2) {\n    right: auto;\n    width: auto;\n    ", "\n    border-radius: ", ";\n    border-top-left-radius: 0px;\n    border: 1px solid ", ";\n    top: calc(100% - 1px);\n  }\n"])), space(1), function (p) { return p.minMenuWidth && "min-width: calc(" + p.minMenuWidth + "px + 10px);"; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.button.default.border; });
var FilterText = styled('em')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-style: normal;\n  color: ", ";\n  margin-right: ", ";\n"], ["\n  font-style: normal;\n  color: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.gray300; }, space(0.5));
var RepoLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=repositorySwitcher.jsx.map