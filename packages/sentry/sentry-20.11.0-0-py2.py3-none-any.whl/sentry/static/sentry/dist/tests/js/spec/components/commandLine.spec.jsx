import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import CommandLine from 'app/components/commandLine';
describe('CommandLine', function () {
    it('renders', function () {
        var children = 'sentry devserver --workers';
        var wrapper = mountWithTheme(<CommandLine>{children}</CommandLine>);
        expect(wrapper.find('CommandLine').text()).toBe(children);
    });
});
//# sourceMappingURL=commandLine.spec.jsx.map