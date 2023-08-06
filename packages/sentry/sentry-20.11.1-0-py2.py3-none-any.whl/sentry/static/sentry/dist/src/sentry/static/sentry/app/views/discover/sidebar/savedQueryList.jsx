import { __extends } from "tslib";
import React from 'react';
import moment from 'moment';
import getDynamicText from 'app/utils/getDynamicText';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t, tct } from 'app/locale';
import { fetchSavedQueries } from '../utils';
import { Fieldset, LoadingContainer, SavedQueryList, SavedQueryListItem, SavedQueryLink, SavedQueryUpdated, } from '../styles';
var SavedQueries = /** @class */ (function (_super) {
    __extends(SavedQueries, _super);
    function SavedQueries() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            data: [],
            savedQuery: null,
        };
        return _this;
    }
    SavedQueries.getDerivedStateFromProps = function (nextProps, prevState) {
        var nextState = {};
        if (nextProps.savedQuery && nextProps.savedQuery !== prevState.savedQuery) {
            nextState.data = prevState.data.map(function (q) {
                return q.id === nextProps.savedQuery.id ? nextProps.savedQuery : q;
            });
        }
        return nextState;
    };
    SavedQueries.prototype.componentDidMount = function () {
        this.fetchAll();
    };
    SavedQueries.prototype.componentDidUpdate = function (prevProps) {
        // Re-fetch on deletion
        if (!this.props.savedQuery && prevProps.savedQuery) {
            this.fetchAll();
        }
    };
    SavedQueries.prototype.fetchAll = function () {
        var _this = this;
        fetchSavedQueries(this.props.organization)
            .then(function (data) {
            _this.setState({ isLoading: false, data: data });
        })
            .catch(function () {
            _this.setState({ isLoading: false });
        });
    };
    SavedQueries.prototype.renderLoading = function () {
        return (<Fieldset>
        <LoadingContainer>
          <LoadingIndicator mini/>
        </LoadingContainer>
      </Fieldset>);
    };
    SavedQueries.prototype.renderEmpty = function () {
        return <Fieldset>{t('No saved queries')}</Fieldset>;
    };
    SavedQueries.prototype.renderListItem = function (query) {
        var savedQuery = this.props.savedQuery;
        var id = query.id, name = query.name, dateUpdated = query.dateUpdated;
        var organization = this.props.organization;
        var relativeLink = "/organizations/" + organization.slug + "/discover/saved/" + id + "/";
        return (<SavedQueryListItem key={id} isActive={savedQuery && savedQuery.id === id}>
        <SavedQueryLink to={relativeLink}>
          {getDynamicText({ value: name, fixed: 'saved query' })}
          <SavedQueryUpdated>
            {tct('Updated [date] (UTC)', {
            date: getDynamicText({
                value: moment.utc(dateUpdated).format('MMM DD HH:mm:ss'),
                fixed: 'update-date',
            }),
        })}
          </SavedQueryUpdated>
        </SavedQueryLink>
      </SavedQueryListItem>);
    };
    SavedQueries.prototype.renderList = function () {
        var _this = this;
        var data = this.state.data;
        return data.length
            ? data.map(function (query) { return _this.renderListItem(query); })
            : this.renderEmpty();
    };
    SavedQueries.prototype.render = function () {
        var isLoading = this.state.isLoading;
        return (<SavedQueryList>
        {isLoading ? this.renderLoading() : this.renderList()}
      </SavedQueryList>);
    };
    return SavedQueries;
}(React.Component));
export default SavedQueries;
//# sourceMappingURL=savedQueryList.jsx.map