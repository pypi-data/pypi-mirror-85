import React from 'react';
import { t } from 'app/locale';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import OptionSelector from 'app/components/charts/optionSelector';
export default function ChartFooter(_a) {
    var total = _a.total, yAxisValue = _a.yAxisValue, yAxisOptions = _a.yAxisOptions, onAxisChange = _a.onAxisChange, displayMode = _a.displayMode, displayOptions = _a.displayOptions, onDisplayChange = _a.onDisplayChange;
    var elements = [];
    elements.push(<SectionHeading key="total-label">{t('Total Events')}</SectionHeading>);
    elements.push(total === null ? (<SectionValue data-test-id="loading-placeholder" key="total-value">
        &mdash;
      </SectionValue>) : (<SectionValue key="total-value">{total.toLocaleString()}</SectionValue>));
    return (<ChartControls>
      <InlineContainer>{elements}</InlineContainer>
      <InlineContainer>
        <OptionSelector title={t('Display')} selected={displayMode} options={displayOptions} onChange={onDisplayChange} menuWidth="170px"/>
        <OptionSelector title={t('Y-Axis')} selected={yAxisValue} options={yAxisOptions} onChange={onAxisChange}/>
      </InlineContainer>
    </ChartControls>);
}
//# sourceMappingURL=chartFooter.jsx.map