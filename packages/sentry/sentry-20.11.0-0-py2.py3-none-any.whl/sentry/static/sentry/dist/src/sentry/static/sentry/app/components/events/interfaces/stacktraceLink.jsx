import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { getIntegrationIcon } from 'app/utils/integrationUtil';
import { OpenInContainer, OpenInLink, OpenInName } from './openInContextLine';
var StacktraceLink = /** @class */ (function (_super) {
    __extends(StacktraceLink, _super);
    function StacktraceLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(StacktraceLink.prototype, "project", {
        get: function () {
            // we can't use the withProject HoC on an the issue page
            // so we ge around that by using the withProjects HoC
            // and look up the project from the list
            var _a = this.props, projects = _a.projects, event = _a.event;
            return projects.find(function (project) { return project.id === event.projectID; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "match", {
        get: function () {
            return this.state.match;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "config", {
        get: function () {
            return this.match.config;
        },
        enumerable: false,
        configurable: true
    });
    StacktraceLink.prototype.getEndpoints = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, frame = _c.frame, event = _c.event;
        var project = this.project;
        if (!project) {
            throw new Error('Unable to find project');
        }
        var commitId = (_b = (_a = event.release) === null || _a === void 0 ? void 0 : _a.lastCommit) === null || _b === void 0 ? void 0 : _b.id;
        return [
            [
                'match',
                "/projects/" + organization.slug + "/" + project.slug + "/stacktrace-link/",
                { query: { file: frame.filename, commitId: commitId } },
            ],
        ];
    };
    StacktraceLink.prototype.renderLoading = function () {
        //TODO: Add loading
        return null;
    };
    StacktraceLink.prototype.renderNoMatch = function () {
        //TODO: Improve UI
        return null;
    };
    StacktraceLink.prototype.renderMatchNoUrl = function () {
        //TODO: Improve UI
        return <OpenInContainer columnQuantity={2}>No Match</OpenInContainer>;
    };
    StacktraceLink.prototype.renderMatchWithUrl = function (config, url) {
        url = url + "#L" + this.props.frame.lineNo;
        return (<OpenInContainer columnQuantity={2}>
        <div>{t('Open this line in')}</div>
        <OpenInLink href={url} openInNewTab>
          {getIntegrationIcon(config.provider.key)}
          <OpenInName>{config.provider.name}</OpenInName>
        </OpenInLink>
      </OpenInContainer>);
    };
    StacktraceLink.prototype.renderBody = function () {
        var _a = this.match || {}, config = _a.config, sourceUrl = _a.sourceUrl;
        if (config && sourceUrl) {
            return this.renderMatchWithUrl(config, sourceUrl);
        }
        else if (config) {
            return this.renderMatchNoUrl();
        }
        else {
            return this.renderNoMatch();
        }
    };
    return StacktraceLink;
}(AsyncComponent));
export default withProjects(withOrganization(StacktraceLink));
//# sourceMappingURL=stacktraceLink.jsx.map