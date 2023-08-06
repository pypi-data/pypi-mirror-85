import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import Button from 'app/components/button';
import { t, tct } from 'app/locale';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import QueryFields from './queryFields';
import { createSavedQuery, generateQueryName } from '../utils';
import { ButtonSpinner, QueryActions, QueryActionsGroup, QueryFieldsContainer, } from '../styles';
var NewQuery = /** @class */ (function (_super) {
    __extends(NewQuery, _super);
    function NewQuery() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NewQuery.prototype.saveQuery = function () {
        var _a = this.props, organization = _a.organization, queryBuilder = _a.queryBuilder;
        var savedQueryName = generateQueryName();
        var data = __assign(__assign({}, queryBuilder.getInternal()), { name: savedQueryName });
        createSavedQuery(organization, data)
            .then(function (savedQuery) {
            addSuccessMessage(tct('Successfully saved query [name]', { name: savedQueryName }));
            browserHistory.push({
                pathname: "/organizations/" + organization.slug + "/discover/saved/" + savedQuery.id + "/",
                query: { editing: true },
            });
        })
            .catch(function (err) {
            var message = (err && err.detail) || t('Could not save query');
            addErrorMessage(message);
        });
    };
    NewQuery.prototype.render = function () {
        var _this = this;
        var _a = this.props, queryBuilder = _a.queryBuilder, onRunQuery = _a.onRunQuery, onReset = _a.onReset, isFetchingQuery = _a.isFetchingQuery, onUpdateField = _a.onUpdateField, isLoading = _a.isLoading;
        return (<QueryFieldsContainer>
        <QueryFields queryBuilder={queryBuilder} onUpdateField={onUpdateField} isLoading={isLoading} actions={<QueryActions>
              <QueryActionsGroup>
                <div>
                  <Button size="xsmall" onClick={onRunQuery} priority="primary" busy={isFetchingQuery}>
                    {t('Run')}
                    {isFetchingQuery && <ButtonSpinner />}
                  </Button>
                </div>
                <div>
                  <Button size="xsmall" onClick={function () { return _this.saveQuery(); }}>
                    {t('Save')}
                  </Button>
                </div>
              </QueryActionsGroup>
              <div>
                <Button size="xsmall" onClick={onReset}>
                  {t('Reset')}
                </Button>
              </div>
            </QueryActions>}/>
      </QueryFieldsContainer>);
    };
    return NewQuery;
}(React.Component));
export default NewQuery;
//# sourceMappingURL=newQuery.jsx.map