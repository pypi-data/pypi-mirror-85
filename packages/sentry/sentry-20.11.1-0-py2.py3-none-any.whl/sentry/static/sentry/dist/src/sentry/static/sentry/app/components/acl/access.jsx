import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import Alert from 'app/components/alert';
import { IconInfo } from 'app/icons';
import SentryTypes from 'app/sentryTypes';
import withConfig from 'app/utils/withConfig';
import withOrganization from 'app/utils/withOrganization';
import { isRenderFunc } from 'app/utils/isRenderFunc';
var DEFAULT_NO_ACCESS_MESSAGE = (<Alert type="error" icon={<IconInfo size="md"/>}>
    {t('You do not have sufficient permissions to access this.')}
  </Alert>);
var defaultProps = {
    renderNoAccessMessage: false,
    isSuperuser: false,
    requireAll: true,
    access: [],
};
/**
 * Component to handle access restrictions.
 */
var Access = /** @class */ (function (_super) {
    __extends(Access, _super);
    function Access() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Access.prototype.render = function () {
        var _a = this.props, organization = _a.organization, config = _a.config, access = _a.access, requireAll = _a.requireAll, isSuperuser = _a.isSuperuser, renderNoAccessMessage = _a.renderNoAccessMessage, children = _a.children;
        var orgAccess = (organization || { access: [] }).access;
        var method = requireAll ? 'every' : 'some';
        var hasAccess = !access || access[method](function (acc) { return orgAccess.includes(acc); });
        var hasSuperuser = !!(config.user && config.user.isSuperuser);
        var renderProps = {
            hasAccess: hasAccess,
            hasSuperuser: hasSuperuser,
        };
        var render = hasAccess && (!isSuperuser || hasSuperuser);
        if (!render && typeof renderNoAccessMessage === 'function') {
            return renderNoAccessMessage(renderProps);
        }
        else if (!render && renderNoAccessMessage) {
            return DEFAULT_NO_ACCESS_MESSAGE;
        }
        if (isRenderFunc(children)) {
            return children(renderProps);
        }
        return render ? children : null;
    };
    Access.propTypes = {
        organization: SentryTypes.Organization,
        access: PropTypes.arrayOf(PropTypes.string),
        requireAll: PropTypes.bool,
        isSuperuser: PropTypes.bool,
        renderNoAccessMessage: PropTypes.oneOfType([PropTypes.func, PropTypes.bool]),
        children: PropTypes.oneOfType([PropTypes.func, PropTypes.node]),
    };
    Access.defaultProps = defaultProps;
    return Access;
}(React.Component));
export default withOrganization(withConfig(Access));
//# sourceMappingURL=access.jsx.map