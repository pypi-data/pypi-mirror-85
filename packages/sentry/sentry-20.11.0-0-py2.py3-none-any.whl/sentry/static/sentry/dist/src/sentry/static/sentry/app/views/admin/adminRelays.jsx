import { __extends } from "tslib";
import React from 'react';
import moment from 'moment';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import ResultGrid from 'app/components/resultGrid';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
var prettyDate = function (x) { return moment(x).format('ll LTS'); };
var AdminRelays = /** @class */ (function (_super) {
    __extends(AdminRelays, _super);
    function AdminRelays() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
        };
        return _this;
    }
    AdminRelays.prototype.onDelete = function (key) {
        var _this = this;
        this.setState({ loading: true });
        this.props.api.request("/relays/" + key + "/", {
            method: 'DELETE',
            success: function () { return _this.setState({ loading: false }); },
            error: function () { return _this.setState({ loading: false }); },
        });
    };
    AdminRelays.prototype.getRow = function (row) {
        var _this = this;
        return [
            <td key="id">
        <strong>{row.relayId}</strong>
      </td>,
            <td key="key">{row.publicKey}</td>,
            <td key="firstSeen" style={{ textAlign: 'right' }}>
        {prettyDate(row.firstSeen)}
      </td>,
            <td key="lastSeen" style={{ textAlign: 'right' }}>
        {prettyDate(row.lastSeen)}
      </td>,
            <td key="tools" style={{ textAlign: 'right' }}>
        <span className="editor-tools">
          <LinkWithConfirmation className="danger" title="Remove" message={t('Are you sure you wish to delete this relay?')} onConfirm={function () { return _this.onDelete(row.id); }}>
            {t('Remove')}
          </LinkWithConfirmation>
        </span>
      </td>,
        ];
    };
    AdminRelays.prototype.render = function () {
        var columns = [
            <th key="id" style={{ width: 350, textAlign: 'left' }}>
        Relay
      </th>,
            <th key="key">Public Key</th>,
            <th key="firstSeen" style={{ width: 150, textAlign: 'right' }}>
        First seen
      </th>,
            <th key="lastSeen" style={{ width: 150, textAlign: 'right' }}>
        Last seen
      </th>,
            <th key="tools"/>,
        ];
        return (<div>
        <h3>{t('Relays')}</h3>
        <ResultGrid path="/manage/relays/" endpoint="/relays/" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch={false} sortOptions={[
            ['firstSeen', 'First seen'],
            ['lastSeen', 'Last seen'],
            ['relayId', 'Relay ID'],
        ]} defaultSort="firstSeen" {...this.props}/>
      </div>);
    };
    return AdminRelays;
}(React.Component));
export { AdminRelays };
export default withApi(AdminRelays);
//# sourceMappingURL=adminRelays.jsx.map