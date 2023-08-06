import { __extends, __makeTemplateObject, __read } from "tslib";
import isNil from 'lodash/isNil';
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { List, AutoSizer, CellMeasurer, CellMeasurerCache, } from 'react-virtualized';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import space from 'app/styles/space';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import Checkbox from 'app/components/checkbox';
import EventDataSection from 'app/components/events/eventDataSection';
import { Panel, PanelBody } from 'app/components/panels';
import DebugMetaStore, { DebugMetaActions } from 'app/stores/debugMetaStore';
import SearchBar from 'app/components/searchBar';
import { parseAddress, getImageRange } from 'app/components/events/interfaces/utils';
import ImageForBar from 'app/components/events/interfaces/imageForBar';
import { t, tct } from 'app/locale';
import ClippedBox from 'app/components/clippedBox';
import { IconWarning } from 'app/icons';
import DebugImage from './debugImage';
import { getFileName } from './utils';
var MIN_FILTER_LEN = 3;
var DEFAULT_CLIP_HEIGHT = 560;
var PANEL_MAX_HEIGHT = 600;
var cache = new CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 81,
});
var DebugMeta = /** @class */ (function (_super) {
    __extends(DebugMeta, _super);
    function DebugMeta() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            filter: '',
            debugImages: [],
            filteredImages: [],
            showUnused: false,
            showDetails: false,
            clipHeight: DEFAULT_CLIP_HEIGHT,
        };
        _this.panelBodyRef = React.createRef();
        _this.listRef = null;
        _this.onStoreChange = function (store) {
            _this.setState({
                filter: store.filter,
            });
        };
        _this.renderRow = function (_a) {
            var index = _a.index, key = _a.key, parent = _a.parent, style = _a.style;
            var _b = _this.props, orgId = _b.orgId, projectId = _b.projectId;
            var _c = _this.state, filteredImages = _c.filteredImages, showDetails = _c.showDetails;
            return (<CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        <DebugImage style={style} image={filteredImages[index]} orgId={orgId} projectId={projectId} showDetails={showDetails}/>
      </CellMeasurer>);
        };
        _this.handleOnReveal = function () {
            var panelBodyHeight = _this.state.panelBodyHeight;
            if (!panelBodyHeight) {
                return;
            }
            _this.setState({
                clipHeight: panelBodyHeight,
            });
        };
        _this.handleChangeShowUnused = function (event) {
            var showUnused = event.target.checked;
            _this.setState({ showUnused: showUnused });
        };
        _this.handleShowUnused = function () {
            _this.setState({ showUnused: true });
        };
        _this.handleChangeShowDetails = function (event) {
            var showDetails = event.target.checked;
            _this.setState({ showDetails: showDetails });
        };
        _this.handleChangeFilter = function (value) {
            if (value === void 0) { value = ''; }
            DebugMetaActions.updateFilter(value);
        };
        return _this;
    }
    DebugMeta.prototype.componentDidMount = function () {
        this.unsubscribeFromStore = DebugMetaStore.listen(this.onStoreChange, undefined);
        cache.clearAll();
        this.filterImages();
    };
    DebugMeta.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.showUnused !== this.state.showUnused ||
            prevState.filter !== this.state.filter) {
            this.filterImages();
        }
        if (!isEqual(prevState.foundFrame, this.state.foundFrame) ||
            this.state.showDetails !== prevState.showDetails ||
            prevState.showUnused !== this.state.showUnused ||
            (prevState.filter && !this.state.filter)) {
            this.updateGrid();
        }
        if (prevState.filteredImages.length === 0 && this.state.filteredImages.length > 0) {
            this.getPanelBodyHeight();
        }
    };
    DebugMeta.prototype.componentWillUnmount = function () {
        if (this.unsubscribeFromStore) {
            this.unsubscribeFromStore();
        }
    };
    DebugMeta.prototype.updateGrid = function () {
        var _a;
        cache.clearAll();
        (_a = this.listRef) === null || _a === void 0 ? void 0 : _a.forceUpdateGrid();
    };
    DebugMeta.prototype.getPanelBodyHeight = function () {
        var _a, _b;
        var panelBodyHeight = (_b = (_a = this.panelBodyRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetHeight;
        if (!panelBodyHeight) {
            return;
        }
        this.setState({ panelBodyHeight: panelBodyHeight });
    };
    DebugMeta.prototype.filterImage = function (image) {
        var _a, _b, _c, _d;
        var _e = this.state, showUnused = _e.showUnused, filter = _e.filter;
        var searchTerm = filter.trim().toLowerCase();
        if (searchTerm.length < MIN_FILTER_LEN) {
            if (showUnused) {
                return true;
            }
            // A debug status of `null` indicates that this information is not yet
            // available in an old event. Default to showing the image.
            if (image.debug_status !== 'unused') {
                return true;
            }
            // An unwind status of `null` indicates that symbolicator did not unwind.
            // Ignore the status in this case.
            if (!isNil(image.unwind_status) && image.unwind_status !== 'unused') {
                return true;
            }
            return false;
        }
        // When searching for an address, check for the address range of the image
        // instead of an exact match.
        if (searchTerm.indexOf('0x') === 0) {
            var needle = parseAddress(searchTerm);
            if (needle > 0) {
                var _f = __read(getImageRange(image), 2), startAddress = _f[0], endAddress = _f[1];
                return needle >= startAddress && needle < endAddress;
            }
        }
        return (
        // Prefix match for identifiers
        (((_a = image.code_id) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '').indexOf(searchTerm) === 0 ||
            (((_b = image.debug_id) === null || _b === void 0 ? void 0 : _b.toLowerCase()) || '').indexOf(searchTerm) === 0 ||
            // Any match for file paths
            (((_c = image.code_file) === null || _c === void 0 ? void 0 : _c.toLowerCase()) || '').indexOf(searchTerm) >= 0 ||
            (((_d = image.debug_file) === null || _d === void 0 ? void 0 : _d.toLowerCase()) || '').indexOf(searchTerm) >= 0);
    };
    DebugMeta.prototype.filterImages = function () {
        var _this = this;
        var foundFrame = this.getFrame();
        // skip null values indicating invalid debug images
        var debugImages = this.getDebugImages();
        var filteredImages = debugImages.filter(function (image) { return _this.filterImage(image); });
        this.setState({ debugImages: debugImages, filteredImages: filteredImages, foundFrame: foundFrame });
    };
    DebugMeta.prototype.isValidImage = function (image) {
        // in particular proguard images do not have a code file, skip them
        if (image === null || image.code_file === null || image.type === 'proguard') {
            return false;
        }
        if (getFileName(image.code_file) === 'dyld_sim') {
            // this is only for simulator builds
            return false;
        }
        return true;
    };
    DebugMeta.prototype.getFrame = function () {
        var _a, _b, _c, _d, _e;
        var entries = this.props.event.entries;
        var frames = (_e = (_d = (_c = (_b = (_a = entries.find(function (_a) {
            var type = _a.type;
            return type === 'exception';
        })) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.values) === null || _c === void 0 ? void 0 : _c[0]) === null || _d === void 0 ? void 0 : _d.stacktrace) === null || _e === void 0 ? void 0 : _e.frames;
        if (!frames) {
            return undefined;
        }
        var searchTerm = this.state.filter.toLowerCase();
        return frames.find(function (frame) { var _a; return ((_a = frame.instructionAddr) === null || _a === void 0 ? void 0 : _a.toLowerCase()) === searchTerm; });
    };
    DebugMeta.prototype.getDebugImages = function () {
        var _this = this;
        var images = this.props.data.images;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        var filtered = images.filter(function (image) { return _this.isValidImage(image); });
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        filtered.sort(function (a, b) { return parseAddress(a.image_addr) - parseAddress(b.image_addr); });
        return filtered;
    };
    DebugMeta.prototype.getNoImagesMessage = function () {
        var _a = this.state, filter = _a.filter, showUnused = _a.showUnused, debugImages = _a.debugImages;
        if (debugImages.length === 0) {
            return t('No loaded images available.');
        }
        if (!showUnused && !filter) {
            return tct('No images are referenced in the stack trace. [toggle: Show Unreferenced]', {
                toggle: <Button priority="link" onClick={this.handleShowUnused}/>,
            });
        }
        return t('Sorry, no images match your query.');
    };
    DebugMeta.prototype.renderToolbar = function () {
        var _a = this.state, filter = _a.filter, showDetails = _a.showDetails, showUnused = _a.showUnused;
        return (<ToolbarWrapper>
        <Label>
          <Checkbox checked={showDetails} onChange={this.handleChangeShowDetails}/>
          {t('details')}
        </Label>

        <Label>
          <Checkbox checked={showUnused || !!filter} disabled={!!filter} onChange={this.handleChangeShowUnused}/>
          {t('show unreferenced')}
        </Label>
        <SearchInputWrapper>
          <StyledSearchBar onChange={this.handleChangeFilter} query={filter} placeholder={t('Search images\u2026')}/>
        </SearchInputWrapper>
      </ToolbarWrapper>);
    };
    DebugMeta.prototype.getListHeight = function () {
        var _a = this.state, showUnused = _a.showUnused, showDetails = _a.showDetails, panelBodyHeight = _a.panelBodyHeight;
        if (!panelBodyHeight ||
            panelBodyHeight > PANEL_MAX_HEIGHT ||
            showUnused ||
            showDetails) {
            return PANEL_MAX_HEIGHT;
        }
        return panelBodyHeight;
    };
    DebugMeta.prototype.renderImageList = function () {
        var _this = this;
        var _a = this.state, filteredImages = _a.filteredImages, showDetails = _a.showDetails, panelBodyHeight = _a.panelBodyHeight, clipHeight = _a.clipHeight;
        var _b = this.props, orgId = _b.orgId, projectId = _b.projectId;
        if (!panelBodyHeight) {
            return filteredImages.map(function (filteredImage) { return (<DebugImage key={filteredImage.debug_id} image={filteredImage} orgId={orgId} projectId={projectId} showDetails={showDetails}/>); });
        }
        return (<AutoSizer disableHeight>
        {function (_a) {
            var width = _a.width;
            return (<StyledList ref={function (el) {
                _this.listRef = el;
            }} deferredMeasurementCache={cache} height={_this.getListHeight()} overscanRowCount={5} rowCount={filteredImages.length} rowHeight={cache.rowHeight} rowRenderer={_this.renderRow} width={width} isScrolling={false} overflowHidden={panelBodyHeight > clipHeight}/>);
        }}
      </AutoSizer>);
    };
    DebugMeta.prototype.render = function () {
        var _a = this.state, filteredImages = _a.filteredImages, foundFrame = _a.foundFrame, panelBodyHeight = _a.panelBodyHeight, clipHeight = _a.clipHeight;
        return (<StyledEventDataSection type="packages" title={<GuideAnchor target="packages" position="bottom">
            <h3>{t('Images Loaded')}</h3>
          </GuideAnchor>} actions={this.renderToolbar()} wrapTitle={false} isCentered>
        <DebugImagesPanel>
          {filteredImages.length > 0 ? (<ClippedBox clipHeight={clipHeight} renderedHeight={panelBodyHeight} onReveal={this.handleOnReveal}>
              {foundFrame && (<ImageForBar frame={foundFrame} onShowAllImages={this.handleChangeFilter}/>)}
              <PanelBody forwardRef={this.panelBodyRef}>
                {this.renderImageList()}
              </PanelBody>
            </ClippedBox>) : (<EmptyMessage icon={<IconWarning size="xl"/>}>
              {this.getNoImagesMessage()}
            </EmptyMessage>)}
        </DebugImagesPanel>
      </StyledEventDataSection>);
    };
    DebugMeta.defaultProps = {
        data: { images: [] },
    };
    return DebugMeta;
}(React.PureComponent));
export default DebugMeta;
var StyledList = styled(List)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n  height: auto !important;\n  max-height: ", "px;\n  outline: none;\n"], ["\n  ", "\n  height: auto !important;\n  max-height: ", "px;\n  outline: none;\n"])), function (p) { return p.overflowHidden && 'overflow: hidden !important;'; }, function (p) { return p.height; });
var Label = styled('label')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: normal;\n  margin-right: 1em;\n  margin-bottom: 0;\n\n  > input {\n    margin-right: 1ex;\n  }\n"], ["\n  font-weight: normal;\n  margin-right: 1em;\n  margin-bottom: 0;\n\n  > input {\n    margin-right: 1ex;\n  }\n"])));
var StyledEventDataSection = styled(EventDataSection)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    padding-bottom: ", ";\n  }\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"], ["\n  @media (max-width: ", ") {\n    padding-bottom: ", ";\n  }\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(4), function (p) { return p.theme.breakpoints[0]; }, space(2));
var DebugImagesPanel = styled(Panel)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  max-height: ", "px;\n  overflow: hidden;\n"], ["\n  margin-bottom: ", ";\n  max-height: ", "px;\n  overflow: hidden;\n"])), space(1), PANEL_MAX_HEIGHT);
var ToolbarWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  @media (max-width: ", ") {\n    flex-wrap: wrap;\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  @media (max-width: ", ") {\n    flex-wrap: wrap;\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var SearchInputWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  max-width: 180px;\n  display: inline-block;\n  @media (max-width: ", ") {\n    width: 100%;\n    max-width: 100%;\n    margin-top: ", ";\n  }\n"], ["\n  max-width: 180px;\n  display: inline-block;\n  @media (max-width: ", ") {\n    width: 100%;\n    max-width: 100%;\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
var StyledSearchBar = styled(SearchBar)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  .search-input {\n    height: 30px;\n  }\n"], ["\n  .search-input {\n    height: 30px;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map