import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { getMeta } from 'app/components/events/meta/metaProxy';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import space from 'app/styles/space';
import TextOverflow from 'app/components/textOverflow';
import ContextSummaryNoSummary from './contextSummaryNoSummary';
import generateClassName from './generateClassName';
import Item from './item';
var ContextSummaryGeneric = function (_a) {
    var data = _a.data, unknownTitle = _a.unknownTitle;
    if (Object.keys(data).length === 0) {
        return <ContextSummaryNoSummary title={unknownTitle}/>;
    }
    var renderValue = function (key) {
        var meta = getMeta(data, key);
        return <AnnotatedText value={data[key]} meta={meta}/>;
    };
    var className = generateClassName(data.name);
    return (<Item className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderValue('name')}</h3>
      <TextOverflow isParagraph>
        <Subject>{t('Version:')}</Subject>
        {!data.version ? t('Unknown') : renderValue('version')}
      </TextOverflow>
    </Item>);
};
export default ContextSummaryGeneric;
var Subject = styled('strong')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryGeneric.jsx.map