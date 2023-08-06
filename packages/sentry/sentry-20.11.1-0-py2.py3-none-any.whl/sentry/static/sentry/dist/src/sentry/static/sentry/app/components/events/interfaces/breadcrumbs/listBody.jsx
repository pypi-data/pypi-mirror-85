import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import Time from './time';
import Data from './data';
import Category from './category';
import Icon from './icon';
import Level from './level';
import { GridCell, GridCellLeft } from './styles';
import { BreadcrumbType } from './types';
var ListBody = React.memo(function (_a) {
    var orgId = _a.orgId, event = _a.event, breadcrumb = _a.breadcrumb, relativeTime = _a.relativeTime, displayRelativeTime = _a.displayRelativeTime, searchTerm = _a.searchTerm, isLastItem = _a.isLastItem;
    var hasError = breadcrumb.type === BreadcrumbType.ERROR;
    return (<React.Fragment>
        <GridCellLeft hasError={hasError} isLastItem={isLastItem}>
          <Tooltip title={breadcrumb.description}>
            <Icon icon={breadcrumb.icon} color={breadcrumb.color}/>
          </Tooltip>
        </GridCellLeft>
        <GridCellCategory hasError={hasError} isLastItem={isLastItem}>
          <Category category={breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category} searchTerm={searchTerm}/>
        </GridCellCategory>
        <GridCell hasError={hasError} isLastItem={isLastItem}>
          <Data event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm}/>
        </GridCell>
        <GridCell hasError={hasError} isLastItem={isLastItem}>
          <Level level={breadcrumb.level} searchTerm={searchTerm}/>
        </GridCell>
        <GridCell hasError={hasError} isLastItem={isLastItem}>
          <Time timestamp={breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.timestamp} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm}/>
        </GridCell>
      </React.Fragment>);
});
export default ListBody;
var GridCellCategory = styled(GridCell)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var templateObject_1;
//# sourceMappingURL=listBody.jsx.map