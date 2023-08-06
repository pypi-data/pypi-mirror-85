import platforms from 'app/data/platforms';
export default function getPlatformName(platform) {
    var platformData = platforms.find(function (_a) {
        var id = _a.id;
        return platform === id;
    });
    return platformData ? platformData.name : null;
}
//# sourceMappingURL=getPlatformName.jsx.map