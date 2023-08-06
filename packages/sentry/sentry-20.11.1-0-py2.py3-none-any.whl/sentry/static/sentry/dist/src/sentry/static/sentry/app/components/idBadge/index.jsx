import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ErrorBoundary from 'app/components/errorBoundary';
import getBadge from './getBadge';
/**
 * Public interface for all "id badges":
 * Organization, project, team, user
 */
var IdBadge = function (props) {
    var componentBadge = getBadge(props);
    if (!componentBadge) {
        throw new Error('IdBadge: required property missing (organization, project, team, member, user) or misconfigured');
    }
    return <InlineErrorBoundary mini>{componentBadge}</InlineErrorBoundary>;
};
export default IdBadge;
var InlineErrorBoundary = styled(ErrorBoundary)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: transparent;\n  border-color: transparent;\n  display: flex;\n  align-items: center;\n  margin-bottom: 0;\n  box-shadow: none;\n  padding: 0; /* Because badges dont have any padding, so this should make the boundary fit well */\n"], ["\n  background-color: transparent;\n  border-color: transparent;\n  display: flex;\n  align-items: center;\n  margin-bottom: 0;\n  box-shadow: none;\n  padding: 0; /* Because badges dont have any padding, so this should make the boundary fit well */\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map