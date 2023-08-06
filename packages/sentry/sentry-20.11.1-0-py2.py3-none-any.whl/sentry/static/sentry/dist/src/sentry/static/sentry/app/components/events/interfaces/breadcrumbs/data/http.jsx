import React from 'react';
import omit from 'lodash/omit';
import ExternalLink from 'app/components/links/externalLink';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import Highlight from 'app/components/highlight';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import Summary from './summary';
var Http = function (_a) {
    var breadcrumb = _a.breadcrumb, searchTerm = _a.searchTerm;
    var data = breadcrumb.data;
    var renderUrl = function (url) {
        if (typeof url === 'string') {
            var content = <Highlight text={searchTerm}>{url}</Highlight>;
            return url.match(/^https?:\/\//) ? (<ExternalLink data-test-id="http-renderer-external-link" href={url}>
          {content}
        </ExternalLink>) : (<span>{content}</span>);
        }
        try {
            return <Highlight text={searchTerm}>{JSON.stringify(url)}</Highlight>;
        }
        catch (_a) {
            return t('Invalid URL');
        }
    };
    var statusCode = data === null || data === void 0 ? void 0 : data.status_code;
    return (<Summary kvData={omit(data, ['method', 'url', 'status_code'])} searchTerm={searchTerm}>
      {(data === null || data === void 0 ? void 0 : data.method) && (<AnnotatedText value={<strong>
              <Highlight text={searchTerm}>{data.method + " "}</Highlight>
            </strong>} meta={getMeta(data, 'method')}/>)}
      {(data === null || data === void 0 ? void 0 : data.url) && (<AnnotatedText value={renderUrl(data.url)} meta={getMeta(data, 'url')}/>)}
      {defined(statusCode) && (<AnnotatedText value={<Highlight data-test-id="http-renderer-status-code" text={searchTerm}>{" [" + statusCode + "]"}</Highlight>} meta={getMeta(data, 'status_code')}/>)}
    </Summary>);
};
export default Http;
//# sourceMappingURL=http.jsx.map