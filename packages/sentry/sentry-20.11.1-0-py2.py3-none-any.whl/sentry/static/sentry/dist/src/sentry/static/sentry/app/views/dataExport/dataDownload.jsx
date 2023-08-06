import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconDownload } from 'app/icons';
import { ExportQueryType } from 'app/components/dataExport';
import DateTime from 'app/components/dateTime';
import AsyncView from 'app/views/asyncView';
import Layout from 'app/views/auth/layout';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
export var DownloadStatus;
(function (DownloadStatus) {
    DownloadStatus["Early"] = "EARLY";
    DownloadStatus["Valid"] = "VALID";
    DownloadStatus["Expired"] = "EXPIRED";
})(DownloadStatus || (DownloadStatus = {}));
var DataDownload = /** @class */ (function (_super) {
    __extends(DataDownload, _super);
    function DataDownload() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DataDownload.prototype.getTitle = function () {
        return t('Download Center');
    };
    DataDownload.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, dataExportId = _a.dataExportId;
        return [['download', "/organizations/" + orgId + "/data-export/" + dataExportId + "/"]];
    };
    DataDownload.prototype.getActionLink = function (queryType) {
        var orgId = this.props.params.orgId;
        switch (queryType) {
            case ExportQueryType.IssuesByTag:
                return "/organizations/" + orgId + "/issues/";
            case ExportQueryType.Discover:
                return "/organizations/" + orgId + "/discover/queries/";
            default:
                return '/';
        }
    };
    DataDownload.prototype.renderDate = function (date) {
        if (!date) {
            return null;
        }
        var d = new Date(date);
        return (<strong>
        <DateTime date={d}/>
      </strong>);
    };
    DataDownload.prototype.renderEarly = function () {
        return (<React.Fragment>
        <Header>
          <h3>
            {t('What are')}
            <i>{t(' you ')}</i>
            {t('doing here?')}
          </h3>
        </Header>
        <Body>
          <p>
            {t("Not that its any of our business, but were you invited to this page? It's just that we don't exactly remember emailing you about it.")}
          </p>
          <p>{t("Close this window and we'll email you when your download is ready.")}</p>
        </Body>
      </React.Fragment>);
    };
    DataDownload.prototype.renderExpired = function () {
        var query = this.state.download.query;
        var actionLink = this.getActionLink(query.type);
        return (<React.Fragment>
        <Header>
          <h3>{t('This is awkward.')}</h3>
        </Header>
        <Body>
          <p>
            {t("That link expired, so your download doesn't live here anymore. Just picked up one day and left town.")}
          </p>
          <p>
            {t('Make a new one with your latest data. Your old download will never see it coming.')}
          </p>
          <DownloadButton href={actionLink} priority="primary">
            {t('Start a New Download')}
          </DownloadButton>
        </Body>
      </React.Fragment>);
    };
    DataDownload.prototype.openInDiscover = function () {
        var info = this.state.download.query.info;
        var orgId = this.props.params.orgId;
        var to = {
            pathname: "/organizations/" + orgId + "/discover/results/",
            query: info,
        };
        browserHistory.push(to);
    };
    DataDownload.prototype.renderOpenInDiscover = function () {
        var _this = this;
        var _a = this.state.download.query, query = _a === void 0 ? {
            type: ExportQueryType.IssuesByTag,
            info: {},
        } : _a;
        // default to IssuesByTag because we dont want to
        // display this unless we're sure its a discover query
        var _b = query.type, type = _b === void 0 ? ExportQueryType.IssuesByTag : _b;
        return type === 'Discover' ? (<React.Fragment>
        <p>{t('Need to make changes?')}</p>
        <Button priority="primary" onClick={function () { return _this.openInDiscover(); }}>
          {t('Open in Discover')}
        </Button>
        <br />
      </React.Fragment>) : null;
    };
    DataDownload.prototype.renderValid = function () {
        var _a = this.state.download, dateExpired = _a.dateExpired, checksum = _a.checksum;
        var _b = this.props.params, orgId = _b.orgId, dataExportId = _b.dataExportId;
        return (<React.Fragment>
        <Header>
          <h3>{t('All done.')}</h3>
        </Header>
        <Body>
          <p>{t("See, that wasn't so bad. Your data is all ready for download.")}</p>
          <Button priority="primary" icon={<IconDownload />} href={"/api/0/organizations/" + orgId + "/data-export/" + dataExportId + "/?download=true"}>
            {t('Download CSV')}
          </Button>
          <p>
            {t("That link won't last forever — it expires:")}
            <br />
            {this.renderDate(dateExpired)}
          </p>
          {this.renderOpenInDiscover()}
          <p>
            <small>
              <strong>SHA1:{checksum}</strong>
            </small>
            <br />
            {tct('Need help verifying? [link].', {
            link: (<a href="https://docs.sentry.io/product/discover-queries/query-builder/#filter-by-table-columns" target="_blank" rel="noopener noreferrer">
                  {t('Check out our docs')}
                </a>),
        })}
          </p>
        </Body>
      </React.Fragment>);
    };
    DataDownload.prototype.renderError = function () {
        var _a;
        var err = this.state.errors.download;
        var errDetail = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail;
        return (<Layout>
        <main>
          <Header>
            <h3>
              {err.status} - {err.statusText}
            </h3>
          </Header>
          {errDetail && (<Body>
              <p>{errDetail}</p>
            </Body>)}
        </main>
      </Layout>);
    };
    DataDownload.prototype.renderContent = function () {
        var download = this.state.download;
        switch (download.status) {
            case DownloadStatus.Early:
                return this.renderEarly();
            case DownloadStatus.Expired:
                return this.renderExpired();
            default:
                return this.renderValid();
        }
    };
    DataDownload.prototype.renderBody = function () {
        return (<Layout>
        <main>{this.renderContent()}</main>
      </Layout>);
    };
    return DataDownload;
}(AsyncView));
var Header = styled('header')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: ", " 40px 0;\n  h3 {\n    font-size: 24px;\n    margin: 0 0 ", " 0;\n  }\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: ", " 40px 0;\n  h3 {\n    font-size: 24px;\n    margin: 0 0 ", " 0;\n  }\n"])), function (p) { return p.theme.border; }, space(3), space(3));
var Body = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " 40px;\n  max-width: 500px;\n  p {\n    margin: ", " 0;\n  }\n"], ["\n  padding: ", " 40px;\n  max-width: 500px;\n  p {\n    margin: ", " 0;\n  }\n"])), space(2), space(1.5));
var DownloadButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1.5));
export default DataDownload;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=dataDownload.jsx.map