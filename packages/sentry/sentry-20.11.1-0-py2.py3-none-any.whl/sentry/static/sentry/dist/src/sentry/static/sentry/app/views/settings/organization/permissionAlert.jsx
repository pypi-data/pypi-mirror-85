import { __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import Alert from 'app/components/alert';
import { IconWarning } from 'app/icons';
var PermissionAlert = function (_a) {
    var _b = _a.access, access = _b === void 0 ? ['org:write'] : _b, props = __rest(_a, ["access"]);
    return (<Access access={access}>
    {function (_a) {
        var hasAccess = _a.hasAccess;
        return !hasAccess && (<Alert type="warning" icon={<IconWarning size="sm"/>} {...props}>
          {t('These settings can only be edited by users with the organization owner or manager role.')}
        </Alert>);
    }}
  </Access>);
};
PermissionAlert.propTypes = {
    access: PropTypes.arrayOf(PropTypes.string),
};
export default PermissionAlert;
//# sourceMappingURL=permissionAlert.jsx.map