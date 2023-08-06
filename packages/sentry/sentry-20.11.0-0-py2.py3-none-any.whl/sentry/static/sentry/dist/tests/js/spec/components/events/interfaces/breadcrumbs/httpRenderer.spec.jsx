import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import HttpRenderer from 'app/components/events/interfaces/breadcrumbs/data/http';
import { BreadcrumbType, BreadcrumbLevelType, } from 'app/components/events/interfaces/breadcrumbs/types';
describe('HttpRenderer', function () {
    describe('render', function () {
        it('should work', function () {
            var httpRendererWrapper = mountWithTheme(<HttpRenderer searchTerm="" breadcrumb={{
                type: BreadcrumbType.HTTP,
                level: BreadcrumbLevelType.INFO,
                data: {
                    method: 'POST',
                    url: 'http://example.com/foo',
                    // status_code 0 is possible via broken client-side XHR; should still render as '[0]'
                    status_code: 0,
                },
            }}/>);
            var annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(3);
            expect(annotatedTexts.at(0).find('strong').text()).toEqual('POST ');
            expect(annotatedTexts.at(1).find('a[data-test-id="http-renderer-external-link"]').text()).toEqual('http://example.com/foo');
            expect(annotatedTexts
                .at(2)
                .find('Highlight[data-test-id="http-renderer-status-code"]')
                .text()).toEqual(' [0]');
        });
        it("shouldn't blow up if crumb.data is missing", function () {
            var httpRendererWrapper = mountWithTheme(<HttpRenderer searchTerm="" breadcrumb={{
                category: 'xhr',
                type: BreadcrumbType.HTTP,
                level: BreadcrumbLevelType.INFO,
            }}/>);
            var annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(0);
        });
        it("shouldn't blow up if url is not a string", function () {
            var httpRendererWrapper = mountWithTheme(<HttpRenderer searchTerm="" breadcrumb={{
                category: 'xhr',
                type: BreadcrumbType.HTTP,
                level: BreadcrumbLevelType.INFO,
                data: {
                    method: 'GET',
                },
            }}/>);
            var annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(1);
        });
    });
});
//# sourceMappingURL=httpRenderer.spec.jsx.map