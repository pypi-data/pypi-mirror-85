import { __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import Button from 'app/components/button';
import { t } from 'app/locale';
import { IconDelete } from 'app/icons';
import QueryFields from './queryFields';
import { parseSavedQuery } from '../utils';
import { ButtonSpinner, QueryActions, QueryActionsGroup, SavedQueryAction, } from '../styles';
var EditSavedQuery = /** @class */ (function (_super) {
    __extends(EditSavedQuery, _super);
    function EditSavedQuery(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            savedQueryName: props.savedQuery.name,
        };
        return _this;
    }
    EditSavedQuery.prototype.handleUpdateName = function (savedQueryName) {
        this.setState({ savedQueryName: savedQueryName });
    };
    EditSavedQuery.prototype.hasChanges = function () {
        var _a = this.props, queryBuilder = _a.queryBuilder, savedQuery = _a.savedQuery;
        var hasChanged = !isEqual(parseSavedQuery(savedQuery), queryBuilder.getInternal()) ||
            this.state.savedQueryName !== savedQuery.name;
        return hasChanged;
    };
    EditSavedQuery.prototype.render = function () {
        var _this = this;
        var _a = this.props, queryBuilder = _a.queryBuilder, savedQuery = _a.savedQuery, isFetchingQuery = _a.isFetchingQuery, onUpdateField = _a.onUpdateField, onRunQuery = _a.onRunQuery, onDeleteQuery = _a.onDeleteQuery, onSaveQuery = _a.onSaveQuery, isLoading = _a.isLoading;
        var savedQueryName = this.state.savedQueryName;
        return (<QueryFields queryBuilder={queryBuilder} onUpdateField={onUpdateField} isLoading={isLoading} savedQuery={savedQuery} savedQueryName={this.state.savedQueryName} onUpdateName={function (name) { return _this.handleUpdateName(name); }} actions={<QueryActions>
            <QueryActionsGroup>
              <div>
                <Button size="xsmall" onClick={onRunQuery} priority="primary" busy={isFetchingQuery}>
                  {t('Run')}
                  {isFetchingQuery && <ButtonSpinner />}
                </Button>
              </div>
              <div>
                <Button size="xsmall" onClick={function () { return onSaveQuery(savedQueryName); }} disabled={!this.hasChanges()}>
                  {t('Save')}
                </Button>
              </div>
            </QueryActionsGroup>
            <div>
              <SavedQueryAction to="" data-test-id="delete" onClick={onDeleteQuery}>
                <IconDelete />
              </SavedQueryAction>
            </div>
          </QueryActions>}/>);
    };
    return EditSavedQuery;
}(React.Component));
export default EditSavedQuery;
//# sourceMappingURL=editSavedQuery.jsx.map