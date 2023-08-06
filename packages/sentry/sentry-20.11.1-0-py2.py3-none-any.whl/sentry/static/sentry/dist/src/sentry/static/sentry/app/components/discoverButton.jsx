import { __rest } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import Feature from 'app/components/acl/feature';
/**
 * Provide a button that turns itself off if the current organization
 * doesn't have access to discover results.
 */
function DiscoverButton(_a) {
    var children = _a.children, buttonProps = __rest(_a, ["children"]);
    return (<Feature features={['organizations:discover-basic']}>
      {function (_a) {
        var hasFeature = _a.hasFeature;
        return (<Button disabled={!hasFeature} {...buttonProps}>
          {children}
        </Button>);
    }}
    </Feature>);
}
export default DiscoverButton;
//# sourceMappingURL=discoverButton.jsx.map