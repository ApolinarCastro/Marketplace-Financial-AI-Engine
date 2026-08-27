/**
 * Marketplace Financial AI Engine — Shared UI Formatting Utilities
 * Single Source of Truth for Currency, Percentage, and Number Formatting in Frontend Templates.
 */
(function(global) {
    'use strict';

    const CLP_FORMATTER = new Intl.NumberFormat("es-CL", {
        style: "currency",
        currency: "CLP",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });

    const NUMBER_FORMATTER = new Intl.NumberFormat("es-CL", {
        maximumFractionDigits: 0
    });

    function formatCLP(value) {
        const amount = Number(value);
        if (!Number.isFinite(amount)) {
            return "$0";
        }
        return CLP_FORMATTER.format(Math.round(amount));
    }

    function formatNumber(value) {
        const amount = Number(value);
        if (!Number.isFinite(amount)) {
            return "0";
        }
        return NUMBER_FORMATTER.format(Math.round(amount));
    }

    function formatPercent(value, decimals = 1) {
        const num = Number(value);
        if (!Number.isFinite(num)) {
            return "0.0%";
        }
        const sign = num > 0 ? "+" : "";
        return sign + num.toFixed(decimals) + "%";
    }

    function formatShort(value, prefix = '') {
        if (value === null || value === undefined || isNaN(value)) {
            return prefix + '0';
        }
        const num = Number(value);
        const abs = Math.abs(num);
        const sign = num < 0 ? '-' : '';
        let formatted = '0';
        if (abs >= 1e9) {
            formatted = (abs / 1e9).toFixed(2) + 'B';
        } else if (abs >= 1e6) {
            formatted = (abs / 1e6).toFixed(1) + 'M';
        } else if (abs >= 1e3) {
            formatted = (abs / 1e3).toFixed(0) + 'K';
        } else {
            formatted = abs.toFixed(0);
        }
        return sign + prefix + formatted;
    }

    // Global exports for backwards compatibility & window object attachment
    global.CLP_FORMATTER = CLP_FORMATTER;
    global.formatCLP = formatCLP;
    global.fmtCLP = formatCLP;
    global.formatNumber = formatNumber;
    global.fmtNumber = formatNumber;
    global.formatPercent = formatPercent;
    global.fmtPercent = formatPercent;
    global.formatShort = formatShort;
    global.fmtShort = function(v) { return formatShort(v, ''); };
    global.fmtShortCurrency = function(v) { return formatShort(v, '$'); };

})(typeof window !== 'undefined' ? window : this);
