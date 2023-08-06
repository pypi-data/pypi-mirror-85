import { __assign, __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { IconChevron } from 'app/icons';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import { callIfFunction } from 'app/utils/callIfFunction';
var defaultProps = {
    size: 'small',
    onCursor: function (cursor, path, query, _direction) {
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), { cursor: cursor }),
        });
    },
};
var Pagination = /** @class */ (function (_super) {
    __extends(Pagination, _super);
    function Pagination() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Pagination.prototype.render = function () {
        var _a = this.props, className = _a.className, onCursor = _a.onCursor, pageLinks = _a.pageLinks, size = _a.size;
        if (!pageLinks) {
            return null;
        }
        var location = this.context.location;
        var path = this.props.to || location.pathname;
        var query = location.query;
        var links = parseLinkHeader(pageLinks);
        var previousDisabled = links.previous.results === false;
        var nextDisabled = links.next.results === false;
        return (<div className={className}>
        <ButtonBar merged>
          <Button icon={<IconChevron direction="left" size="sm" color={previousDisabled ? 'gray200' : 'gray500'}/>} aria-label={t('Previous')} size={size} disabled={previousDisabled} onClick={function () {
            callIfFunction(onCursor, links.previous.cursor, path, query, -1);
        }}/>
          <Button icon={<IconChevron direction="right" size="sm" color={nextDisabled ? 'gray200' : 'gray500'}/>} aria-label={t('Next')} size={size} disabled={nextDisabled} onClick={function () {
            callIfFunction(onCursor, links.next.cursor, path, query, 1);
        }}/>
        </ButtonBar>
      </div>);
    };
    Pagination.propTypes = {
        pageLinks: PropTypes.string,
        to: PropTypes.string,
        onCursor: PropTypes.func,
        className: PropTypes.string,
    };
    Pagination.contextTypes = {
        location: PropTypes.object,
    };
    Pagination.defaultProps = defaultProps;
    return Pagination;
}(React.Component));
export default styled(Pagination)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: 20px 0 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: 20px 0 0 0;\n"])));
var templateObject_1;
//# sourceMappingURL=pagination.jsx.map