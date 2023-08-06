import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { fetchSavedQuery } from 'app/actionCreators/discoverSavedQueries';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import * as Layout from 'app/components/layouts/thirds';
import DiscoverBreadcrumb from './breadcrumb';
import EventInputName from './eventInputName';
import SavedQueryButtonGroup from './savedQuery';
var ResultsHeader = /** @class */ (function (_super) {
    __extends(ResultsHeader, _super);
    function ResultsHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            savedQuery: undefined,
            loading: true,
        };
        return _this;
    }
    ResultsHeader.prototype.componentDidMount = function () {
        if (this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.eventView &&
            this.props.eventView &&
            prevProps.eventView.id !== this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, api = _a.api, eventView = _a.eventView, organization = _a.organization;
        if (typeof eventView.id === 'string') {
            this.setState({ loading: true });
            fetchSavedQuery(api, organization.slug, eventView.id).then(function (savedQuery) {
                _this.setState({ savedQuery: savedQuery, loading: false });
            });
        }
    };
    ResultsHeader.prototype.renderAuthor = function () {
        var _a;
        var eventView = this.props.eventView;
        var savedQuery = this.state.savedQuery;
        // No saved query in use.
        if (!eventView.id) {
            return null;
        }
        var createdBy = ' \u2014 ';
        var lastEdit = ' \u2014 ';
        if (savedQuery !== undefined) {
            createdBy = ((_a = savedQuery.createdBy) === null || _a === void 0 ? void 0 : _a.email) || '\u2014';
            lastEdit = <TimeSince date={savedQuery.dateUpdated}/>;
        }
        return (<Subtitle>
        {t('Created by:')} {createdBy} | {t('Last Edited:')} {lastEdit}
      </Subtitle>);
    };
    ResultsHeader.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, errorCode = _a.errorCode, eventView = _a.eventView, onIncompatibleAlertQuery = _a.onIncompatibleAlertQuery;
        var _b = this.state, savedQuery = _b.savedQuery, loading = _b.loading;
        return (<Layout.Header>
        <Layout.HeaderContent>
          <DiscoverBreadcrumb eventView={eventView} organization={organization} location={location}/>
          <EventInputName savedQuery={savedQuery} organization={organization} eventView={eventView}/>
          {this.renderAuthor()}
        </Layout.HeaderContent>
        <Layout.HeaderActions>
          <SavedQueryButtonGroup location={location} organization={organization} eventView={eventView} savedQuery={savedQuery} savedQueryLoading={loading} disabled={errorCode >= 400 && errorCode < 500} updateCallback={function () { return _this.fetchData(); }} onIncompatibleAlertQuery={onIncompatibleAlertQuery}/>
        </Layout.HeaderActions>
      </Layout.Header>);
    };
    return ResultsHeader;
}(React.Component));
var Subtitle = styled('h4')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.4;\n  color: ", ";\n  margin: 0;\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.4;\n  color: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; });
export default withApi(ResultsHeader);
var templateObject_1;
//# sourceMappingURL=resultsHeader.jsx.map