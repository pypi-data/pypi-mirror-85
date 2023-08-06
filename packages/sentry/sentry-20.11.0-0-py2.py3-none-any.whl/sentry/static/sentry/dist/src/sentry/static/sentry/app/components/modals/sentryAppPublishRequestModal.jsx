import { __extends, __makeTemplateObject, __values } from "tslib";
import { Body, Header } from 'react-bootstrap/lib/Modal';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import React from 'react';
import intersection from 'lodash/intersection';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import FormModel from 'app/views/settings/components/forms/model';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import space from 'app/styles/space';
import { SENTRY_APP_PERMISSIONS } from 'app/constants';
/**
 * Given an array of scopes, return the choices the user has picked for each option
 * @param scopes {Array}
 */
var getPermissionSelectionsFromScopes = function (scopes) {
    var e_1, _a;
    var permissions = [];
    try {
        for (var SENTRY_APP_PERMISSIONS_1 = __values(SENTRY_APP_PERMISSIONS), SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next(); !SENTRY_APP_PERMISSIONS_1_1.done; SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next()) {
            var permObj = SENTRY_APP_PERMISSIONS_1_1.value;
            var highestChoice = void 0;
            for (var perm in permObj.choices) {
                var choice = permObj.choices[perm];
                var scopesIntersection = intersection(choice.scopes, scopes);
                if (scopesIntersection.length > 0 &&
                    scopesIntersection.length === choice.scopes.length) {
                    if (!highestChoice || scopesIntersection.length > highestChoice.scopes.length) {
                        highestChoice = choice;
                    }
                }
            }
            if (highestChoice) {
                //we can remove the read part of "Read & Write"
                var label = highestChoice.label.replace('Read & Write', 'Write');
                permissions.push(permObj.resource + " " + label);
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (SENTRY_APP_PERMISSIONS_1_1 && !SENTRY_APP_PERMISSIONS_1_1.done && (_a = SENTRY_APP_PERMISSIONS_1.return)) _a.call(SENTRY_APP_PERMISSIONS_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return permissions;
};
var PublishRequestFormModel = /** @class */ (function (_super) {
    __extends(PublishRequestFormModel, _super);
    function PublishRequestFormModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PublishRequestFormModel.prototype.getTransformedData = function () {
        var data = this.getData();
        //map object to list of questions
        var questionnaire = Array.from(this.fieldDescriptor.values()).map(function (field) {
            //we read the meta for the question that has a react node for the label
            return ({
                question: field.meta || field.label,
                answer: data[field.name],
            });
        });
        return { questionnaire: questionnaire };
    };
    return PublishRequestFormModel;
}(FormModel));
var SentryAppPublishRequestModal = /** @class */ (function (_super) {
    __extends(SentryAppPublishRequestModal, _super);
    function SentryAppPublishRequestModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.form = new PublishRequestFormModel();
        _this.handleSubmitSuccess = function () {
            addSuccessMessage(t('Request to publish %s successful.', _this.props.app.slug));
            _this.props.closeModal();
        };
        _this.handleSubmitError = function () {
            addErrorMessage(t('Request to publish %s fails.', _this.props.app.slug));
        };
        return _this;
    }
    Object.defineProperty(SentryAppPublishRequestModal.prototype, "formFields", {
        get: function () {
            var app = this.props.app;
            var permissions = getPermissionSelectionsFromScopes(app.scopes);
            var permissionQuestionBaseText = 'Please justify why you are requesting each of the following permissions: ';
            var permissionQuestionPlainText = "" + permissionQuestionBaseText + permissions.join(', ') + ".";
            var permissionLabel = (<React.Fragment>
        {permissionQuestionBaseText}
        {permissions.map(function (permission, i) { return (<React.Fragment key={permission}>
            {i > 0 && ', '} <code>{permission}</code>
          </React.Fragment>); })}
        .
      </React.Fragment>);
            //No translations since we need to be able to read this email :)
            var baseFields = [
                {
                    type: 'textarea',
                    required: true,
                    label: 'What does your integration do? Please be as detailed as possible.',
                    autosize: true,
                    rows: 1,
                    inline: false,
                    name: 'question0',
                },
                {
                    type: 'textarea',
                    required: true,
                    label: 'What value does it offer customers?',
                    autosize: true,
                    rows: 1,
                    inline: false,
                    name: 'question1',
                },
                {
                    type: 'textarea',
                    required: true,
                    label: 'Do you operate the web service your integration communicates with?',
                    autosize: true,
                    rows: 1,
                    inline: false,
                    name: 'question2',
                },
            ];
            //Only add the permissions question if there are perms to add
            if (permissions.length > 0) {
                baseFields.push({
                    type: 'textarea',
                    required: true,
                    label: permissionLabel,
                    autosize: true,
                    rows: 1,
                    inline: false,
                    meta: permissionQuestionPlainText,
                    name: 'question3',
                });
            }
            return baseFields;
        },
        enumerable: false,
        configurable: true
    });
    SentryAppPublishRequestModal.prototype.render = function () {
        var _this = this;
        var app = this.props.app;
        var endpoint = "/sentry-apps/" + app.slug + "/publish-request/";
        var forms = [
            {
                title: t('Questions to answer'),
                fields: this.formFields,
            },
        ];
        return (<React.Fragment>
        <Header>{t('Publish Request Questionnaire')}</Header>
        <Body>
          <Explanation>
            {t("Please fill out this questionnaire in order to get your integration evaluated for publication.\n              Once your integration has been approved, users outside of your organization will be able to install it.")}
          </Explanation>
          <Form allowUndo apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} model={this.form} submitLabel={t('Request Publication')} onCancel={function () { return _this.props.closeModal(); }}>
            <JsonForm forms={forms}/>
          </Form>
        </Body>
      </React.Fragment>);
    };
    SentryAppPublishRequestModal.propTypes = {
        app: PropTypes.object.isRequired,
    };
    return SentryAppPublishRequestModal;
}(React.Component));
export default SentryAppPublishRequestModal;
var Explanation = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0px;\n  font-size: 18px;\n"], ["\n  margin: ", " 0px;\n  font-size: 18px;\n"])), space(1.5));
var templateObject_1;
//# sourceMappingURL=sentryAppPublishRequestModal.jsx.map