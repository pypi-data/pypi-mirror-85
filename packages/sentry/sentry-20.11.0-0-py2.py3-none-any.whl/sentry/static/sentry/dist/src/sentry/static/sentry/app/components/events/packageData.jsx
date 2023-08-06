import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import ClippedBox from 'app/components/clippedBox';
import ErrorBoundary from 'app/components/errorBoundary';
import EventDataSection from 'app/components/events/eventDataSection';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
import SentryTypes from 'app/sentryTypes';
var EventPackageData = /** @class */ (function (_super) {
    __extends(EventPackageData, _super);
    function EventPackageData() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventPackageData.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event.id !== nextProps.event.id;
    };
    EventPackageData.prototype.render = function () {
        var event = this.props.event;
        var longKeys, title;
        var packages = Object.entries(event.packages || {});
        switch (event.platform) {
            case 'csharp':
                longKeys = true;
                title = t('Assemblies');
                break;
            default:
                longKeys = false;
                title = t('Packages');
        }
        return (<EventDataSection type="packages" title={title}>
        <ClippedBox>
          <ErrorBoundary mini>
            <KeyValueList data={packages} longKeys={longKeys}/>
          </ErrorBoundary>
        </ClippedBox>
      </EventDataSection>);
    };
    EventPackageData.propTypes = {
        event: SentryTypes.Event.isRequired,
    };
    return EventPackageData;
}(React.Component));
export default EventPackageData;
//# sourceMappingURL=packageData.jsx.map