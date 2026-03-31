import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import type { Order } from '../interfaces/OrderInterface.ts';
import { API } from '../conf.ts';
import type { OrderItem } from '../interfaces/OrderItemInterface.ts';
import { getCookie } from '../utils.ts';

interface State {
    orders: Array<Order>,
    loading: boolean
}

export const fetchOrders = createAsyncThunk(
    'orders/fetchOrders',

    async (): Promise<Array<Order>> => {
        const response = await fetch(`${API}/orders/`, {
            method: 'GET',
            credentials: 'include'
        })
        const data = await response.json() as Array<any>
        return data.map(order => (
            {
                id: order.id,
                price: order.price,
                status: order.status,
                items: order.products.map(orderItem => (
                    {
                        product: orderItem.product,
                        price: orderItem.price,
                        amount: orderItem.amount
                    } as OrderItem
                ))
            } as Order
        ))
    }
)

export const createOrder = createAsyncThunk(
    'orders/createOrder',

    async (): Promise<Order> => {
        const response = await fetch(`${API}/orders/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')!
            }
        })
        const { order, formUrl } = await response.json()
        window.open(formUrl, '_blank')

        return {
            id: order.id,
            price: order.price,
            status: order.status,
            items: order.products.map((orderItem: any) => (
                {
                    product: orderItem.product,
                    price: orderItem.price,
                    amount: orderItem.amount
                } as OrderItem
            ))
        } as Order
    }
)

export const OrdersSlice = createSlice({
    name: 'orders',

    initialState: {
        orders: [] as Array<Order>,
        loading: false
    } as State,

    reducers: {},

    extraReducers: (builder) => {
        builder
            // FETCH ORDERS
            .addCase(fetchOrders.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchOrders.fulfilled, (state, action) => {
                state.orders = action.payload
                state.loading = false
            })
            .addCase(fetchOrders.rejected, (state) => {
                state.orders = []
                state.loading = false
            })

            // CREATE ORDER
            .addCase(createOrder.pending, (state) => {
                state.loading = true
            })
            .addCase(createOrder.fulfilled, (state, action) => {
                state.orders.push(action.payload)
                state.loading = false
            })
            .addCase(createOrder.rejected, (state) => {
                state.orders = []
                state.loading = false
            })
    }
})

export const ordersReducer = OrdersSlice.reducer