import { __assign, __extends, __rest } from "tslib";
import { Box } from 'reflexbox';
import PropTypes from 'prop-types';
import React from 'react';
import scrollToElement from 'scroll-to-element';
import * as Sentry from '@sentry/react';
import { defined } from 'app/utils';
import { sanitizeQuerySelector } from 'app/utils/sanitizeQuerySelector';
import FieldFromConfig from './fieldFromConfig';
import FormPanel from './formPanel';
var JsonForm = /** @class */ (function (_super) {
    __extends(JsonForm, _super);
    function JsonForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            highlighted: getLocation(_this.props, _this.context).hash,
        };
        return _this;
    }
    JsonForm.prototype.componentDidMount = function () {
        this.scrollToHash();
    };
    JsonForm.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (getLocation(this.props, this.context).hash !==
            getLocation(nextProps, this.context).hash) {
            var hash = getLocation(nextProps, this.context).hash;
            this.scrollToHash(hash);
            this.setState({ highlighted: hash });
        }
    };
    JsonForm.prototype.scrollToHash = function (toHash) {
        var hash = toHash || getLocation(this.props, this.context).hash;
        if (!hash) {
            return;
        }
        // Push onto callback queue so it runs after the DOM is updated,
        // this is required when navigating from a different page so that
        // the element is rendered on the page before trying to getElementById.
        try {
            scrollToElement(sanitizeQuerySelector(decodeURIComponent(hash)), {
                align: 'middle',
                offset: -100,
            });
        }
        catch (err) {
            Sentry.captureException(err);
        }
    };
    JsonForm.prototype.shouldDisplayForm = function (fields) {
        var fieldsWithVisibleProp = fields.filter(function (field) { return typeof field !== 'function' && defined(field === null || field === void 0 ? void 0 : field.visible); });
        if (fields.length === fieldsWithVisibleProp.length) {
            var _a = this.props, additionalFieldProps_1 = _a.additionalFieldProps, props_1 = __rest(_a, ["additionalFieldProps"]);
            var areAllFieldsHidden = fieldsWithVisibleProp.every(function (field) {
                if (typeof field.visible === 'function') {
                    return !field.visible(__assign(__assign({}, props_1), additionalFieldProps_1));
                }
                return !field.visible;
            });
            return !areAllFieldsHidden;
        }
        return true;
    };
    JsonForm.prototype.renderForm = function (_a) {
        var fields = _a.fields, formPanelProps = _a.formPanelProps, title = _a.title;
        var shouldDisplayForm = this.shouldDisplayForm(fields);
        if (!shouldDisplayForm &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderFooter) &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderHeader)) {
            return null;
        }
        return <FormPanel title={title} fields={fields} {...formPanelProps}/>;
    };
    JsonForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, access = _a.access, fields = _a.fields, title = _a.title, forms = _a.forms, disabled = _a.disabled, features = _a.features, additionalFieldProps = _a.additionalFieldProps, renderFooter = _a.renderFooter, renderHeader = _a.renderHeader, _location = _a.location, otherProps = __rest(_a, ["access", "fields", "title", "forms", "disabled", "features", "additionalFieldProps", "renderFooter", "renderHeader", "location"]);
        var formPanelProps = {
            access: access,
            disabled: disabled,
            features: features,
            additionalFieldProps: additionalFieldProps,
            renderFooter: renderFooter,
            renderHeader: renderHeader,
            highlighted: this.state.highlighted,
        };
        return (<Box {...otherProps}>
        {typeof forms !== 'undefined' &&
            forms.map(function (formGroup, i) { return (<React.Fragment key={i}>
              {_this.renderForm(__assign({ formPanelProps: formPanelProps }, formGroup))}
            </React.Fragment>); })}
        {typeof forms === 'undefined' &&
            typeof fields !== 'undefined' &&
            this.renderForm({ fields: fields, formPanelProps: formPanelProps, title: title })}
      </Box>);
    };
    JsonForm.propTypes = {
        /**
         * Fields that are grouped by "section"
         */
        forms: PropTypes.arrayOf(PropTypes.shape({
            title: PropTypes.string,
            fields: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.func, FieldFromConfig.propTypes.field])),
        })),
        /**
         * If `forms` is not defined, `title` + `fields` must be required.
         * Allows more fine grain control of title/fields
         */
        fields: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.func, FieldFromConfig.propTypes.field])),
        /**
         * Panel title if `forms` is not defined
         */
        title: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
        access: PropTypes.object,
        features: PropTypes.object,
        renderFooter: PropTypes.func,
        /**
         * Renders inside of PanelBody
         */
        renderHeader: PropTypes.func,
        /**
         * Disables the entire form
         */
        disabled: PropTypes.bool,
    };
    JsonForm.contextTypes = {
        location: PropTypes.object,
    };
    JsonForm.defaultProps = {
        additionalFieldProps: {},
    };
    return JsonForm;
}(React.Component));
export default JsonForm;
function getLocation(props, context) {
    return props.location || context.location || {};
}
//# sourceMappingURL=jsonForm.jsx.map