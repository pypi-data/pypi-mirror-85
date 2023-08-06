import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import isEqual from 'lodash/isEqual';
import map from 'lodash/map';
import styled from '@emotion/styled';
import LoadingIndicator from 'app/components/loadingIndicator';
import { IconClose } from 'app/icons/iconClose';
import { queryToObj, objToQuery } from 'app/utils/stream';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import IssueListTagFilter from './tagFilter';
var IssueListSidebar = /** @class */ (function (_super) {
    __extends(IssueListSidebar, _super);
    function IssueListSidebar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            queryObj: queryToObj(_this.props.query),
            textFilter: queryToObj(_this.props.query).__text,
        };
        _this.onSelectTag = function (tag, value) {
            var newQuery = __assign({}, _this.state.queryObj);
            if (value) {
                newQuery[tag.key] = value;
            }
            else {
                delete newQuery[tag.key];
            }
            _this.setState({
                queryObj: newQuery,
            }, _this.onQueryChange);
        };
        _this.onTextChange = function (evt) {
            _this.setState({ textFilter: evt.target.value });
        };
        _this.onTextFilterSubmit = function (evt) {
            evt && evt.preventDefault();
            var newQueryObj = __assign(__assign({}, _this.state.queryObj), { __text: _this.state.textFilter });
            _this.setState({
                queryObj: newQueryObj,
            }, _this.onQueryChange);
        };
        _this.onQueryChange = function () {
            var query = objToQuery(_this.state.queryObj);
            _this.props.onQueryChange && _this.props.onQueryChange(query);
        };
        _this.onClearSearch = function () {
            _this.setState({
                textFilter: '',
            }, _this.onTextFilterSubmit);
        };
        return _this;
    }
    IssueListSidebar.prototype.componentWillReceiveProps = function (nextProps) {
        // If query was updated by another source (e.g. SearchBar),
        // clobber state of sidebar with new query.
        var query = objToQuery(this.state.queryObj);
        if (!isEqual(nextProps.query, query)) {
            var queryObj = queryToObj(nextProps.query);
            this.setState({
                queryObj: queryObj,
                textFilter: queryObj.__text,
            });
        }
    };
    IssueListSidebar.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, tagValueLoader = _a.tagValueLoader, tags = _a.tags;
        return (<StreamSidebar>
        {loading ? (<LoadingIndicator />) : (<React.Fragment>
            <StreamTagFilter>
              <StyledHeader>{t('Text')}</StyledHeader>
              <form onSubmit={this.onTextFilterSubmit}>
                <input className="form-control" placeholder={t('Search title and culprit text body')} onChange={this.onTextChange} value={this.state.textFilter}/>
                {this.state.textFilter && (<StyledIconClose size="xs" onClick={this.onClearSearch}/>)}
              </form>
              <StyledHr />
            </StreamTagFilter>

            {map(tags, function (tag) { return (<IssueListTagFilter value={_this.state.queryObj[tag.key]} key={tag.key} tag={tag} onSelect={_this.onSelectTag} tagValueLoader={tagValueLoader}/>); })}
          </React.Fragment>)}
      </StreamSidebar>);
    };
    IssueListSidebar.propTypes = {
        tags: PropTypes.objectOf(SentryTypes.Tag).isRequired,
        query: PropTypes.string,
        onQueryChange: PropTypes.func.isRequired,
        loading: PropTypes.bool,
        tagValueLoader: PropTypes.func.isRequired,
    };
    IssueListSidebar.defaultProps = {
        tags: {},
        query: '',
        onQueryChange: function () { },
    };
    return IssueListSidebar;
}(React.Component));
export default IssueListSidebar;
var StreamSidebar = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  width: 100%;\n"], ["\n  display: flex;\n  flex-direction: column;\n  width: 100%;\n"])));
var StyledIconClose = styled(IconClose)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: pointer;\n  position: absolute;\n  top: 13px;\n  right: 10px;\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  cursor: pointer;\n  position: absolute;\n  top: 13px;\n  right: 10px;\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
var StyledHeader = styled('h6')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space(1));
var StreamTagFilter = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var StyledHr = styled('hr')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: ", " 0 0;\n"], ["\n  margin: ", " 0 0;\n"])), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebar.jsx.map