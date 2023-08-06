import React from 'react';
import NavTabs from 'app/components/navTabs';
var SetupChoices = function (_a) {
    var choices = _a.choices, selectedChoice = _a.selectedChoice, onSelect = _a.onSelect;
    return (<NavTabs underlined>
    {choices.map(function (_a) {
        var id = _a.id, title = _a.title;
        return (<li key={id} className={id === selectedChoice ? 'active' : undefined}>
        <a href="#" data-test-id={"onboarding-getting-started-" + id} onClick={function (e) {
            onSelect(id);
            e.preventDefault();
        }}>
          {title}
        </a>
      </li>);
    })}
  </NavTabs>);
};
export default SetupChoices;
//# sourceMappingURL=setupChoices.jsx.map