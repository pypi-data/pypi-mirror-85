import { __assign } from "tslib";
import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import accountDetailsFields from 'app/data/forms/accountDetails';
import { fields } from 'app/data/forms/projectGeneralSettings';
// @ts-expect-error
var user = TestStubs.User({});
describe('JsonForm', function () {
    describe('form prop', function () {
        it('default', function () {
            var wrapper = mountWithTheme(<JsonForm forms={accountDetailsFields} additionalFieldProps={{ user: user }}/>);
            expect(wrapper).toSnapshot();
        });
        it('missing additionalFieldProps required in "valid" prop', function () {
            // eslint-disable-next-line no-console
            console.error = jest.fn();
            try {
                mountWithTheme(<JsonForm forms={accountDetailsFields}/>);
            }
            catch (error) {
                expect(error.message).toBe("Cannot read property 'email' of undefined");
            }
        });
        it('should ALWAYS hide panel, if all fields have visible set to false  AND there is no renderHeader & renderFooter -  visible prop is of type boolean', function () {
            var modifiedAccountDetails = accountDetailsFields.map(function (accountDetailsField) { return (__assign(__assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(function (field) { return (__assign(__assign({}, field), { visible: false })); }) })); });
            var wrapper = mountWithTheme(<JsonForm forms={modifiedAccountDetails} additionalFieldProps={{ user: user }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
        it('should ALWAYS hide panel, if all fields have visible set to false AND there is no renderHeader & renderFooter -  visible prop is of type func', function () {
            var modifiedAccountDetails = accountDetailsFields.map(function (accountDetailsField) { return (__assign(__assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(function (field) { return (__assign(__assign({}, field), { visible: function () { return false; } })); }) })); });
            var wrapper = mountWithTheme(<JsonForm forms={modifiedAccountDetails} additionalFieldProps={{ user: user }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
        it('should NOT hide panel, if at least one field has visible set to true -  no visible prop (1 field) + visible prop is of type func (2 field)', function () {
            // accountDetailsFields has two fields. The second field will always have visible set to false, because the username and the email are the same 'foo@example.com'
            var wrapper = mountWithTheme(<JsonForm forms={accountDetailsFields} additionalFieldProps={{ user: user }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(1);
        });
        it('should NOT hide panel, if all fields have visible set to false AND a prop renderHeader is passed', function () {
            var modifiedAccountDetails = accountDetailsFields.map(function (accountDetailsField) { return (__assign(__assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(function (field) { return (__assign(__assign({}, field), { visible: false })); }) })); });
            var wrapper = mountWithTheme(<JsonForm forms={modifiedAccountDetails} additionalFieldProps={{ user: user }} renderHeader={function () { return <div>this is a Header </div>; }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(0);
        });
        it('should NOT hide panel, if all fields have visible set to false AND a prop renderFooter is passed', function () {
            var modifiedAccountDetails = accountDetailsFields.map(function (accountDetailsField) { return (__assign(__assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(function (field) { return (__assign(__assign({}, field), { visible: false })); }) })); });
            var wrapper = mountWithTheme(<JsonForm forms={modifiedAccountDetails} additionalFieldProps={{ user: user }} renderFooter={function () { return <div>this is a Footer </div>; }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(0);
        });
    });
    describe('fields prop', function () {
        var jsonFormFields = [fields.slug, fields.platform];
        it('default', function () {
            var wrapper = mountWithTheme(<JsonForm fields={jsonFormFields}/>);
            expect(wrapper).toSnapshot();
        });
        it('missing additionalFieldProps required in "valid" prop', function () {
            // eslint-disable-next-line no-console
            console.error = jest.fn();
            try {
                mountWithTheme(<JsonForm fields={[__assign(__assign({}, jsonFormFields[0]), { visible: function (_a) {
                            var test = _a.test;
                            return !!test.email;
                        } })]}/>);
            }
            catch (error) {
                expect(error.message).toBe("Cannot read property 'email' of undefined");
            }
        });
        it('should NOT hide panel, if at least one field has visible set to true - no visible prop', function () {
            // slug and platform have no visible prop, that means they will be always visible
            var wrapper = mountWithTheme(<JsonForm fields={jsonFormFields}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(2);
        });
        it('should NOT hide panel, if at least one field has visible set to true -  visible prop is of type boolean', function () {
            // slug and platform have no visible prop, that means they will be always visible
            var wrapper = mountWithTheme(<JsonForm fields={jsonFormFields.map(function (field) { return (__assign(__assign({}, field), { visible: true })); })}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(2);
        });
        it('should NOT hide panel, if at least one field has visible set to true -  visible prop is of type func', function () {
            // slug and platform have no visible prop, that means they will be always visible
            var wrapper = mountWithTheme(<JsonForm fields={jsonFormFields.map(function (field) { return (__assign(__assign({}, field), { visible: function () { return true; } })); })}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(2);
        });
        it('should ALWAYS hide panel, if all fields have visible set to false -  visible prop is of type boolean', function () {
            // slug and platform have no visible prop, that means they will be always visible
            var wrapper = mountWithTheme(<JsonForm fields={jsonFormFields.map(function (field) { return (__assign(__assign({}, field), { visible: false })); })}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
        it('should ALWAYS hide panel, if all fields have visible set to false - visible prop is of type function', function () {
            // slug and platform have no visible prop, that means they will be always visible
            var wrapper = mountWithTheme(<JsonForm fields={jsonFormFields.map(function (field) { return (__assign(__assign({}, field), { visible: function () { return false; } })); })}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
    });
});
//# sourceMappingURL=jsonForm.spec.jsx.map