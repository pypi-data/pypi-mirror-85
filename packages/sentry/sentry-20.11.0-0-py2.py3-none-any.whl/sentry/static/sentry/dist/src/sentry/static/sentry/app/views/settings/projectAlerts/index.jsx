import React from 'react';
import Access from 'app/components/acl/access';
import Feature from 'app/components/acl/feature';
var ProjectAlerts = function (_a) {
    var children = _a.children, organization = _a.organization;
    return (<Access organization={organization} access={['project:write']}>
    {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Feature organization={organization} features={['incidents']}>
        {function (_a) {
            var hasMetricAlerts = _a.hasFeature;
            return (<React.Fragment>
            {React.isValidElement(children) &&
                React.cloneElement(children, {
                    organization: organization,
                    canEditRule: hasAccess,
                    hasMetricAlerts: hasMetricAlerts,
                })}
          </React.Fragment>);
        }}
      </Feature>);
    }}
  </Access>);
};
export default ProjectAlerts;
//# sourceMappingURL=index.jsx.map