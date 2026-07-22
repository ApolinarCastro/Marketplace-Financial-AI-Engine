/**
 * api_client.js
 * Centralized safe fetch wrapper and contract guards for the Financial Engine
 */

window.ApiClient = {
    /**
     * SAFE_FETCH: Wraps native fetch with error handling and JSON parsing
     */
    async safeFetch(url, options = {}) {
        try {
            const res = await fetch(url, options);
            if (!res.ok) {
                let errorMsg = `HTTP Error ${res.status}`;
                try {
                    const errorData = await res.json();
                    if (errorData.detail) errorMsg = errorData.detail;
                } catch(e) {}
                throw new Error(errorMsg);
            }
            return await res.json();
        } catch (error) {
            console.error(`[API_CLIENT] Fetch error for ${url}:`, error);
            throw error; // Re-throw for specific component handling if needed
        }
    },

    /**
     * CONTRACT_GUARD: Validates that critical numeric fields are not NaN or undefined
     */
    validateFinancialContract(data, contractType) {
        if (!data) throw new Error(`[INVALID_CONTRACT] Data is null or undefined for ${contractType}`);

        const checkNumeric = (val, fieldName) => {
            if (val === undefined) {
                console.error(`[INVALID_CONTRACT] Missing field: ${fieldName} in ${contractType}`);
                throw new Error(`INVALID_CONTRACT: Missing field ${fieldName}`);
            }
            if (Number.isNaN(val) || val === 'NaN') {
                console.error(`[INVALID_CONTRACT] NaN value for field: ${fieldName} in ${contractType}`);
                throw new Error(`INVALID_CONTRACT: NaN value in ${fieldName}`);
            }
        };

        if (contractType === 'summary') {
            checkNumeric(data.gross_sales, 'gross_sales');
            checkNumeric(data.devoluciones, 'devoluciones');
            checkNumeric(data.costos_operacionales, 'costos_operacionales');
            checkNumeric(data.comisiones, 'comisiones');
            checkNumeric(data.ajustes, 'ajustes');
            checkNumeric(data.recuperaciones, 'recuperaciones');
            checkNumeric(data.neto, 'neto');
        } else if (contractType === 'waterfall') {
            if (!Array.isArray(data)) throw new Error('INVALID_CONTRACT: waterfall must be an array');
            data.forEach(item => {
                checkNumeric(item.monto, 'monto');
            });
        }
        // Return data unmodified if it passes
        return data;
    },

    /**
     * Endpoints
     */
    async getPeriodos() {
        return this.safeFetch('/api/v4/periodos');
    },
    
    async getSummary(mp, periodo, options = {}) {
        let url = `/api/v4/exec/summary?periodo=${periodo}`;
        if (mp && mp !== 'ALL') url += `&marketplace=${mp}`;
        const data = await this.safeFetch(url, options);
        return this.validateFinancialContract(data, 'summary');
    },

    async getFinancialStructure(mp, periodo, options = {}) {
        let url = `/api/v4/financial-structure?periodo=${periodo}`;
        if (mp && mp !== 'ALL') url += `&marketplace=${mp}`;
        return this.safeFetch(url, options);
    },

    async getWaterfall(mp, periodo, options = {}) {
        let url = `/api/v4/exec/waterfall-v3?periodo=${periodo}`;
        if (mp && mp !== 'ALL') url += `&marketplace=${mp}`;
        const data = await this.safeFetch(url, options);
        return this.validateFinancialContract(data, 'waterfall');
    },
    
    async getLedger(mp, periodo, offset=0, orderId=null, options = {}) {
        let url = `/api/v4/ledger?marketplace=${mp}`;
        if (periodo && periodo !== 'YTD') url += `&periodo=${periodo}`;
        if (orderId) url += `&order_id=${orderId}`;
        else url += `&offset=${offset}`;
        return this.safeFetch(url, options);
    },
    
    async runAudit(mp) {
        return this.safeFetch(`/api/v4/run-audit?marketplace=${mp}`, { method: 'POST' });
    },

    /**
     * DETALLE_TO_CONCEPT: Maps ledger 'detalle' values to financial concepts
     */
    DETALLE_TO_CONCEPT: {
        'Cargo por venta (Comisión)': 'Comisiones',
        'Comisiones sobre pedidos': 'Comisiones',
        'Comisión por venta': 'Comisiones',
        'Comisiones': 'Comisiones',
        'Comisión de reembolso': 'Comisiones',
        'Cargo por envíos de Mercado Libre': 'Logística',
        'Cargo por Mercado Envíos': 'Logística',
        'Envío': 'Logística',
        'Gastos de envío (RIPLEY) pagados por el operador': 'Logística',
        'Gastos de envío (RIPLEY)': 'Logística',
        'Importe del envío del pedido': 'Logística',
        'Despacho': 'Logística',
        'Cobro por despacho': 'Logística',
        'Logística inversa': 'Logística',
        'Compensación logística': 'Logística',
        'Cofinanciamiento logístico': 'Logística',
        'Recargo por precio mínimo': 'Logística',
        'Descuento por costo logístico': 'Logística',
        'Descuento por logística inversa': 'Logística',
        'Mercado Envíos': 'Logística',
        'Descuento logistico': 'Logística',
        'Cobro por cofinanciamiento logistico': 'Logística',
        'Product Ads': 'Publicidad',
        'Cargo por publicidad': 'Publicidad',
        'Cargo por publicación': 'Publicidad',
        'Publicidad': 'Publicidad',
        'Costo de Marketing': 'Publicidad',
        'Cargo por Asesoría Comercial': 'Servicios',
        'Asesoría Comercial': 'Servicios',
        'Cargo por Mi Página': 'Servicios',
        'Mi Página': 'Servicios',
        'Full': 'Fulfillment',
        'Costo Full': 'Fulfillment',
        'Almacenamiento': 'Fulfillment',
        'Retiro stock': 'Fulfillment',
        'Stock antiguo': 'Fulfillment',
        'Cobro por almacenamiento': 'Fulfillment',
    },

    /**
     * mapDetalleToConcept: Classifies a ledger 'detalle' string into a financial concept
     */
    mapDetalleToConcept(detalle) {
        if (!detalle) return 'Otros';
        const direct = this.DETALLE_TO_CONCEPT[detalle];
        if (direct) return direct;
        const lower = detalle.toLowerCase();
        for (const [key, val] of Object.entries(this.DETALLE_TO_CONCEPT)) {
            if (lower.includes(key.toLowerCase())) return val;
        }
        if (lower.includes('bonificación') || lower.includes('incentivo')) return 'Bonificaciones';
        if (lower.includes('comisión') || lower.includes('comision')) return 'Comisiones';
        if (lower.includes('envío') || lower.includes('envio') || lower.includes('logísti') || lower.includes('despacho')) return 'Logística';
        if (lower.includes('publicidad') || lower.includes('ads')) return 'Publicidad';
        if (lower.includes('full') || lower.includes('almacen')) return 'Fulfillment';
        if (lower.includes('asesoría')) return 'Servicios';
        if (lower.includes('devolución') || lower.includes('devolucion') || lower.includes('reembolso') || lower.includes('refund')) return 'Devoluciones';
        return 'Otros';
    }
};
