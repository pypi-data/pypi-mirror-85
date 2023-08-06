import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Breadcrumbs from 'app/components/breadcrumbs';
function BuilderBreadCrumbs(props) {
    var hasMetricAlerts = props.hasMetricAlerts, orgSlug = props.orgSlug, title = props.title;
    return (<StyledBreadcrumbs crumbs={[
        {
            to: hasMetricAlerts
                ? "/organizations/" + orgSlug + "/alerts/"
                : "/organizations/" + orgSlug + "/alerts/rules/",
            label: t('Alerts'),
            preserveGlobalSelection: true,
        },
        {
            label: title,
        },
    ]}/>);
}
var StyledBreadcrumbs = styled(Breadcrumbs)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 18px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 18px;\n  margin-bottom: ", ";\n"])), space(3));
export default BuilderBreadCrumbs;
var templateObject_1;
//# sourceMappingURL=builderBreadCrumbs.jsx.map