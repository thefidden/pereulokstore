import styled from 'styled-components';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'

import { fetchUser } from './slices/UserSlice.ts';
import { fetchCart } from './slices/CartSlice.ts';
import { fetchOrders } from './slices/OrdersSlice.ts';
import { useAppDispatch, useAppSelector } from './store.ts';

import StorePage from './pages/StorePage.tsx';
import ProductPage from './pages/ProductPage.tsx';
import CartPage from './pages/CartPage.tsx';
import OrdersPage from './pages/OrdersPage.tsx';
import OrderCheckPaymentPage from './pages/OrderCheckPaymentPage.tsx';
import Header from "./components/Header.tsx";

const Root = styled.div`
    max-width: 1440px;

    padding: 40px 0;
    margin: 0 auto;

    display: flex;
    flex-direction: column;
    gap: 80px;
`

export default function App() {
    const dispatch = useAppDispatch()

    const { user } = useAppSelector(state => state.user)
    const { cart } = useAppSelector(state => state.cart)
    const { orders } = useAppSelector(state => state.orders)

    useEffect(() => {
        dispatch(fetchUser())
        dispatch(fetchCart())
        dispatch(fetchOrders())
    }, [])

    useEffect(() => console.log(user), [user])
    useEffect(() => console.log(cart), [cart])
    useEffect(() => console.log(orders), [orders])

    return (
        <Router>
            <Root>
                <Header />
                <Routes>
                    <Route path = "/" element = { <Navigate to = "store?type=suit" replace /> } />
                    <Route path = "/store" element = { <StorePage /> } />
                    <Route path = "/product/:productUUID" element = { <ProductPage /> } />
                    <Route path = "/cart" element = { <CartPage /> } />
                    <Route path = "/orders" element = { <OrdersPage /> } />
                    <Route path = "/orders/:orderUUID/payment/check" element = { <OrderCheckPaymentPage /> } />
                </Routes>
            </Root>
        </Router>
    )
}

