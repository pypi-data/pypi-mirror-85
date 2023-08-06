import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconChevron } from 'app/icons';
import Button from 'app/components/button';
var Pagination = /** @class */ (function (_super) {
    __extends(Pagination, _super);
    function Pagination() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Pagination.prototype.render = function () {
        var _a = this.props, getPreviousPage = _a.getPreviousPage, getNextPage = _a.getNextPage, previous = _a.previous, next = _a.next;
        return (<PaginationButtons className="btn-group">
        <Button className="btn" disabled={!previous} size="xsmall" icon={<IconChevron direction="left" size="xs"/>} onClick={getPreviousPage}/>
        <Button className="btn" disabled={!next} size="xsmall" icon={<IconChevron direction="right" size="xs"/>} onClick={getNextPage}/>
      </PaginationButtons>);
    };
    return Pagination;
}(React.Component));
export default Pagination;
var PaginationButtons = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var templateObject_1;
//# sourceMappingURL=pagination.jsx.map