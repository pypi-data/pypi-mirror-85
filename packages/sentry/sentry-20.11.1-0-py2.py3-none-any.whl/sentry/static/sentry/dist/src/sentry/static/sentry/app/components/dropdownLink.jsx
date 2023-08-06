import { __assign, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import DropdownMenu from 'app/components/dropdownMenu';
import { IconChevron } from 'app/icons';
var DropdownLink = function (_a) {
    var anchorRight = _a.anchorRight, disabled = _a.disabled, title = _a.title, caret = _a.caret, children = _a.children, menuClasses = _a.menuClasses, className = _a.className, alwaysRenderMenu = _a.alwaysRenderMenu, topLevelClasses = _a.topLevelClasses, otherProps = __rest(_a, ["anchorRight", "disabled", "title", "caret", "children", "menuClasses", "className", "alwaysRenderMenu", "topLevelClasses"]);
    return (<DropdownMenu alwaysRenderMenu={alwaysRenderMenu} {...otherProps}>
    {function (_a) {
        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
        var shouldRenderMenu = alwaysRenderMenu || isOpen;
        var cx = classNames('dropdown-actor', className, {
            'dropdown-menu-right': anchorRight,
            'dropdown-toggle': true,
            hover: isOpen,
            disabled: disabled,
        });
        var topLevelCx = classNames('dropdown', topLevelClasses, {
            'pull-right': anchorRight,
            'anchor-right': anchorRight,
            open: isOpen,
        });
        return (<span {...getRootProps({
            className: topLevelCx,
        })}>
          <a {...getActorProps({
            className: cx,
        })}>
            <div className="dropdown-actor-title">
              <span>{title}</span>
              {caret && <IconChevron direction="down" size="xs"/>}
            </div>
          </a>

          {shouldRenderMenu && (<ul {...getMenuProps({
            className: classNames(menuClasses, 'dropdown-menu'),
        })}>
              {children}
            </ul>)}
        </span>);
    }}
  </DropdownMenu>);
};
DropdownLink.defaultProps = {
    alwaysRenderMenu: true,
    disabled: false,
    anchorRight: false,
    caret: true,
};
DropdownLink.propTypes = __assign(__assign({}, DropdownMenu.propTypes), { title: PropTypes.node, caret: PropTypes.bool, disabled: PropTypes.bool, anchorRight: PropTypes.bool, alwaysRenderMenu: PropTypes.bool, topLevelClasses: PropTypes.string, menuClasses: PropTypes.string });
export default DropdownLink;
//# sourceMappingURL=dropdownLink.jsx.map