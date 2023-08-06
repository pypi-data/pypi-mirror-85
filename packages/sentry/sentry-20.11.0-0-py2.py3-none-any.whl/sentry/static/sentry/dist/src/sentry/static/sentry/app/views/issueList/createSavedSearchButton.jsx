import { __assign, __extends } from "tslib";
import React from 'react';
import Modal from 'react-bootstrap/lib/Modal';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import { createSavedSearch } from 'app/actionCreators/savedSearches';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import { TextField } from 'app/components/forms';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import { IconAdd } from 'app/icons';
var CreateSavedSearchButton = /** @class */ (function (_super) {
    __extends(CreateSavedSearchButton, _super);
    function CreateSavedSearchButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isModalOpen: false,
            isSaving: false,
            name: '',
            error: null,
            query: null,
        };
        _this.onSubmit = function (e) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            var query = _this.state.query || _this.props.query;
            e.preventDefault();
            _this.setState({ isSaving: true });
            addLoadingMessage(t('Saving Changes'));
            createSavedSearch(api, organization.slug, _this.state.name, query)
                .then(function (_data) {
                _this.onToggle();
                _this.setState({
                    error: null,
                    isSaving: false,
                });
                clearIndicators();
            })
                .catch(function (err) {
                var error = t('Unable to save your changes.');
                if (err.responseJSON && err.responseJSON.detail) {
                    error = err.responseJSON.detail;
                }
                _this.setState({
                    error: error,
                    isSaving: false,
                });
                clearIndicators();
            });
        };
        _this.onToggle = function (event) {
            var newState = __assign(__assign({}, _this.state), { isModalOpen: !_this.state.isModalOpen });
            if (newState.isModalOpen === false) {
                newState.name = '';
                newState.error = null;
                newState.query = null;
            }
            _this.setState(newState);
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }
        };
        _this.handleChangeName = function (val) {
            _this.setState({ name: String(val) });
        };
        _this.handleChangeQuery = function (val) {
            _this.setState({ query: String(val) });
        };
        return _this;
    }
    CreateSavedSearchButton.prototype.render = function () {
        var _a = this.state, isSaving = _a.isSaving, isModalOpen = _a.isModalOpen, error = _a.error;
        var _b = this.props, organization = _b.organization, query = _b.query, buttonClassName = _b.buttonClassName, iconOnly = _b.iconOnly, withTooltip = _b.withTooltip;
        return (<Access organization={organization} access={['org:write']}>
        <Button title={withTooltip ? t('Add to organization saved searches') : undefined} onClick={this.onToggle} data-test-id="save-current-search" size="zero" borderless type="button" aria-label={t('Add to organization saved searches')} icon={<IconAdd size="xs"/>} className={buttonClassName}>
          {!iconOnly && t('Create Saved Search')}
        </Button>
        <Modal show={isModalOpen} animation={false} onHide={this.onToggle}>
          <form onSubmit={this.onSubmit}>
            <div className="modal-header">
              <h4>{t('Save Current Search')}</h4>
            </div>

            <div className="modal-body">
              {this.state.error && (<div className="alert alert-error alert-block">{error}</div>)}

              <p>{t('All team members will now have access to this search.')}</p>
              <TextField key="name" name="name" label={t('Name')} placeholder="e.g. My Search Results" required onChange={this.handleChangeName}/>
              <TextField key="query" name="query" label={t('Query')} value={query} required onChange={this.handleChangeQuery}/>
            </div>
            <div className="modal-footer">
              <Button priority="default" size="small" disabled={isSaving} onClick={this.onToggle} style={{ marginRight: space(1) }}>
                {t('Cancel')}
              </Button>
              <Button priority="primary" size="small" disabled={isSaving}>
                {t('Save')}
              </Button>
            </div>
          </form>
        </Modal>
      </Access>);
    };
    return CreateSavedSearchButton;
}(React.Component));
export default withApi(CreateSavedSearchButton);
//# sourceMappingURL=createSavedSearchButton.jsx.map