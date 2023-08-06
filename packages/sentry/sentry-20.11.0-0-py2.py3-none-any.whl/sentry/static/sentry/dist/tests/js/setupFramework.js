/* global process */
import '@visual-snapshot/jest';
process.on('unhandledRejection', function (reason) {
    // eslint-disable-next-line no-console
    console.error(reason);
});
//# sourceMappingURL=setupFramework.js.map