import { __extends, __read } from "tslib";
import debounce from 'lodash/debounce';
import isEqual from 'lodash/isEqual';
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
//! Coordinate with other ExportQueryType (src/sentry/data_export/base.py)
export var ExportQueryType;
(function (ExportQueryType) {
    ExportQueryType["IssuesByTag"] = "Issues-by-Tag";
    ExportQueryType["Discover"] = "Discover";
})(ExportQueryType || (ExportQueryType = {}));
var DataExport = /** @class */ (function (_super) {
    __extends(DataExport, _super);
    function DataExport() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.initialState;
        _this.resetState = function () {
            _this.setState(_this.initialState);
        };
        _this.startDataExport = function () {
            var _a = _this.props, api = _a.api, slug = _a.organization.slug, _b = _a.payload, queryType = _b.queryType, queryInfo = _b.queryInfo;
            _this.setState({ inProgress: true });
            api
                .requestPromise("/organizations/" + slug + "/data-export/", {
                includeAllArgs: true,
                method: 'POST',
                data: {
                    query_type: queryType,
                    query_info: queryInfo,
                },
            })
                .then(function (_a) {
                var _b = __read(_a, 3), _data = _b[0], _ = _b[1], response = _b[2];
                addSuccessMessage((response === null || response === void 0 ? void 0 : response.status) === 201
                    ? t("Sit tight. We'll shoot you an email when your data is ready for download.")
                    : t("It looks like we're already working on it. Sit tight, we'll email you."));
            })
                .catch(function (err) {
                var _a, _b;
                var message = (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : "We tried our hardest, but we couldn't export your data. Give it another go.";
                addErrorMessage(t(message));
                _this.setState({ inProgress: false });
            });
        };
        return _this;
    }
    DataExport.prototype.componentDidUpdate = function (_a) {
        var prevPayload = _a.payload;
        var payload = this.props.payload;
        if (!isEqual(prevPayload, payload))
            this.resetState();
    };
    Object.defineProperty(DataExport.prototype, "initialState", {
        get: function () {
            return {
                inProgress: false,
            };
        },
        enumerable: false,
        configurable: true
    });
    DataExport.prototype.render = function () {
        var inProgress = this.state.inProgress;
        var _a = this.props, children = _a.children, disabled = _a.disabled, icon = _a.icon;
        return (<Feature features={['organizations:discover-query']}>
        {inProgress ? (<Button size="small" priority="default" title="You can get on with your life. We'll email you when your data's ready." {...this.props} disabled icon={icon}>
            {t("We're working on it...")}
          </Button>) : (<Button onClick={debounce(this.startDataExport, 500)} disabled={disabled || false} size="small" priority="default" title="Put your data to work. Start your export and we'll email you when it's finished." icon={icon} {...this.props}>
            {children ? children : t('Export All to CSV')}
          </Button>)}
      </Feature>);
    };
    return DataExport;
}(React.Component));
export { DataExport };
export default withApi(withOrganization(DataExport));
//# sourceMappingURL=dataExport.jsx.map