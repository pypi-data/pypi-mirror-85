import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconQuestion, IconSettings } from 'app/icons';
import { Panel, PanelAlert, PanelTable } from 'app/components/panels';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import { t, tn } from 'app/locale';
import Access from 'app/components/acl/access';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import AutoSelectText from 'app/components/autoSelectText';
import Button from 'app/components/button';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import TimeSince from 'app/components/timeSince';
import formGroups from 'app/data/forms/processingIssues';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var MESSAGES = {
    native_no_crashed_thread: t('No crashed thread found in crash report'),
    native_internal_failure: t('Internal failure when attempting to symbolicate: {error}'),
    native_bad_dsym: t('The debug information file used was broken.'),
    native_missing_optionally_bundled_dsym: t('An optional debug information file was missing.'),
    native_missing_dsym: t('A required debug information file was missing.'),
    native_missing_system_dsym: t('A system debug information file was missing.'),
    native_missing_symbol: t('Could not resolve one or more frames in debug information file.'),
    native_simulator_frame: t('Encountered an unprocessable simulator frame.'),
    native_unknown_image: t('A binary image is referenced that is unknown.'),
    proguard_missing_mapping: t('A proguard mapping file was missing.'),
    proguard_missing_lineno: t('A proguard mapping file does not contain line info.'),
};
var HELP_LINKS = {
    native_missing_dsym: 'https://docs.sentry.io/clients/cocoa/dsym/',
    native_bad_dsym: 'https://docs.sentry.io/clients/cocoa/dsym/',
    native_missing_system_dsym: 'https://docs.sentry.io/server/dsym/',
    native_missing_symbol: 'https://docs.sentry.io/server/dsym/',
};
var ProjectProcessingIssues = /** @class */ (function (_super) {
    __extends(ProjectProcessingIssues, _super);
    function ProjectProcessingIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            formData: {},
            loading: true,
            reprocessing: false,
            expected: 0,
            error: false,
            processingIssues: null,
            pageLinks: null,
        };
        _this.fetchData = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                expected: _this.state.expected + 2,
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/", {
                success: function (data) {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        loading: expected > 0,
                        formData: data.options,
                    });
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/processingissues/?detailed=1", {
                success: function (data, _, jqXHR) {
                    var _a;
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: false,
                        loading: expected > 0,
                        processingIssues: data,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        _this.sendReprocessing = function () {
            _this.setState({
                reprocessing: true,
            });
            addLoadingMessage(t('Started reprocessing\u2026'));
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/reprocessing/", {
                method: 'POST',
                success: function () {
                    _this.fetchData();
                    _this.setState({
                        reprocessing: false,
                    });
                },
                error: function () {
                    _this.setState({
                        reprocessing: false,
                    });
                },
                complete: function () {
                    clearIndicators();
                },
            });
        };
        _this.discardEvents = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                expected: _this.state.expected + 1,
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/processingissues/discard/", {
                method: 'DELETE',
                success: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: false,
                        loading: expected > 0,
                    });
                    // TODO (billyvg): Need to fix this
                    // we reload to get rid of the badge in the sidebar
                    window.location.reload();
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        _this.deleteProcessingIssues = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                expected: _this.state.expected + 1,
            });
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/processingissues/", {
                method: 'DELETE',
                success: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: false,
                        loading: expected > 0,
                    });
                    // TODO (billyvg): Need to fix this
                    // we reload to get rid of the badge in the sidebar
                    window.location.reload();
                },
                error: function () {
                    var expected = _this.state.expected - 1;
                    _this.setState({
                        expected: expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        return _this;
    }
    ProjectProcessingIssues.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectProcessingIssues.prototype.renderDebugTable = function () {
        var body;
        var _a = this.state, loading = _a.loading, error = _a.error, processingIssues = _a.processingIssues;
        if (loading) {
            body = this.renderLoading();
        }
        else if (error) {
            body = <LoadingError onRetry={this.fetchData}/>;
        }
        else if ((processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.hasIssues) || (processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.resolveableIssues) || (processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.issuesProcessing)) {
            body = this.renderResults();
        }
        else {
            body = this.renderEmpty();
        }
        return body;
    };
    ProjectProcessingIssues.prototype.renderLoading = function () {
        return (<div className="box">
        <LoadingIndicator />
      </div>);
    };
    ProjectProcessingIssues.prototype.renderEmpty = function () {
        return (<Panel>
        <EmptyStateWarning>
          <p>{t('Good news! There are no processing issues.')}</p>
        </EmptyStateWarning>
      </Panel>);
    };
    ProjectProcessingIssues.prototype.getProblemDescription = function (item) {
        var msg = MESSAGES[item.type];
        return msg || t('Unknown Error');
    };
    ProjectProcessingIssues.prototype.getImageName = function (path) {
        var pathSegments = path.split(/^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/');
        return pathSegments[pathSegments.length - 1];
    };
    ProjectProcessingIssues.prototype.renderProblem = function (item) {
        var description = this.getProblemDescription(item);
        var helpLink = HELP_LINKS[item.type];
        return (<div className="processing-issue">
        <span className="description">{description}</span>{' '}
        {helpLink && (<a href={helpLink} className="help-link">
            <IconQuestion size="xs"/>
          </a>)}
      </div>);
    };
    ProjectProcessingIssues.prototype.renderDetails = function (item) {
        var dsymUUID = null;
        var dsymName = null;
        var dsymArch = null;
        if (item.data._scope === 'native') {
            if (item.data.image_uuid) {
                dsymUUID = <code className="uuid">{item.data.image_uuid}</code>;
            }
            if (item.data.image_path) {
                dsymName = <em>{this.getImageName(item.data.image_path)}</em>;
            }
            if (item.data.image_arch) {
                dsymArch = item.data.image_arch;
            }
        }
        return (<span>
        {dsymUUID && <span> {dsymUUID}</span>}
        {dsymArch && <span> {dsymArch}</span>}
        {dsymName && <span> (for {dsymName})</span>}
      </span>);
    };
    ProjectProcessingIssues.prototype.renderResolveButton = function () {
        var issues = this.state.processingIssues;
        if (issues === null || this.state.reprocessing) {
            return null;
        }
        if (issues.resolveableIssues <= 0) {
            return null;
        }
        var fixButton = tn('Click here to trigger processing for %s pending event', 'Click here to trigger processing for %s pending events', issues.resolveableIssues);
        return (<div className="alert alert-block alert-info">
        Pro Tip: <a onClick={this.sendReprocessing}>{fixButton}</a>
      </div>);
    };
    ProjectProcessingIssues.prototype.renderResults = function () {
        var _this = this;
        var _a;
        var processingIssues = this.state.processingIssues;
        var fixLink = processingIssues ? processingIssues.signedLink : false;
        var fixLinkBlock = null;
        if (fixLink) {
            fixLinkBlock = (<div className="panel panel-info">
          <div className="panel-heading">
            <h3>{t('Having trouble uploading debug informations? We can help!')}</h3>
          </div>
          <div className="panel-body">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>
                {t("Paste this command into your shell and we'll attempt to upload the missing symbols from your machine:")}
              </label>
              <AutoSelectText className="form-control disabled" style={{ marginBottom: 6 }}>
                curl -sL "{fixLink}" | bash
              </AutoSelectText>
            </div>
          </div>
        </div>);
        }
        var processingRow = null;
        if (processingIssues && processingIssues.issuesProcessing > 0) {
            processingRow = (<StyledPanelAlert type="info" icon={<IconSettings size="sm"/>}>
          {tn('Reprocessing %s event …', 'Reprocessing %s events …', processingIssues.issuesProcessing)}
        </StyledPanelAlert>);
        }
        return (<div>
        {fixLinkBlock}
        <h3>
          {t('Pending Issues')}
          <Access access={['project:write']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<Button size="small" className="pull-right" disabled={!hasAccess} onClick={function () { return _this.discardEvents(); }}>
                {t('Discard all')}
              </Button>);
        }}
          </Access>
        </h3>
        <PanelTable headers={[t('Problem'), t('Details'), t('Events'), t('Last seen')]}>
          {processingRow}
          {(_a = processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.issues) === null || _a === void 0 ? void 0 : _a.map(function (item, idx) { return (<React.Fragment key={idx}>
              <div>{_this.renderProblem(item)}</div>
              <div>{_this.renderDetails(item)}</div>
              <div>{item.numEvents + ''}</div>
              <div>
                <TimeSince date={item.lastSeen}/>
              </div>
            </React.Fragment>); })}
        </PanelTable>
      </div>);
    };
    ProjectProcessingIssues.prototype.renderReprocessingSettings = function () {
        var access = new Set(this.props.organization.access);
        if (this.state.loading) {
            return this.renderLoading();
        }
        var formData = this.state.formData;
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return (<Form saveOnBlur onSubmitSuccess={this.deleteProcessingIssues} apiEndpoint={"/projects/" + orgId + "/" + projectId + "/"} apiMethod="PUT" initialData={formData}>
        <JsonForm access={access} forms={formGroups} renderHeader={function () { return (<PanelAlert type="warning">
              <TextBlock noMargin>
                {t("Reprocessing does not apply to Minidumps. Even when enabled,\n                    Minidump events with processing issues will show up in the\n                    issues stream immediately and cannot be reprocessed.")}
              </TextBlock>
            </PanelAlert>); }}/>
      </Form>);
    };
    ProjectProcessingIssues.prototype.render = function () {
        var projectId = this.props.params.projectId;
        var title = t('Processing Issues');
        return (<div>
        <SentryDocumentTitle title={title} objSlug={projectId}/>
        <SettingsPageHeader title={title}/>
        <TextBlock>
          {t("For some platforms the event processing requires configuration or\n          manual action.  If a misconfiguration happens or some necessary\n          steps are skipped, issues can occur during processing. (The most common\n          reason for this is missing debug symbols.) In these cases you can see\n          all the problems here with guides of how to correct them.")}
        </TextBlock>
        {this.renderDebugTable()}
        {this.renderResolveButton()}
        {this.renderReprocessingSettings()}
      </div>);
    };
    return ProjectProcessingIssues;
}(React.Component));
var StyledPanelAlert = styled(PanelAlert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-column: 1/5;\n"], ["\n  grid-column: 1/5;\n"])));
export { ProjectProcessingIssues };
export default withApi(withOrganization(ProjectProcessingIssues));
var templateObject_1;
//# sourceMappingURL=projectProcessingIssues.jsx.map