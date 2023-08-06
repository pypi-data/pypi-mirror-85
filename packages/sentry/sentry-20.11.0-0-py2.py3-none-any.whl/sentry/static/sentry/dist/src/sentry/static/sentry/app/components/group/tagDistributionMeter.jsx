import { __assign, __extends } from "tslib";
import React from 'react';
import { deviceNameMapper, loadDeviceListModule } from 'app/components/deviceName';
import TagDistributionMeter from 'app/components/tagDistributionMeter';
var GroupTagDistributionMeter = /** @class */ (function (_super) {
    __extends(GroupTagDistributionMeter, _super);
    function GroupTagDistributionMeter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
        };
        return _this;
    }
    GroupTagDistributionMeter.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupTagDistributionMeter.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return (this.state.loading !== nextState.loading ||
            this.state.error !== nextState.error ||
            this.props.tag !== nextProps.tag ||
            this.props.name !== nextProps.name ||
            this.props.totalValues !== nextProps.totalValues ||
            this.props.topValues !== nextProps.topValues);
    };
    GroupTagDistributionMeter.prototype.fetchData = function () {
        var _this = this;
        this.setState({
            loading: true,
            error: false,
        });
        loadDeviceListModule()
            .then(function (iOSDeviceList) {
            _this.setState({
                iOSDeviceList: iOSDeviceList,
                error: false,
                loading: false,
            });
        })
            .catch(function () {
            _this.setState({
                error: true,
                loading: false,
            });
        });
    };
    GroupTagDistributionMeter.prototype.render = function () {
        var _a = this.props, organization = _a.organization, group = _a.group, tag = _a.tag, totalValues = _a.totalValues, topValues = _a.topValues;
        var _b = this.state, loading = _b.loading, error = _b.error, iOSDeviceList = _b.iOSDeviceList;
        var url = "/organizations/" + organization.slug + "/issues/" + group.id + "/tags/" + tag + "/";
        var segments = topValues
            ? topValues.map(function (value) { return (__assign(__assign({}, value), { name: iOSDeviceList
                    ? deviceNameMapper(value.name || '', iOSDeviceList) || ''
                    : value.name, url: url })); })
            : [];
        return (<TagDistributionMeter title={tag} totalValues={totalValues} isLoading={loading} hasError={error} segments={segments}/>);
    };
    return GroupTagDistributionMeter;
}(React.Component));
export default GroupTagDistributionMeter;
//# sourceMappingURL=tagDistributionMeter.jsx.map