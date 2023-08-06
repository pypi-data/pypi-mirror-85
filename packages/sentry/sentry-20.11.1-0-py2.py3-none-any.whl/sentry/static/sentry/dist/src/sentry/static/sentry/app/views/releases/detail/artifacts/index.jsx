import { __extends } from "tslib";
import React from 'react';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import routeTitleGen from 'app/utils/routeTitle';
import { formatVersion } from 'app/utils/formatters';
import withOrganization from 'app/utils/withOrganization';
import AlertLink from 'app/components/alertLink';
import { Main } from 'app/components/layouts/thirds';
import { ReleaseContext } from '..';
var ReleaseArtifacts = /** @class */ (function (_super) {
    __extends(ReleaseArtifacts, _super);
    function ReleaseArtifacts() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReleaseArtifacts.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Artifacts - Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseArtifacts.prototype.renderBody = function () {
        var project = this.context.project;
        var _a = this.props, params = _a.params, organization = _a.organization;
        return (<Main fullWidth>
        <AlertLink to={"/settings/" + organization.slug + "/projects/" + project.slug + "/source-maps/" + encodeURIComponent(params.release) + "/"} priority="info">
          {tct('Artifacts were moved to [sourceMaps] in Settings.', {
            sourceMaps: <u>{t('Source Maps')}</u>,
        })}
        </AlertLink>
      </Main>);
    };
    ReleaseArtifacts.contextType = ReleaseContext;
    return ReleaseArtifacts;
}(AsyncView));
export default withOrganization(ReleaseArtifacts);
//# sourceMappingURL=index.jsx.map