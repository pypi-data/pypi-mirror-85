import React from 'react';
import { t } from 'app/locale';
export function getGroupingChanges(project, groupingConfigs, groupingEnhancementBases) {
    var _a, _b;
    var byId = {};
    var updateNotes = '';
    var riskLevel = 0;
    var latestGroupingConfig = null;
    var latestEnhancementsBase = null;
    groupingConfigs.forEach(function (cfg) {
        byId[cfg.id] = cfg;
        if (cfg.latest && project.groupingConfig !== cfg.id) {
            updateNotes = cfg.changelog;
            latestGroupingConfig = cfg;
            riskLevel = cfg.risk;
        }
    });
    if (latestGroupingConfig) {
        var next = (_a = latestGroupingConfig.base) !== null && _a !== void 0 ? _a : '';
        while (next !== project.groupingConfig) {
            var cfg = byId[next];
            if (!cfg) {
                break;
            }
            riskLevel = Math.max(riskLevel, cfg.risk);
            updateNotes = cfg.changelog + '\n' + updateNotes;
            next = (_b = cfg.base) !== null && _b !== void 0 ? _b : '';
        }
    }
    groupingEnhancementBases.forEach(function (base) {
        if (base.latest && project.groupingEnhancementsBase !== base.id) {
            updateNotes += '\n\n' + base.changelog;
            latestEnhancementsBase = base;
        }
    });
    return { updateNotes: updateNotes, riskLevel: riskLevel, latestGroupingConfig: latestGroupingConfig, latestEnhancementsBase: latestEnhancementsBase };
}
export function getGroupingRisk(riskLevel) {
    switch (riskLevel) {
        case 0:
            return {
                riskNote: t('This upgrade has the chance to create some new issues.'),
                alertType: 'info',
            };
        case 1:
            return {
                riskNote: t('This upgrade will create some new issues.'),
                alertType: 'warning',
            };
        case 2:
            return {
                riskNote: (<strong>
            {t('The new grouping strategy is incompatible with the current and will create entirely new issues.')}
          </strong>),
                alertType: 'error',
            };
        default:
            return { riskNote: undefined, alertType: undefined };
    }
}
//# sourceMappingURL=utils.jsx.map