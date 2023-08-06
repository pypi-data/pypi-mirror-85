import { __read } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueListV2';
import ContextData from 'app/components/contextData';
import { defined } from 'app/utils';
import ErrorBoundary from 'app/components/errorBoundary';
import ClippedBox from 'app/components/clippedBox';
import { t } from 'app/locale';
import getTransformedData from './getTransformedData';
var RichHttpContentClippedBoxBodySection = function (_a) {
    var value = _a.data, meta = _a.meta, inferredContentType = _a.inferredContentType;
    var getContent = function () {
        if (!defined(value)) {
            return null;
        }
        switch (inferredContentType) {
            case 'application/json':
                return (<ContextData data-test-id="rich-http-content-body-context-data" data={value} preserveQuotes/>);
            case 'application/x-www-form-urlencoded':
            case 'multipart/form-data':
                return (<KeyValueList data-test-id="rich-http-content-body-key-value-list" data={getTransformedData(value).map(function (_a) {
                    var _b = __read(_a, 2), key = _b[0], v = _b[1];
                    return ({
                        key: key,
                        subject: key,
                        value: v,
                        meta: meta,
                    });
                })} isContextData/>);
            default:
                return (<pre data-test-id="rich-http-content-body-section-pre">
            <AnnotatedText value={value && JSON.stringify(value, null, 2)} meta={meta} data-test-id="rich-http-content-body-context-data"/>
          </pre>);
        }
    };
    var content = getContent();
    return content ? (<ClippedBox title={t('Body')} defaultClipped>
      <ErrorBoundary mini>{content}</ErrorBoundary>
    </ClippedBox>) : null;
};
RichHttpContentClippedBoxBodySection.propTypes = {
    meta: PropTypes.object,
};
export default RichHttpContentClippedBoxBodySection;
//# sourceMappingURL=richHttpContentClippedBoxBodySection.jsx.map