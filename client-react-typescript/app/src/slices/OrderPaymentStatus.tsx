import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { API } from "../conf.ts";

interface State {
    status: 'successful' | 'failure',
    loading: boolean
}

export const fetchOrderPaymentStatus = createAsyncThunk(
    'orderPaymentStatus/fetchOrderPaymentStatus',

    async (
        { orderId, bankOrderId }: { orderId: string, bankOrderId: string }
    ): Promise<'successful' | 'failure'> => {
        const response = await fetch(`${ API }/orders/${ orderId }/payment/check/?bankOrderId=${ bankOrderId }`, {
            credentials: 'include'
        })
        const { paymentStatus } = await response.json()
        return paymentStatus
    }
)

export const OrderPaymentStatusSlice = createSlice({
    name: 'orderPaymentStatus',

    initialState: {
        status: null,
        loading: false
    } as State,

    reducers: {},

    extraReducers: (builder) => (
        builder
            // FETCH PAYMENT STATUS
            .addCase(fetchOrderPaymentStatus.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchOrderPaymentStatus.fulfilled, (state, action) => {
                state.loading = false
                state.status = action.payload
            })
            .addCase(fetchOrderPaymentStatus.rejected, (state) => {
                state.loading = false
            })
    )
})

export const OrderPaymentStatusReducer = OrderPaymentStatusSlice.reducer