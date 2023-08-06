import React from 'react';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconPrevious, IconNext } from 'app/icons';
var NavigationButtonGroup = function (_a) {
    var location = _a.location, urls = _a.urls, _b = _a.hasNext, hasNext = _b === void 0 ? false : _b, _c = _a.hasPrevious, hasPrevious = _c === void 0 ? false : _c, className = _a.className;
    return (<ButtonBar className={className} merged>
    <Button size="small" to={{ pathname: urls[0], query: location.query }} disabled={!hasPrevious} label={t('Oldest')} icon={<IconPrevious size="xs"/>}/>
    <Button size="small" to={{
        pathname: urls[1],
        query: location.query,
    }} disabled={!hasPrevious}>
      {t('Older')}
    </Button>
    <Button size="small" to={{ pathname: urls[2], query: location.query }} disabled={!hasNext}>
      {t('Newer')}
    </Button>
    <Button size="small" to={{ pathname: urls[3], query: location.query }} disabled={!hasNext} label={t('Newest')} icon={<IconNext size="xs"/>}/>
  </ButtonBar>);
};
export default NavigationButtonGroup;
//# sourceMappingURL=navigationButtonGroup.jsx.map