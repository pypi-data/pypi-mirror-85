import { __extends } from "tslib";
import React from 'react';
import { getTitle } from 'app/utils/events';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import withOrganization from 'app/utils/withOrganization';
import StacktracePreview from './stacktracePreview';
var EventOrGroupTitle = /** @class */ (function (_super) {
    __extends(EventOrGroupTitle, _super);
    function EventOrGroupTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOrGroupTitle.prototype.render = function () {
        var _a = this.props, hasGuideAnchor = _a.hasGuideAnchor, data = _a.data, organization = _a.organization;
        var _b = getTitle(data, organization), title = _b.title, subtitle = _b.subtitle;
        var titleWithHoverStacktrace = (<StacktracePreview organization={organization} issueId={data.id}>
        {title}
      </StacktracePreview>);
        return subtitle ? (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target="issue_title" position="bottom">
          <span>{titleWithHoverStacktrace}</span>
        </GuideAnchor>
        <Spacer />
        <em title={subtitle}>{subtitle}</em>
        <br />
      </span>) : (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target="issue_title" position="bottom">
          {titleWithHoverStacktrace}
        </GuideAnchor>
      </span>);
    };
    return EventOrGroupTitle;
}(React.Component));
export default withOrganization(EventOrGroupTitle);
/**
 * &nbsp; is used instead of margin/padding to split title and subtitle
 * into 2 separate text nodes on the HTML AST. This allows the
 * title to be highlighted without spilling over to the subtitle.
 */
var Spacer = function () { return <span style={{ display: 'inline-block', width: 10 }}>&nbsp;</span>; };
//# sourceMappingURL=eventOrGroupTitle.jsx.map