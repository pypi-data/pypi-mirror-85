import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import LoadingIndicator from 'app/components/loadingIndicator';
import theme from 'app/utils/theme';
var defaultProps = {
    isLoading: false,
    isReloading: false,
    maskBackgroundColor: theme.white,
};
export default function LoadingContainer(props) {
    var className = props.className, children = props.children, isReloading = props.isReloading, isLoading = props.isLoading, maskBackgroundColor = props.maskBackgroundColor;
    var isLoadingOrReloading = isLoading || isReloading;
    return (<Container className={className}>
      {isLoadingOrReloading && (<div>
          <LoadingMask isReloading={isReloading} maskBackgroundColor={maskBackgroundColor}/>
          <Indicator />
        </div>)}
      {children}
    </Container>);
}
LoadingContainer.defaultProps = defaultProps;
LoadingContainer.propTypes = {
    isLoading: PropTypes.bool.isRequired,
    isReloading: PropTypes.bool.isRequired,
    children: PropTypes.node,
};
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var LoadingMask = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  z-index: 1;\n  background-color: ", ";\n  width: 100%;\n  height: 100%;\n  opacity: ", ";\n"], ["\n  position: absolute;\n  z-index: 1;\n  background-color: ", ";\n  width: 100%;\n  height: 100%;\n  opacity: ", ";\n"])), function (p) { return p.maskBackgroundColor; }, function (p) { return (p.isReloading ? '0.6' : '1'); });
var Indicator = styled(LoadingIndicator)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  z-index: 3;\n  width: 100%;\n"], ["\n  position: absolute;\n  z-index: 3;\n  width: 100%;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=loadingContainer.jsx.map